import argparse
import ast
from typing import Optional, Set, Union
import libcst as cst
import os
import json
import sys


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:]


def is_literal_node(node: cst.BaseExpression) -> bool:
    """
    Check if the given node represents 'Literal', either as a bare name
    or as an attribute (e.g. typing.Literal).
    """
    if isinstance(node, cst.Name) and node.value == "Literal":
        return True
    if isinstance(node, cst.Attribute) and node.attr.value == "Literal":
        return True
    return False


def extract_literal_value(
    annotation: Union[cst.BaseExpression, cst.Annotation],
) -> Optional[str]:
    """
    Attempt to extract the literal value from an annotation if it represents
    either a Literal[...] or an Annotated[...] wrapping a Literal[...].
    """
    if isinstance(annotation, cst.Annotation):
        annotation = annotation.annotation

    if isinstance(annotation, cst.Subscript):
        # Direct Literal[...] case.
        if is_literal_node(annotation.value):
            if annotation.slice and isinstance(
                annotation.slice[0], cst.SubscriptElement
            ):
                index = annotation.slice[0].slice
                if isinstance(index, cst.Index):
                    expr = index.value
                    if isinstance(expr, cst.SimpleString):
                        try:
                            literal_value = ast.literal_eval(expr.value)
                            return literal_value
                        except Exception as e:
                            print(f"Error evaluating literal: {e}", file=sys.stderr)
                            return None
        # Annotated[...] wrapping a Literal[...] case.
        if (
            isinstance(annotation.value, cst.Name)
            and annotation.value.value == "Annotated"
        ):
            if annotation.slice:
                first_elem = annotation.slice[0].slice
                if isinstance(first_elem, cst.Index):
                    inner = first_elem.value
                    if isinstance(inner, cst.Subscript) and is_literal_node(
                        inner.value
                    ):
                        if inner.slice and isinstance(
                            inner.slice[0], cst.SubscriptElement
                        ):
                            index = inner.slice[0].slice
                            if isinstance(index, cst.Index):
                                expr = index.value
                                if isinstance(expr, cst.SimpleString):
                                    try:
                                        literal_value = ast.literal_eval(expr.value)
                                        return literal_value
                                    except Exception as e:
                                        print(
                                            f"Error evaluating inner literal: {e}",
                                        )
                                        return None
    return None


def flatten_union(union_node: cst.Subscript) -> cst.Subscript:
    """
    Given a Subscript node representing a Union (e.g. Union[...]),
    recursively flatten any nested Unions and return a new Subscript node.
    """
    # Confirm that this node represents a Union.
    if not (
        (isinstance(union_node.value, cst.Name) and union_node.value.value == "Union")
        or (
            isinstance(union_node.value, cst.Attribute)
            and union_node.value.attr.value == "Union"
        )
    ):
        return union_node

    new_elements = []
    for elem in union_node.slice:
        if isinstance(elem.slice, cst.Index):
            value = elem.slice.value
            # If the value itself is a Union, flatten it.
            if isinstance(value, cst.Subscript) and (
                (isinstance(value.value, cst.Name) and value.value.value == "Union")
                or (
                    isinstance(value.value, cst.Attribute)
                    and value.value.attr.value == "Union"
                )
            ):
                flattened_inner = flatten_union(value)
                for inner_elem in flattened_inner.slice:
                    new_elements.append(inner_elem)
            else:
                new_elements.append(elem)
        else:
            new_elements.append(elem)
    return union_node.with_changes(slice=new_elements)


class UnionMemberCollector(cst.CSTVisitor):
    def __init__(self, target_alias: str) -> None:
        self.target_alias = target_alias
        self.union_members: Set[str] = set()

    def visit_Assign(self, node: cst.Assign) -> None:
        # Process assignments similar to your leave_Assign,
        # but just record the union members without modifying nodes.
        if not (
            len(node.targets) == 1 and isinstance(node.targets[0].target, cst.Name)
        ):
            return
        target_name = node.targets[0].target.value
        if target_name != self.target_alias:
            return
        if isinstance(node.value, cst.Subscript):
            base = node.value.value
            if (isinstance(base, cst.Name) and base.value == "Annotated") or (
                isinstance(base, cst.Attribute) and base.attr.value == "Annotated"
            ):
                if node.value.slice:
                    first_elem = node.value.slice[0].slice
                    if isinstance(first_elem, cst.Index):
                        type_expr = first_elem.value
                        if isinstance(type_expr, cst.Subscript) and (
                            (
                                isinstance(type_expr.value, cst.Name)
                                and type_expr.value.value == "Union"
                            )
                            or (
                                isinstance(type_expr.value, cst.Attribute)
                                and type_expr.value.attr.value == "Union"
                            )
                        ):
                            flattened = flatten_union(type_expr)
                            for elem in flattened.slice:
                                if isinstance(elem.slice, cst.Index):
                                    constituent = elem.slice.value
                                    if isinstance(constituent, cst.Name):
                                        self.union_members.add(constituent.value)


class TagTransformer(cst.CSTTransformer):
    """
    A CST transformer that:
      1. Searches for a type alias assignment whose target name equals the file's base name.
         If found and if its value is an Annotated[...] whose first argument is a (possibly nested) Union,
         it flattens that union and records the names of its constituent types.
      2. Later, for each class definition, if the class name is in the recorded union members,
         it scans the class for the first annotated field with a literal and appends keyword arguments
         (tag_field and tag) to the class definition.
    """

    def __init__(self, target_alias: str, union_members: Set[str]) -> None:
        self.target_alias = target_alias
        self.union_members = union_members

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        """
        If the class name is in the recorded union members, then scan the class for all annotated fields
        whose annotation is a Literal (or Annotated[...] with a Literal). If exactly one such field exists,
        add tag configuration and remove the field declaration from the class body.
        """
        if original_node.name.value in self.union_members:
            literal_fields = []
            # Annotated assignments are often wrapped in SimpleStatementLine nodes.
            for stmt in original_node.body.body:
                if isinstance(stmt, cst.SimpleStatementLine):
                    for small_stmt in stmt.body:
                        if isinstance(small_stmt, cst.AnnAssign) and isinstance(
                            small_stmt.target, cst.Name
                        ):
                            field_name = small_stmt.target.value
                            literal = extract_literal_value(small_stmt.annotation)
                            if literal is not None:
                                literal_fields.append((field_name, literal))
            # Only tag the class if exactly one literal field is found.
            if len(literal_fields) == 1:
                tag_field, tag_value = literal_fields[0]
                new_keywords = list(updated_node.keywords) + [
                    cst.Arg(
                        keyword=cst.Name("tag_field"),
                        value=cst.SimpleString(f'"{tag_field}"'),
                    ),
                    cst.Arg(
                        keyword=cst.Name("tag"),
                        value=cst.SimpleString(f'"{tag_value}"'),
                    ),
                ]
                print(
                    f"Adding tag_field='{tag_field}' and tag='{tag_value}' to class {original_node.name.value}",
                    file=sys.stderr,
                )
                updated_node = updated_node.with_changes(keywords=new_keywords)

                # Remove the tagged field from the class body.
                new_body = []
                for stmt in updated_node.body.body:
                    if isinstance(stmt, cst.SimpleStatementLine):
                        new_small_stmts = []
                        for small_stmt in stmt.body:
                            if (
                                isinstance(small_stmt, cst.AnnAssign)
                                and isinstance(small_stmt.target, cst.Name)
                                and small_stmt.target.value == tag_field
                            ):
                                # Skip this assignment (i.e. remove the tag field).
                                continue
                            new_small_stmts.append(small_stmt)
                        if new_small_stmts:
                            new_stmt = stmt.with_changes(body=new_small_stmts)
                            new_body.append(new_stmt)
                        # If no small statements remain in the line, skip adding it.
                    else:
                        new_body.append(stmt)
                # Update the class body.
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=tuple(new_body))
                )
            elif len(literal_fields) > 1:
                print(
                    f"Class {original_node.name.value} has multiple literal fields, skipping tagging: {literal_fields}",
                )
        return updated_node


def generate_type_tags(input_file: str) -> None:
    with open(input_file, "r", encoding="utf-8") as f:
        source = f.read()

    module = cst.parse_module(source)
    target_alias = os.path.splitext(os.path.basename(input_file))[0]

    # First pass: collect union members.
    collector = UnionMemberCollector(target_alias)
    module.visit(collector)

    # Second pass: use a transformer that relies on collector.union_members.
    transformer = TagTransformer(target_alias, union_members=collector.union_members)
    modified_module = module.visit(transformer)

    try:
        new_source = modified_module.code
    except Exception as e:
        sys.exit(f"Error generating modified source: {e}")

    try:
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(new_source)
    except Exception as e:
        sys.exit(f"Error writing output file: {e}")


def generate_stub(file_path: str, json_folder: str) -> None:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)

    if "Request" not in name:
        return

    json_fp = os.path.join(json_folder, f"{name}.json")
    with open(json_fp, "r", encoding="utf-8") as json_file:
        j = json.load(json_file)

        service = j["service"]
        unary_type = j["unary_type"]
        response_file_root_name: str = j["response_type"]  # no extension
        route = j["route"]

        request_type_name = "".join(
            capitalize_first_letter(word) for word in name.split("_")
        )
        response_type_name = "".join(
            capitalize_first_letter(word) for word in response_file_root_name.split("_")
        )

        with open(file_path, "r") as f:
            lines = f.readlines()

        request_str = f"""
ResponseType = {response_type_name}
route = "{route}"
unary_type = "{unary_type}"
"""

        lines.insert(
            4,
            f"from architect_py.grpc_client.{service}.{response_file_root_name} import {response_type_name}\n",
        )
        lines.append(f"\n{request_str}\n")

        with open(file_path, "w") as f:
            f.writelines(lines)


def fix_lines(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(line.strip() == "def timestamp(self) -> int:" for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    if any("definitions.dir" in line for line in lines):
        lines.insert(4, "from architect_py.scalars import OrderDir\n")

    lines = list(map(lambda l: l.replace("Dir", "OrderDir"), lines))
    lines = list(map(lambda l: l.replace("definitions.OrderDir", "OrderDir"), lines))

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main(file_path: str, json_folder: str) -> None:
    fix_lines(file_path)
    if "definitions.py" not in file_path:
        generate_stub(file_path, json_folder)
        generate_type_tags(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder of types")
    parser.add_argument(
        "--file_path",
        type=str,
        nargs="?",
        default="architect_py/grpc_client",
        help="Path to the JSON file with the gRPC service definitions",
    )
    parser.add_argument(
        "--json_folder",
        type=str,
        help="Path to the processed_schema folder output by preprocess_grpc_types.py.",
    )

    args = parser.parse_args()
    main(args.file_path, args.json_folder)
