import argparse
import re
import json

import sys
import os

# Regex for removing the OrderDir class definition from the file
remove_OrderDir = re.compile(
    r"^class\s+OrderDir\b.*?(?=^class\s+\w|\Z)", re.DOTALL | re.MULTILINE
)

# regex for fixing imports from other grpc classes
import_fix = re.compile(r"^from\s+(\.+)(\w*)\s+import\s+(.+)$")

# Regex to find enum class definitions.
class_header_re = re.compile(r"^(\s*)class\s+(\w+)\([^)]*Enum[^)]*\)\s*:")

# Regex to find member assignments. It assumes the member value is an integer literal.
member_re = re.compile(r"^(\s*)(\w+)\s*=\s*([0-9]+)(.*)")


def modify_class_definition(
    file_text: str, class_name: str, tag: str, tag_field: str
) -> str:
    """
    Finds the class definition for `class_name` in file_text and
    modifies its base list so that the first base "Struct" is replaced with
    "Struct, tag="<tag>", tag_field="<tag_field>".
    """
    # regex to capture a class definition line like:
    #   class ClassName(Base1, Base2):
    # We look for the first occurrence of "Struct" within the parenthesized list.
    pattern = re.compile(
        rf"^(class\s+{re.escape(class_name)}\s*\((.*?)\))",
        re.MULTILINE | re.DOTALL,
    )

    def repl(match):
        whole_line = match.group(0)
        bases = match.group(2)
        # Replace first occurrence of "Struct" in the bases with the extended version.
        new_bases, count = re.subn(
            r"\bStruct\b",
            f'Struct, tag="{tag}", tag_field="{tag_field}"',
            bases,
            count=1,
        )
        return whole_line.replace(bases, new_bases)

    new_text, count = pattern.subn(repl, file_text)
    if count == 0:
        print(
            f"Warning: class {class_name} definition not found or not modified.",
            file=sys.stderr,
        )
    return new_text


def create_tagged_subtypes_for_variant_types(file_path: str, json_folder: str) -> None:
    """
    this is for Variant types with a tag

    This creates subtypes for the variant types to add the tag to the class
    """
    json_fp = get_corresponding_json_file(file_path, json_folder)
    with open(json_fp, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    if not json_data.get("tagged", False):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if "Request" in file_path:
        service = json_data["service"]
        unary_type = json_data["unary_type"]
        response_type = json_data["response_type"]
        route = json_data["route"]
        lines.append(f'\n\nunary = "{unary_type}"\n')
        lines.append(f"response_type = {response_type}\n")
        lines.append(f'route = "{route}"\n')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))


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
            m = import_fix.match(line)
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

    # Write the updated content back to the Python file.
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
    # lines = [line.replace("(Struct)", "(Struct, omit_defaults=True)") for line in lines]

    if any("OrderDir" in line for line in lines):
        lines.insert(4, "from architect_py.scalars import OrderDir\n")

    l = "".join(lines)

    # Removes the OrderDir class definition from the file
    # (originally it was the Dir class definition)
    l = remove_OrderDir.sub("", l)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(l)


def main(file_path: str, json_folder: str) -> None:
    fix_lines(file_path)
    if not file_path.endswith("definitions.py"):
        add_post_processing_to_loosened_types(file_path, json_folder)
        generate_stub(file_path, json_folder)
    fix_enum_member_names(file_path, json_folder)
    # create_tagged_subtypes_for_variant_types(file_path, json_folder)


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
