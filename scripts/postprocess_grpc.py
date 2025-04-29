#!/usr/bin/env python3
"""
This script processes Python gRPC types definition files along with corresponding JSON files.
It is run after auto-generation of the Python files from JSON schema files.
It further processes the Python files to add metadata to variant types, fix enum member names,
update variant type aliases, adjust imports, and generate stubs.
"""

import argparse
import importlib
import json
import multiprocessing
import os
import re
from collections import defaultdict
from typing import Annotated, List, Tuple, Union, get_args, get_origin

# --------------------------------------------------------------------
# Regular Expressions (Constants)
# --------------------------------------------------------------------

REMOVE_ORDERDIR_RE = re.compile(
    r"^class\s+OrderDir\b.*?(?=^class\s+\w|\Z)", re.DOTALL | re.MULTILINE
)
IMPORT_FIX_RE = re.compile(r"^from\s+(\.+)(\w*)\s+import\s+(.+)$")
CLASS_HEADER_RE = re.compile(r"^(\s*)class\s+(\w+)\([^)]*Enum[^)]*\)\s*:")
MEMBER_RE = re.compile(r"^(\s*)(\w+)\s*=\s*([0-9]+)(.*)")

ALIAS_PATTERN_UNION = re.compile(
    r"^(?P<alias>\w+)\s*=\s*Annotated\[\s*(?P<union>Union\[(?P<union_content>.*?)\])\s*,\s*Meta\((?P<meta>.*?)\)\s*,?\s*\]",
    re.DOTALL | re.MULTILINE,
)
ALIAS_PATTERN_SINGLE = re.compile(
    r"^(?P<alias>\w+)\s*=\s*Annotated\[\s*(?P<single_type>\w+(?:\.\w+)*)\s*,\s*Meta\((?P<meta>.*?)\)\s*,?\s*\]",
    re.DOTALL | re.MULTILINE,
)

# --------------------------------------------------------------------
# Utility Functions
# --------------------------------------------------------------------


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def get_py_file_json_pairs(py_folder: str, json_folder: str) -> List[Tuple[str, dict]]:
    """
    Traverse json_folder recursively and yield pairs (py_file, json_data)
    where py_file is the corresponding Python file in py_folder and json_data is
    the JSON content loaded from the JSON file in json_folder.
    """
    pairs = []
    for root, dirs, files in os.walk(json_folder):
        for file in files:
            json_file_path = os.path.join(root, file)
            rel_path = os.path.relpath(json_file_path, json_folder)
            py_rel_path = f"{os.path.splitext(rel_path)[0]}.py"
            py_file = os.path.join(py_folder, py_rel_path)

            with open(json_file_path, "r", encoding="utf-8") as f:
                json_data: dict = json.load(f)

            # print(f"{json_file_path}: {py_file}")
            pairs.append((py_file, json_data))
    return pairs


def add_to_typing_import(file_str: str, type_to_add: str) -> str:
    """
    Ensures that `type_to_add` is imported from typing.
    If an import line exists, it adds the type if missing;
    otherwise, it prepends a new import statement.
    """
    typing_import_re = re.compile(
        r"^(?P<indent>\s*)from\s+typing\s+import\s+(?P<imports>.+)$", re.MULTILINE
    )
    found = False

    def replace_func(match):
        nonlocal found
        found = True
        indent = match.group("indent")
        imports = match.group("imports")
        items = [item.strip() for item in imports.split(",")]
        if type_to_add not in items:
            items.append(type_to_add)
            return f"{indent}from typing import {', '.join(items)}"
        return match.group(0)

    new_file_str = typing_import_re.sub(replace_func, file_str)

    if not found:
        new_file_str = f"from typing import {type_to_add}\n" + new_file_str

    return new_file_str


def split_top_level(s: str, delimiter: str = ",") -> List[str]:
    """
    Splits string `s` at top-level (non-nested) occurrences of `delimiter`.
    Avoids splitting inside nested brackets.
    """
    parts = []
    current = []
    level = 0
    for char in s:
        if char in "[(":
            level += 1
        elif char in "])":
            level -= 1
        if char == delimiter and level == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [part for part in parts if part]


def get_unannotated_type(t: type) -> type:
    origin = get_origin(t)
    if origin is Annotated:
        t = get_args(t)[0]

    origin = get_origin(t)
    args = get_args(t)
    if origin is not None and args:
        # Rebuild the generic using the built-in generic type.
        return origin[args]

    return t


def get_type_str(t: type) -> str:
    origin = get_origin(t)
    if origin is Annotated:
        t = get_unannotated_type(t)
        origin = get_origin(t)

    if origin is Union:
        return " | ".join(get_type_str(arg) for arg in get_args(t))

    if origin is not None:
        args = get_args(t)
        if args:
            arg_str = ", ".join(get_type_str(arg) for arg in args)
            return f"{origin.__name__}[{arg_str}]"
        else:
            # If no arguments are found, just return the name of the origin
            return origin.__name__

    return t.__name__


def built_in_type(t: type) -> bool:
    return getattr(t, "__module__", None) == "builtins"


def get_import_str(t: type) -> str:
    origin = get_origin(t)
    if origin is Annotated:
        t = get_unannotated_type(t)
        origin = get_origin(t)

    if origin is Union:
        args = get_args(t)
        args = [arg for arg in args if not built_in_type(arg)]
        return ",  ".join(get_import_str(arg) for arg in args)

    if origin is not None:
        args = get_args(t)
        args = [arg for arg in args if not built_in_type(arg)]
        if args:
            return ", ".join(get_import_str(arg) for arg in args)
        else:
            # If no arguments are found, just return the name of the origin
            return origin.__name__

    name = t.__name__
    if "." in name:
        return name.split(".")[-1]
    else:
        return name


# --------------------------------------------------------------------
# Core Processing Functions (Refactored to work with content strings)
# --------------------------------------------------------------------


def create_tagged_subtypes_for_variant_types(content: str, json_data: dict) -> str:
    """
    Processes the file content for variant types with a tag.
    Creates or updates subtype classes with tag metadata and rebuilds
    the type alias so that the Union is replaced by the variant classes.
    """

    tag_field = json_data.get("tag_field")
    if tag_field is None:
        return content

    # Build a mapping from base type name to its variants.
    tag_field_map: dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for p in json_data["oneOf"]:
        tag_field_map[p["title"]].append((p["variant_name"], p["tag_value"]))

    # Match the type alias (Union or single type)
    alias_match = ALIAS_PATTERN_UNION.search(content)
    if alias_match:
        union_content = alias_match.group("union_content")
        meta = alias_match.group("meta")
        types = split_top_level(union_content)
    else:
        alias_match = ALIAS_PATTERN_SINGLE.search(content)
        if not alias_match:
            print(f"No type alias found in the file {json_data['title']}.")
            return content
        types = [alias_match.group("single_type")]
        meta = alias_match.group("meta")
        content = add_to_typing_import(content, "Union")

    new_union_types = []
    additional_class_defs = ""

    for base_type in types:
        # Leave dictionary types unchanged.
        if base_type.startswith("dict") or base_type.startswith("Dict"):
            new_union_types.append(base_type)
            continue

        simple_name = base_type.split(".")[-1]
        if simple_name in tag_field_map:
            for variant_name, tag_value in tag_field_map[simple_name]:
                pattern = re.compile(
                    rf"^(class\s+{variant_name}\s*\()(?P<inheritance>[^)]*)(\))(\s*:)",
                    re.MULTILINE,
                )

                def repl(m):
                    if "tag=" in m.group("inheritance"):
                        return m.group(0)
                    return (
                        f"{m.group(1)}{m.group('inheritance')}, omit_defaults=True, "
                        f'tag_field="{tag_field}", tag="{tag_value}"{m.group(3)}{m.group(4)}'
                    )

                content, count = pattern.subn(repl, content)
                if count == 0:
                    new_class_def = (
                        f"\n\nclass {variant_name}({base_type}, omit_defaults=True, "
                        f'tag_field="{tag_field}", tag="{tag_value}"):\n'
                        "    pass\n"
                    )
                    additional_class_defs += new_class_def
                new_union_types.append(variant_name)
        else:
            new_union_types.append(base_type)

    # Rebuild the union type alias.
    if ALIAS_PATTERN_UNION.search(content):
        final_union = [t for t in types if t.split(".")[-1] not in tag_field_map]
        final_union += new_union_types
        seen = set()
        final_union_ordered = [t for t in final_union if not (t in seen or seen.add(t))]
        new_union_str = "Union[" + ", ".join(final_union_ordered) + "]"
    else:
        new_union_str = "Union[" + ", ".join(new_union_types) + "]"

    # Reassemble the alias definition.
    alias_match = ALIAS_PATTERN_UNION.search(content) or ALIAS_PATTERN_SINGLE.search(
        content
    )
    if not alias_match:
        print(
            f"No type alias found for {json_data['title']} when reinserting subclass definitions."
        )
        return content

    alias_name = alias_match.group("alias")
    new_alias_text = f"{alias_name} = Annotated[{new_union_str}, Meta({meta})]"

    alias_start_index = alias_match.start()
    content = (
        content[:alias_start_index]
        + additional_class_defs
        + "\n\n"
        + new_alias_text
        + content[alias_match.end() :]
    )
    return content


def fix_lines(content: str) -> str:
    """
    Fixes type annotations and adds necessary imports.
    """
    lines = content.splitlines(keepends=True)

    if any("def timestamp(self) -> int:" in line for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    lines = [line.replace("Dir", "OrderDir") for line in lines]
    lines = [line.replace("definitions.OrderDir", "OrderDir") for line in lines]
    lines = [line.replace("(Struct)", "(Struct, omit_defaults=True)") for line in lines]

    if any("OrderDir" in line for line in lines):
        lines.insert(4, "from architect_py.common_types import OrderDir\n")

    content = "".join(lines)
    content = REMOVE_ORDERDIR_RE.sub("", content)
    return content


def add_post_processing_to_loosened_types(content: str, json_data: dict) -> str:
    """
    Adds a __post_init__ method to the flattened types to enforce field requirements.
    """
    enum_tag = json_data.get("enum_tag")
    if enum_tag is None:
        return content

    class_title = json_data["title"]

    properties = json_data["properties"]
    enum_tag_to_other_required_keys: dict[str, List[str]] = json_data[
        "enum_tag_to_other_required_keys"
    ]

    lines = content.splitlines(keepends=True)
    # Append __post_init__ method at the end
    lines.append("\n    def __post_init__(self):\n")

    common_keys = set.intersection(*map(set, enum_tag_to_other_required_keys.values()))
    union_keys = set.union(*map(set, enum_tag_to_other_required_keys.values()))

    for i, (enum_value, required_keys) in enumerate(
        enum_tag_to_other_required_keys.items()
    ):
        conditional = "if" if i == 0 else "elif"
        title = properties[enum_tag]["title"]
        req_keys_subset = [key for key in required_keys if key not in common_keys]
        should_be_empty_keys = list(union_keys - set(required_keys))
        lines.append(
            f'        {conditional} self.{enum_tag} == "{enum_value}":\n'
            f"            if not all(getattr(self, key) is not None for key in {req_keys_subset}):\n"
            f'                raise ValueError(f"When field {enum_tag} ({title}) is of value {enum_value}, '
            f'class {class_title} requires fields {req_keys_subset}")\n'
            f"            elif any(getattr(self, key) is not None for key in {should_be_empty_keys}):\n"
            f'                raise ValueError(f"When field {enum_tag} ({title}) is of value {enum_value}, '
            f'class {class_title} should not have fields {should_be_empty_keys}")\n'
        )

    return "".join(lines)


def generate_stub(content: str, json_data: dict) -> str:
    """
    Generates stub code for Request files linking Request type to Response type, service, and route.
    """
    request_type_name: str | None = json_data.get("title")
    if request_type_name is None or "Request" not in request_type_name:
        return content

    service = json_data["service"]
    rpc_method = json_data["rpc_method"]
    response_type_name = json_data["response_type"]
    route = json_data["route"]

    try:
        response_type_module = importlib.import_module(
            f"architect_py.grpc.models.{service}.{response_type_name}"
        )
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"{e}\n"
            f"Module {response_type_name} not found in architect_py.grpc.models.{service}. "
        )
    except ImportError as e:
        raise ImportError(
            f"{e}\n"
            f"Module {response_type_name} could not be imported from architect_py.grpc.models.{service}. "
        )
    ResponseType = getattr(response_type_module, response_type_name)
    UnAnnotatedResponseType = get_unannotated_type(ResponseType)
    unannotated_response_type_str = get_type_str(UnAnnotatedResponseType)
    union_type_import_str = get_import_str(UnAnnotatedResponseType)

    request_type_module = importlib.import_module(
        f"architect_py.grpc.models.{service}.{request_type_name}"
    )
    RequestType = getattr(request_type_module, request_type_name)
    UnAnnotatedRequestType = get_unannotated_type(RequestType)
    unannotated_request_type_str = get_type_str(UnAnnotatedRequestType)

    if get_origin(UnAnnotatedResponseType) is Union:
        response_import_str = f"from architect_py.grpc.models.{service}.{response_type_name} import {response_type_name}, {union_type_import_str}\n"
    elif get_origin(UnAnnotatedResponseType) is not None:
        response_import_str = f"from architect_py.grpc.models.{service}.{response_type_name} import {response_type_name}, {union_type_import_str}\n"
    else:
        response_import_str = f"from architect_py.grpc.models.{service}.{response_type_name} import {response_type_name}\n"

    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('    "SENTINAL_VALUE"'):
            lines[i] = f"""
    @staticmethod
    def get_response_type():
        return {response_type_name}

    @staticmethod
    def get_unannotated_response_type():
        return {unannotated_response_type_str}

    @staticmethod
    def get_route() -> str:
        return "{route}"
    
    @staticmethod
    def get_rpc_method():
        return "{rpc_method}"
"""

    # If this is a Request file, append additional gRPC info.
    if json_data.get("tag_field") is not None:
        service = json_data["service"]
        rpc_method = json_data["rpc_method"]
        response_type = json_data["response_type"]
        route = json_data["route"]

        lines.append(f'\n\n{request_type_name}_rpc_method = "{rpc_method}"\n')
        lines.append(
            f"Unannotated{request_type_name} = {unannotated_request_type_str}\n"
        )
        lines.append(f"{request_type_name}ResponseType = {response_type}\n")
        lines.append(
            f"{request_type_name}UnannotatedResponseType = {unannotated_response_type_str}\n"
        )
        lines.append(f'{request_type_name}_route = "{route}"\n')

    lines.insert(4, response_import_str)
    return "".join(lines)


def fix_enum_member_names(content: str, json_data: dict) -> str:
    """
    Fixes enum member names based on JSON definitions.
    For each enum class (classes that inherit from Enum),
    it replaces the member names with the names defined in the JSON file under "x-enumNames".
    """

    lines = content.splitlines()
    # Fix import statements from grpc classes.
    for i, line in enumerate(lines):
        if line.strip() != "from .. import definitions":
            m = IMPORT_FIX_RE.match(line)
            if m:
                dots, module, imports = m.groups()
                names = [name.strip() for name in imports.split(",")]
                if module:
                    lines[i] = "\n".join(
                        f"from {dots}{module}.{name} import {name}" for name in names
                    )
                else:
                    lines[i] = "\n".join(
                        f"from {dots}{name} import {name}" for name in names
                    )

    new_lines = []
    in_enum_class = False
    enum_class_indent = ""
    enum_values = []
    enum_names = []

    for line in lines:
        stripped_line = line.rstrip("\n")
        class_match = CLASS_HEADER_RE.match(stripped_line)
        if class_match:
            indent, class_name = class_match.groups()
            if class_name in json_data:
                in_enum_class = True
                enum_class_indent = indent
                enum_values = json_data[class_name].get("enum", [])
                enum_names = json_data[class_name].get("x-enumNames", [])
            else:
                in_enum_class = False
            new_lines.append(stripped_line)
            continue

        if in_enum_class:
            member_match = MEMBER_RE.match(stripped_line)
            if member_match:
                member_indent, _, member_value, rest = member_match.groups()
                if len(member_indent) <= len(enum_class_indent):
                    in_enum_class = False
                    new_lines.append(stripped_line)
                    continue
                try:
                    value_int = int(member_value)
                except ValueError:
                    new_lines.append(stripped_line)
                    continue
                if value_int in enum_values:
                    index = enum_values.index(value_int)
                    new_line = (
                        f"{member_indent}{enum_names[index]} = {member_value}{rest}"
                    )
                    new_lines.append(new_line)
                else:
                    new_lines.append(stripped_line)
            else:
                if stripped_line.strip() and not stripped_line.startswith(
                    " " * (len(enum_class_indent) + 1)
                ):
                    in_enum_class = False
                new_lines.append(stripped_line)
        else:
            new_lines.append(stripped_line)

    return "\n".join(new_lines)


# --------------------------------------------------------------------
# Main Entry Point (Processing Pipeline)
# --------------------------------------------------------------------


def main(py_file_path: str, json_folder: str) -> None:
    num_cores = max(multiprocessing.cpu_count() - 1, 1)

    py_fp_json_pairs: list[tuple[str, dict]] = get_py_file_json_pairs(
        py_file_path, json_folder
    )

    print("[1/2] Post-processing...")
    with multiprocessing.Pool(processes=num_cores) as pool:
        _ = pool.starmap(part_1, py_fp_json_pairs)

    print("[2/2] Post-processing...")
    for py_fp, json_data in py_fp_json_pairs:
        part_2(py_fp, json_data)

    print("Post-processing complete.")


def part_1(py_file_path: str, json_data: dict) -> None:
    content = read_file(py_file_path)

    content = create_tagged_subtypes_for_variant_types(content, json_data)
    content = fix_lines(content)
    if not py_file_path.endswith("definitions.py"):
        content = add_post_processing_to_loosened_types(content, json_data)

    content = fix_enum_member_names(content, json_data)

    write_file(py_file_path, content)


def part_2(py_file_path: str, json_data: dict) -> None:
    content = read_file(py_file_path)
    if not py_file_path.endswith("definitions.py"):
        """
        we write and then read the same file because we need to update the content for when we do the import for the variant types
        """
        content = generate_stub(content, json_data)
    else:
        content = content.replace('    "SENTINAL_VALUE"', "")

    write_file(py_file_path, content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process gRPC service definitions")
    parser.add_argument(
        "--file_path",
        type=str,
        default="architect_py/grpc_client",
        help="Path to the Python folder with the gRPC service definitions",
    )
    parser.add_argument(
        "--json_folder",
        type=str,
        required=True,
        help="Path to the processed_schema folder output by preprocess_grpc_types.py",
    )
    args = parser.parse_args()
    main(args.file_path, args.json_folder)
