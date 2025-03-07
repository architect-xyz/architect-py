import argparse
import ast
from typing import Optional, Union
import libcst as cst
import os
import json
import os
import sys


def main(file_path: str, json_folder: str) -> None:
    fix_lines(file_path)
    if "definitions.py" not in file_path:
        generate_stub(file_path, json_folder)
        generate_type_tags(file_path)


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:]


def generate_type_tags(input_file: str) -> None:
    with open(input_file, "r", encoding="utf-8") as f:
        source = f.read()

    module = cst.parse_module(source)

    target_class = os.path.splitext(os.path.basename(input_file))[0]
    transformer = TagTransformer(target_class)
    modified_module = module.visit(transformer)

    try:
        # Generate the modified source code while preserving formatting and comments.
        new_source = modified_module.code
    except Exception as e:
        sys.exit(f"Error generating modified source: {e}")

    try:
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(new_source)
    except Exception as e:
        sys.exit(f"Error writing output file: {e}")


def extract_literal_value(
    annotation: Union[cst.BaseExpression, cst.Annotation],
) -> Optional[str]:
    """
    Attempt to extract the literal value from an annotation if it represents
    either a Literal (e.g. Literal['VALUE']) or an Annotated wrapping a Literal.

    Args:
        annotation: A libcst expression representing a type annotation.
                    If this is an Annotation node, it will be unwrapped.

    Returns:
        The literal value as a string if found, otherwise None.
    """
    if isinstance(annotation, cst.Annotation):
        annotation = annotation.annotation

    # Check for a direct Literal[...] case.
    if isinstance(annotation, cst.Subscript):
        if (
            isinstance(annotation.value, cst.Name)
            and annotation.value.value == "Literal"
        ):
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
        # Check for an Annotated[...] wrapping a Literal[...] case.
        if (
            isinstance(annotation.value, cst.Name)
            and annotation.value.value == "Annotated"
        ):
            if annotation.slice:
                first_elem = annotation.slice[0].slice
                if isinstance(first_elem, cst.Index):
                    inner = first_elem.value
                    if (
                        isinstance(inner, cst.Subscript)
                        and isinstance(inner.value, cst.Name)
                        and inner.value.value == "Literal"
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
                                            file=sys.stderr,
                                        )
                                        return None
    return None


def flatten_union(union_node: cst.Subscript) -> cst.BaseExpression:
    """
    Given a Subscript node representing a Union (e.g. Union[...]),
    recursively flatten any nested Unions and return a new node.
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
        # Each elem is a SubscriptElement; its slice should be an Index.
        if isinstance(elem.slice, cst.Index):
            value = elem.slice.value
            # If the value is itself a Union, flatten it.
            if isinstance(value, cst.Subscript) and (
                (isinstance(value.value, cst.Name) and value.value.value == "Union")
                or (
                    isinstance(value.value, cst.Attribute)
                    and value.value.attr.value == "Union"
                )
            ):
                flattened_inner = flatten_union(value)
                # flattened_inner.slice is a sequence of SubscriptElements.
                if isinstance(flattened_inner, cst.Subscript):
                    for inner_elem in flattened_inner.slice:
                        new_elements.append(inner_elem)
            else:
                new_elements.append(elem)
        else:
            new_elements.append(elem)
    return union_node.with_changes(slice=new_elements)


class TagTransformer(cst.CSTTransformer):
    """
    A CST transformer that finds the class with a name matching the target (derived from the file name)
    and appends keyword arguments (tag_field and tag) to the class definition.
    """

    def __init__(self, target_class: str) -> None:
        self.target_class = target_class

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> cst.Assign:
        """
        Process type alias assignments. If the assignment’s value is an Annotated[...] whose
        first argument is a Union (possibly nested), flatten that Union.
        """
        # Only process assignments that look like a type alias:
        #   Identifier = Annotated[..., Meta(...)]
        if not (len(updated_node.targets) == 1 and isinstance(updated_node.targets[0].target, cst.Name)):
            return updated_node

        # Check if the value is a Subscript (i.e. a call to Annotated).
        if isinstance(updated_node.value, cst.Subscript):
            base = updated_node.value.value
            if ((isinstance(base, cst.Name) and base.value == "Annotated") or
                (isinstance(base, cst.Attribute) and base.attr.value == "Annotated")):
                if updated_node.value.slice:
                    # The first element should be the type expression.
                    first_elem = updated_node.value.slice[0].slice
                    if isinstance(first_elem, cst.Index):
                        type_expr = first_elem.value
                        # Check if the type expression is a Union that might be nested.
                        if isinstance(type_expr, cst.Subscript) and (
                            (isinstance(type_expr.value, cst.Name) and type_expr.value.value == "Union") or
                            (isinstance(type_expr.value, cst.Attribute) and type_expr.value.attr.value == "Union")
                        ):
                            print("Original Union:", type_expr, file=sys.stderr)
                            flattened = flatten_union(type_expr)
                            print("Flattened Union:", flattened, file=sys.stderr)
                            new_index = cst.Index(value=flattened)
                            new_slice = list(updated_node.value.slice)
                            new_slice[0] = cst.SubscriptElement(slice=new_index)
                            new_subscript = updated_node.value.with_changes(slice=new_slice)
                            return updated_node.with_changes(value=new_subscript)
        return updated_node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        # Only process classes whose names contain "Request".
        if "Request" in original_node.name.value:
            tag_field = None
            tag_value = None

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
                                tag_field = field_name
                                tag_value = literal
                                break
                    if tag_field is not None:
                        break

            if tag_field is not None and tag_value is not None:
                # Append new keyword arguments to the class definition.
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
                updated_node = updated_node.with_changes(keywords=new_keywords)
        return updated_node


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

        # the split("_") is for files like Array_of_L1BookSnapshot.json
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
            (
                f"from architect_py.grpc_client.{service}.{response_file_root_name} import {response_type_name}\n"
                # f"{request_import}\n"
            ),
        )
        lines.append(f"\n{request_str}\n")

        with open(file_path, "w") as f:
            f.writelines(lines)


def fix_lines(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # lines = [
    #     line
    #     for line in lines
    #     if line != "Decimal1 = Decimal\n" and line != "DecimalModel = Decimal\n"
    # ]

    if any(line.strip() == "def timestamp(self) -> int:" for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


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
