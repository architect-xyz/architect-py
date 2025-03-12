import argparse
from collections import defaultdict
import re
import json

import os

# Regex for removing the OrderDir class definition from the file
remove_OrderDir_re = re.compile(
    r"^class\s+OrderDir\b.*?(?=^class\s+\w|\Z)", re.DOTALL | re.MULTILINE
)

# regex for fixing imports from other grpc classes
import_fix_re = re.compile(r"^from\s+(\.+)(\w*)\s+import\s+(.+)$")

# Regex to find enum class definitions.
class_header_re = re.compile(r"^(\s*)class\s+(\w+)\([^)]*Enum[^)]*\)\s*:")

# Regex to find member assignments. It assumes the member value is an integer literal.
member_re = re.compile(r"^(\s*)(\w+)\s*=\s*([0-9]+)(.*)")

# Regex to detect the type alias assignment using Annotated[...] with Meta(...)
alias_pattern_union = re.compile(
    r"^(?P<alias>\w+)\s*=\s*Annotated\[\s*(?P<union>Union\[(?P<union_content>.*?)\])\s*,\s*Meta\((?P<meta>.*?)\)\s*,?\s*\]",
    re.DOTALL | re.MULTILINE,
)

alias_pattern_single = re.compile(
    r"^(?P<alias>\w+)\s*=\s*Annotated\[\s*(?P<single_type>\w+(?:\.\w+)*)\s*,\s*Meta\((?P<meta>.*?)\)\s*,?\s*\]",
    re.DOTALL | re.MULTILINE,
)


def add_to_typing_import(file_str: str, type_to_add: str) -> str:
    """
    in a given file that is a string:

    For example, for Union
    "from typing import A, B, C" -> "from typing import A, B, C, Union"

    "from typing import A, Union, C"
    will have nothing added

    and if there is no "from typing import" line, it will add it at the top
    """
    # Regular expression to match lines like: from typing import ...
    typing_import_re = re.compile(
        r"^(?P<indent>\s*)from\s+typing\s+import\s+(?P<imports>.+)$", re.MULTILINE
    )
    found = False

    def replace_func(match):
        nonlocal found
        found = True
        indent = match.group("indent")
        imports = match.group("imports")
        # Split the imports on commas and strip extra whitespace
        items = [item.strip() for item in imports.split(",")]
        # If "Union" is not already imported, add it
        if type_to_add not in items:
            items.append(type_to_add)
            # Return a new import line with Union added
            return f"{indent}from typing import {', '.join(items)}"
        else:
            # Otherwise, leave the line as is
            return match.group(0)

    # Substitute all occurrences with our replacement function
    new_file_str = typing_import_re.sub(replace_func, file_str)

    # If no "from typing import" line was found, add one at the top
    if not found:
        new_file_str = "from typing import Union\n" + new_file_str

    return new_file_str


# --------------------------------------------------------------------
# Create tagged subtypes for variant types
# --------------------------------------------------------------------


def split_top_level(s: str, delimiter: str = ",") -> list[str]:
    """
    Split a string at top-level (non-nested) occurrences of delimiter.
    This avoids splitting commas inside nested brackets.
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
    # Filter out any empty parts that might result from trailing commas
    return [part for part in parts if part]


def create_tagged_subtypes_for_variant_types(file_path: str, json_folder: str) -> None:
    """
    Processes the Python file for variant types with a tag.

    It creates or updates subtype classes with tag metadata and rebuilds
    the type alias so that the Union is replaced by the variant classes.
    The alias is reassembled without a trailing comma after the Meta call.
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    tag: str | None = json_data.get("tag", None)
    if tag is None:
        return

    tag_field_map: dict[str, list[tuple[str, str]]] = defaultdict(list)
    one_of = json_data["oneOf"]
    for p in one_of:
        tag_field = p["tag_field"]
        type_name = p["title"]
        variant_name = p["variant_name"]
        tag_field_map[type_name].append((variant_name, tag_field))

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read()

    if "Request" in file_path:
        unary_type = json_data["unary_type"]
        response_type = json_data["response_type"]
        route = json_data["route"]
        service = json_data["service"]
        lines += f'\n\nunary = "{unary_type}"\n'
        lines += f"response_type = {response_type}\n"
        lines += f'route = "{route}"\n'

        temp = lines.split("\n")
        temp.insert(
            4,
            f"from architect_py.grpc_client.{service}.{response_type} import {response_type}",
        )
        lines = "\n".join(temp)

    alias_match = alias_pattern_union.search(lines)
    if alias_match:
        alias = alias_match.group("alias")
        union_expr = alias_match.group("union")
        union_content = alias_match.group("union_content")
        meta = alias_match.group("meta")
        types = split_top_level(union_content)
    else:
        # Fallback to a single-type alias.
        alias_match = alias_pattern_single.search(lines)
        if not alias_match:
            print(f"No type alias found in the file {file_path}.")
            return
        alias = alias_match.group("alias")
        single_type = alias_match.group("single_type")
        meta = alias_match.group("meta")
        types = [single_type]
        lines = add_to_typing_import(lines, "Union")

    new_union_types = []  # Collect new union member names.
    additional_class_defs = ""  # Collect new subclass definitions.

    # Process each type in the union list.
    for base_type in types:
        # If the type is a dictionary type, leave it unchanged.
        if base_type.startswith("dict") or base_type.startswith("Dict"):
            new_union_types.append(base_type)
            continue

        # Get the simple name (if qualified, e.g. definitions.Ticker -> Ticker)
        simple_name = base_type.split(".")[-1]
        if simple_name in tag_field_map:
            for variant_name, tag_field in tag_field_map[simple_name]:
                # Use an improved regex to insert the tag metadata inside the parentheses.
                pattern = re.compile(
                    rf"^(class\s+{variant_name}\s*\()(?P<inheritance>[^)]*)(\))(\s*:)",
                    re.MULTILINE,
                )

                def repl(m):
                    header_prefix = m.group(1)
                    inheritance = m.group("inheritance")
                    closing_paren = m.group(3)
                    colon = m.group(4)
                    # If already tagged, leave unchanged.
                    if "tag=" in inheritance:
                        return m.group(0)
                    return f'{header_prefix}{inheritance}, omit_defaults=True, tag="{tag}", tag_field="{tag_field}"{closing_paren}{colon}'

                # Replace class header if already present.
                lines, count = pattern.subn(repl, lines)
                # If the class wasn't found at all, create it.
                if count == 0:
                    new_class_def = (
                        f'\n\nclass {variant_name}({base_type}, tag="{tag}", tag_field="{tag_field}"):\n'
                        "    pass\n"
                    )
                    additional_class_defs += new_class_def
                new_union_types.append(variant_name)
        else:
            new_union_types.append(base_type)

    # If the original alias was a union, we need to remove the original base types that were replaced.
    if alias_pattern_union.search(lines):
        final_union = []
        for base_type in types:
            simple_name = base_type.split(".")[-1]
            if simple_name in tag_field_map:
                continue
            final_union.append(base_type)
        final_union += new_union_types
        # Remove duplicates while preserving order.
        seen = set()
        final_union_ordered = []
        for t in final_union:
            if t not in seen:
                seen.add(t)
                final_union_ordered.append(t)
        new_union_str = "Union[" + ", ".join(final_union_ordered) + "]"
    else:
        # If it was a single type but now we have variants, build a union out of them.
        new_union_str = "Union[" + ", ".join(new_union_types) + "]"

    # Re-search for the alias (either union or single-type).
    alias_match = alias_pattern_union.search(lines) or alias_pattern_single.search(
        lines
    )
    if not alias_match:
        print(
            f"No type alias found in the file {file_path} when reinserting subclass definitions."
        )
        return

    # Build the new union string (for a single-type alias, new_union_str is the union of variant names).
    # For example, new_union_str might be "Union[Snapshot, Diff]"

    # Reassemble the alias definition, preserving the original alias name and meta block.
    alias_name = alias_match.group("alias")
    meta_content = alias_match.group("meta")
    new_alias_text = f"{alias_name} = Annotated[{new_union_str}, Meta({meta_content})]"

    # Insert the new subclass definitions before the alias definition.
    alias_start_index = alias_match.start()
    lines = (
        lines[:alias_start_index]
        + additional_class_defs
        + "\n\n"
        + new_alias_text
        + lines[alias_match.end() :]
    )

    # Write the updated content back.
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(lines)


# --------------------------------------------------------------------
# Add post processing to loosened types
# --------------------------------------------------------------------


def add_post_processing_to_loosened_types(file_path: str, json_folder: str) -> None:
    """
    adds a __post_init__ method to the flattened types
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    class_title = json_data["title"]

    # this will be a file with a single class
    enum_tag = json_data.get("enum_tag", None)
    if enum_tag is None:
        return

    properties = json_data["properties"]

    enum_tag_to_other_required_keys: dict[str, list[str]] = json_data[
        "enum_tag_to_other_required_keys"
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines.append("\n    def __post_init__(self):\n")

    common_keys: set[str] = set.intersection(
        *map(set, enum_tag_to_other_required_keys.values())
    )
    union_keys = set.union(*map(set, enum_tag_to_other_required_keys.values()))

    i = 0
    for enum_value, required_keys in enum_tag_to_other_required_keys.items():
        if i == 0:
            conditional = "if"
        else:
            conditional = "elif"
        title = properties[enum_tag]["title"]

        req_keys_subset = [x for x in required_keys if x not in common_keys]

        should_be_empty_keys = list(union_keys - set(required_keys))

        s = (
            f'        {conditional} self.{enum_tag} == "{enum_value}":\n'
            f"            if not all(getattr(self, key) is not None for key in {req_keys_subset}):\n"
            f'                raise ValueError(f"When field {enum_tag} ({title}) is of value {enum_value}, class {class_title} requires fields {req_keys_subset}")\n'
            f"            elif any(getattr(self, key) is not None for key in {should_be_empty_keys}):\n"
            f'                raise ValueError(f"When field {enum_tag} ({title}) is of value {enum_value}, class {class_title} should not have fields {should_be_empty_keys}")\n'
        )
        lines.append(s)

        i += 1

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


def fix_enum_member_names(file_path: str, json_folder: str) -> None:
    """
    This function fixes the Python Enum values based on JSON file.

    For each enum class in the Python file (i.e. classes that inherit from Enum),
    it replaces the member names with the names defined in the JSON file under "x-enumNames".

    The JSON file is expected to have the same base name as the Python file.
    Example JSON structure for a key "CandleWidth":

    {
      "CandleWidth": {
        "type": "integer",
        "enum": [1, 2, 4, 8, 16, 32],
        "x-enumNames": [
          "OneSecond",
          "FiveSecond",
          "OneMinute",
          "FifteenMinute",
          "OneHour",
          "OneDay"
        ]
      },
      ...
    }
    """
    # Determine the JSON file path based on the Python file name.
    json_fp = get_corresponding_json_file(file_path, json_folder)

    # Load JSON configuration.
    with open(json_fp, "r") as jf:
        json_data = json.load(jf)

    # Read the Python file lines.
    with open(file_path, "r") as pf:
        lines = pf.readlines()

    # fix imports from other grpc classes
    # move to another function
    for i, line in enumerate(lines):
        if line != "from .. import definitions\n":
            m = import_fix_re.match(line)
            if m:
                dots, module, imports = m.groups()  # e.g. for "from . import Ticker":
                #   dots=".", module="" and imports="Ticker"

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
        # Remove any trailing newline for easier manipulation.
        line_stripped = line.rstrip("\n")

        # Look for an enum class definition.
        class_match = class_header_re.match(line_stripped)
        if class_match:
            indent, class_name = class_match.groups()
            if class_name in json_data:
                # Entering an enum class that is defined in the JSON.
                in_enum_class = True
                enum_class_indent = indent
                enum_values = json_data[class_name].get("enum", [])
                enum_names = json_data[class_name].get("x-enumNames", [])
            else:
                in_enum_class = False
            new_lines.append(line_stripped)
            continue

        # Process lines inside an enum class.
        if in_enum_class:
            member_match = member_re.match(line_stripped)
            if member_match:
                member_indent, member_name, member_value, rest = member_match.groups()
                # Check that the line is still indented relative to the enum class header.
                if len(member_indent) <= len(enum_class_indent):
                    # We've reached a dedented line; exit the enum class block.
                    in_enum_class = False
                    new_lines.append(line_stripped)
                    continue
                try:
                    value_int = int(member_value)
                except ValueError:
                    # If conversion fails, leave the line as is.
                    new_lines.append(line_stripped)
                    continue
                if value_int in enum_values:
                    index = enum_values.index(value_int)
                    new_member_name = enum_names[index]
                    # Construct the new line with the new member name.
                    new_line = (
                        f"{member_indent}{new_member_name} = {member_value}{rest}"
                    )
                    new_lines.append(new_line)
                else:
                    new_lines.append(line_stripped)
            else:
                # If the line doesn't match a member assignment, check if it is dedented.
                if line_stripped.strip() and not line_stripped.startswith(
                    " " * (len(enum_class_indent) + 1)
                ):
                    in_enum_class = False
                new_lines.append(line_stripped)
        else:
            new_lines.append(line_stripped)

    # Write the updated lines back to the Python file.
    with open(file_path, "w") as pf:
        pf.write("\n".join(new_lines))


def get_corresponding_json_file(file_path: str, json_folder: str) -> str:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return os.path.join(json_folder, f"{name}.json")


def generate_stub(file_path: str, json_folder: str) -> None:
    """
    For a request file, this generates the stub code for the request type
    that links the Request type to the Response type, service, and route.

    Reads from the json to get the information
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

        with open(file_path, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line == f'        return "&RESPONSE_TYPE:{request_type_name}"\n':
                lines[i] = f"        return {response_type}"
            elif line == f'        return "&ROUTE:{request_type_name}"\n':
                lines[i] = f'        return "{route}"'
            elif line == f'        return "&UNARY_TYPE:{request_type_name}"\n':
                lines[i] = f'        return "{unary_type}"'

        lines.insert(
            4,
            f"from architect_py.grpc_client.{service}.{response_type} import {response_type}\n",
        )

        with open(file_path, "w") as f:
            f.writelines(lines)


def fix_lines(file_path: str) -> None:
    """
    fixes types

    adds imports
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(line.strip() == "def timestamp(self) -> int:" for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    lines = [line.replace("Dir", "OrderDir") for line in lines]
    lines = [line.replace("definitions.OrderDir", "OrderDir") for line in lines]
    lines = [line.replace("(Struct)", "(Struct, omit_defaults=True)") for line in lines]

    if any("OrderDir" in line for line in lines):
        lines.insert(4, "from architect_py.scalars import OrderDir\n")

    l = "".join(lines)

    # Removes the OrderDir class definition from the file
    # (originally it was the Dir class definition)
    l = remove_OrderDir_re.sub("", l)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(l)


def main(file_path: str, json_folder: str) -> None:
    create_tagged_subtypes_for_variant_types(file_path, json_folder)

    fix_lines(file_path)
    if not file_path.endswith("definitions.py"):
        add_post_processing_to_loosened_types(file_path, json_folder)
        generate_stub(file_path, json_folder)
    fix_enum_member_names(file_path, json_folder)


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
