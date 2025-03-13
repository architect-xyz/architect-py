#!/usr/bin/env python3
"""
This script processes Python gRPC types definition files along with corresponding JSON files.
This script is run after the auto-generation of the Python files from the JSON schema files.
It further processes the Python files to add metadata to variant types, fix enum member names,

It updates variant type aliases, fixes enum member names, adjusts imports, and generates stubs.
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

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


def read_lines(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_lines(file_path: str, lines: List[str]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def get_corresponding_json_file(file_path: str, json_folder: str) -> str:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return os.path.join(json_folder, f"{name}.json")


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


# --------------------------------------------------------------------
# Core Processing Functions
# --------------------------------------------------------------------


def create_tagged_subtypes_for_variant_types(file_path: str, json_folder: str) -> None:
    """
    Processes the Python file for variant types with a tag.
    Creates or updates subtype classes with tag metadata and rebuilds
    the type alias so that the Union is replaced by the variant classes.
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    tag_field = json_data.get("tag_field")
    if tag_field is None:
        return

    # Build a mapping from base type name to its variants.
    tag_field_map: dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for p in json_data["oneOf"]:
        tag_field_map[p["title"]].append((p["variant_name"], p["tag_value"]))

    content = read_file(file_path)

    # If this is a Request file, append additional gRPC info.
    if "Request" in file_path:
        service = json_data["service"]
        unary_type = json_data["unary_type"]
        response_type = json_data["response_type"]
        route = json_data["route"]
        content += f'\n\nunary = "{unary_type}"\n'
        content += f"response_type = {response_type}\n"
        content += f'route = "{route}"\n'

        lines = content.split("\n")
        lines.insert(
            4,
            f"from architect_py.grpc_client.{service}.{response_type} import {response_type}",
        )
        content = "\n".join(lines)

    # Match the type alias (Union or single type)
    alias_match = ALIAS_PATTERN_UNION.search(content)
    if alias_match:
        union_content = alias_match.group("union_content")
        meta = alias_match.group("meta")
        types = split_top_level(union_content)
    else:
        alias_match = ALIAS_PATTERN_SINGLE.search(content)
        if not alias_match:
            print(f"No type alias found in the file {file_path}.")
            return
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
                        f'{m.group(1)}{m.group("inheritance")}, omit_defaults=True, '
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
            f"No type alias found in the file {file_path} when reinserting subclass definitions."
        )
        return

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

    write_file(file_path, content)


def add_post_processing_to_loosened_types(file_path: str, json_folder: str) -> None:
    """
    Adds a __post_init__ method to the flattened types to enforce field requirements.
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    class_title = json_data["title"]
    enum_tag = json_data.get("enum_tag")
    if enum_tag is None:
        return

    properties = json_data["properties"]
    enum_tag_to_other_required_keys: dict[str, List[str]] = json_data[
        "enum_tag_to_other_required_keys"
    ]

    lines = read_lines(file_path)
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

    write_file(file_path, "".join(lines))


def fix_enum_member_names(file_path: str, json_folder: str) -> None:
    """
    Fixes enum member names based on JSON definitions.

        For each enum class in the Python file (i.e. classes that inherit from Enum),
    it replaces the member names with the names defined in the JSON file under "x-enumNames".
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as jf:
        json_data = json.load(jf)

    lines = read_lines(file_path)
    # Fix import statements from grpc classes.
    for i, line in enumerate(lines):
        if line.strip() != "from .. import definitions":
            m = IMPORT_FIX_RE.match(line)
            if m:
                dots, module, imports = m.groups()
                names = [name.strip() for name in imports.split(",")]
                if module:
                    lines[i] = (
                        "\n".join(
                            f"from {dots}{module}.{name} import {name}"
                            for name in names
                        )
                        + "\n"
                    )
                else:
                    lines[i] = (
                        "\n".join(f"from {dots}{name} import {name}" for name in names)
                        + "\n"
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

    write_file(file_path, "\n".join(new_lines))


def generate_stub(file_path: str, json_folder: str) -> None:
    """
    Generates stub code for Request files linking Request type to Response type, service, and route.
    """
    if "Request" not in file_path:
        return

    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    service = json_data["service"]
    unary_type = json_data["unary_type"]
    response_type = json_data["response_type"]
    route = json_data["route"]
    request_type_name = json_data["title"]

    lines = read_lines(file_path)
    for i, line in enumerate(lines):
        if line == f'        return "&RESPONSE_TYPE:{request_type_name}"\n':
            lines[i] = f"        return {response_type}\n"
        elif line == f'        return "&ROUTE:{request_type_name}"\n':
            lines[i] = f'        return "{route}"\n'
        elif line == f'        return "&UNARY_TYPE:{request_type_name}"\n':
            lines[i] = f'        return "{unary_type}"\n'

    lines.insert(
        4,
        f"from architect_py.grpc_client.{service}.{response_type} import {response_type}\n",
    )
    write_lines(file_path, lines)


def fix_lines(file_path: str) -> None:
    """
    Fixes type annotations and adds necessary imports.
    """
    lines = read_lines(file_path)

    if any("def timestamp(self) -> int:" in line for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    lines = [line.replace("Dir", "OrderDir") for line in lines]
    lines = [line.replace("definitions.OrderDir", "OrderDir") for line in lines]
    lines = [line.replace("(Struct)", "(Struct, omit_defaults=True)") for line in lines]

    if any("OrderDir" in line for line in lines):
        lines.insert(4, "from architect_py.scalars import OrderDir\n")

    content = "".join(lines)
    content = REMOVE_ORDERDIR_RE.sub("", content)
    write_file(file_path, content)


# --------------------------------------------------------------------
# Main Entry Point
# --------------------------------------------------------------------


def main(file_path: str, json_folder: str) -> None:
    create_tagged_subtypes_for_variant_types(file_path, json_folder)
    fix_lines(file_path)
    if not file_path.endswith("definitions.py"):
        add_post_processing_to_loosened_types(file_path, json_folder)
        generate_stub(file_path, json_folder)
    fix_enum_member_names(file_path, json_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process gRPC service definitions")
    parser.add_argument(
        "--file_path",
        type=str,
        default="architect_py/grpc_client",
        help="Path to the Python file with the gRPC service definitions",
    )
    parser.add_argument(
        "--json_folder",
        type=str,
        required=True,
        help="Path to the processed_schema folder output by preprocess_grpc_types.py",
    )
    args = parser.parse_args()
    main(args.file_path, args.json_folder)
