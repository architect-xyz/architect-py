import argparse
import json
import os
import re
from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------
# Constants and Regular Expressions
# ---------------------------------------------------------------------

DECIMAL_RE = re.compile(r'(^\s*)"\$ref": "#/definitions/Decimal"', flags=re.MULTILINE)
SINGLE_ALL_OF_DECIMAL = re.compile(
    r'"allOf":\s*\[\s*\{\s*'
    r'(?P<indent>[ \t]*)"type":\s*"number",\s*'
    r'(?P=indent)"format":\s*"decimal"\s*'
    r"\}\s*\]",
    flags=re.MULTILINE,
)
CAMEL_CASE_RE = re.compile(r"(?<!^)(?=[A-Z])")
EXTRACT_REF_RE = re.compile(r'("\$ref":\s*"#/definitions/)([^"]+)(")')


def replace_and_indent(match: re.Match) -> str:
    indent = match.group(1)
    return f'{indent}"type": "number",\n{indent}"format": "decimal"'


# ---------------------------------------------------------------------
# Type And Ref Fixing Functions
# ---------------------------------------------------------------------


def _apply_type_fixes_to_text(
    text: str, is_definitions_file: bool, type_to_json_file: Dict[str, str]
) -> str:
    """
    Perform string replacements and regex substitutions on the JSON text.
    """
    replacements = {
        "uint32": "default",
        "uint64": "default",
        '"format": "int"': '"format": "default"',
        '"format": "partial-date-time"': '"format": "time"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Fix Decimal references with proper indenting.
    text = DECIMAL_RE.sub(replace_and_indent, text)
    text = SINGLE_ALL_OF_DECIMAL.sub(replace_and_indent, text)

    def replace_ref(match: re.Match) -> str:
        prefix, class_title, suffix = match.groups()
        if class_title in type_to_json_file:
            ref = (
                f"{type_to_json_file[class_title]}/#"
                if is_definitions_file
                else f"../{type_to_json_file[class_title]}/#"
            )
        else:
            ref = (
                f"#/{class_title}"
                if is_definitions_file
                else f"../definitions.json#/{class_title}"
            )
        return f'"$ref": "{ref}"'

    return EXTRACT_REF_RE.sub(replace_ref, text)


def apply_type_fixes(
    schema: Dict, is_definitions_file: bool, type_to_json_file: Dict[str, str]
) -> Dict:
    """
    Convert the schema dictionary to text, apply type fixes, and convert it back.
    """
    json_text = json.dumps(schema, indent=2)
    fixed_text = _apply_type_fixes_to_text(
        json_text, is_definitions_file, type_to_json_file
    )
    return json.loads(fixed_text)


# ---------------------------------------------------------------------
# Schema Metadata and Enum Correction Functions
# ---------------------------------------------------------------------


def parse_class_description(text: str) -> Tuple[Dict[str, str], str]:
    """
    Parse metadata from a special comment in the description.
    Expected format: <!-- py: key1=value1, key2=value2 -->
    """
    pattern = r"<!--\s*py:\s*(.*?)\s*-->"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        raise ValueError("No valid 'py:' comment found in the text.")

    metadata_str = match.group(1)
    metadata: Dict[str, str] = {}
    for pair in metadata_str.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"Malformed key-value pair: '{pair}'")
        key, value = map(str.strip, pair.split("=", 1))
        metadata[key] = value

    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return metadata, cleaned_text


def correct_flattened_types(schema: Dict[str, Any]) -> None:
    """
    Processes any type that has
    #[serde(flatten)]

    because it would generate several types in the json
    while we want 1 type.

    Removes the oneOf list and merges common keys and additional properties.
    """
    if "oneOf" not in schema or "required" not in schema:
        return

    one_of: List[Dict[str, Any]] = schema.pop("oneOf")
    sets = [set(group) for group in one_of]
    common_keys: list[str] = list(set().intersection(*sets))
    additional_properties: Dict[str, Any] = {}

    enum_tag: str = ""
    enum_value_to_required: Dict[str, List[str]] = {}
    enum_tag_title = CAMEL_CASE_RE.sub("_", schema["title"]).lower()
    enum_tag_property: Dict[str, Any] = {
        "type": "string",
        "title": f"{enum_tag_title}_type",
        "enum": [],
    }

    for item in one_of:
        assert (
            item.get("type") == "object"
        ), f"Expected object type in {schema['title']}"
        properties = item.get("properties", {})
        required = item.get("required", [])
        for key, prop in properties.items():
            if "enum" in prop:
                if not enum_tag:
                    enum_tag = key
                else:
                    assert enum_tag == key, f"Enum field mismatch in {schema['title']}"
                [enum_value] = prop["enum"]
                enum_tag_property["enum"].append(enum_value)
                enum_value_to_required[enum_value] = required
            else:
                if key in additional_properties:
                    assert (
                        additional_properties[key] == prop
                    ), f"Conflicting properties for {key} in {schema['title']}"
                else:
                    additional_properties[key] = prop

    if not enum_tag:
        raise ValueError(f"Enum value not found in {schema['title']}")
    schema["required"].extend(common_keys)
    schema["properties"].update(additional_properties)
    schema["properties"][enum_tag] = enum_tag_property
    schema["enum_tag"] = enum_tag
    schema["enum_tag_to_other_required_keys"] = enum_value_to_required


def correct_enums(
    schema: Dict[str, Any],
    definitions: Dict[str, Any],
    type_to_json_file: Dict[str, str],
) -> None:
    """
    Process types that were Enums on the rust side.

    This is because the Variants need both the Variant name and the actual type name.

    pub enum Dropcopy {
        #[serde(rename = "o")]
        #[schemars(title = "Order|Order")]
        Order(Order),
        #[schemars(title = "Fill|Fill")]
        #[serde(rename = "f")]
        Fill(Fill),
        #[serde(rename = "af")]
        #[schemars(title = "AberrantFill|AberrantFill")]
        AberrantFill(AberrantFill),
    }
    """

    one_of_key = "oneOf"
    if one_of_key not in schema or "required" in schema:
        return

    description = schema.get("description", "")
    metadata, new_description = parse_class_description(description)
    if new_description.strip():
        schema["description"] = new_description.strip()
    else:
        schema.pop("description", None)

    tag = metadata["tag"]
    new_one_of: List[Dict[str, Any]] = []
    for item in schema[one_of_key]:
        item["required"].remove(tag)
        tag_field = item["properties"].pop(tag)
        title = item.pop("title")
        if "|" not in title:
            continue

        variant_name, type_name = title.split("|", 1)
        if type_name in definitions:
            if definitions[type_name] != item:
                raise ValueError(f"Conflicting definitions for {type_name}.")
        elif type_name in type_to_json_file:
            pass
        else:
            definitions[type_name] = item

        if type_name in type_to_json_file:
            ref = f"../{type_to_json_file[type_name]}/#"
            ref_correction = type_name
        else:
            ref = f"../definitions.json#/{type_name}"
            ref_correction = None

        enum_ref = {
            "$ref": ref,
            "tag": tag,
            "tag_field": tag_field,
            "variant_name": variant_name,
        }
        if ref_correction:
            enum_ref["ref_correction"] = ref_correction
        new_one_of.append(enum_ref)

    schema[one_of_key] = new_one_of


def process_schema_definitions(
    schema: Dict[str, Any],
    definitions: Dict[str, Any],
    type_to_json_file: Dict[str, str],
) -> None:
    """
    Extract and process definitions from a schema.
    Updates the "Decimal" format and applies enum corrections.
    """
    if "definitions" not in schema:
        return

    if "Decimal" in schema["definitions"]:
        schema["definitions"]["Decimal"]["format"] = "decimal"

    correct_enums(schema, definitions, type_to_json_file)
    correct_flattened_types(schema)

    new_defs: dict[str, Any] = schema.pop("definitions")
    for t, definition in new_defs.items():
        if t in type_to_json_file:
            continue
        definitions[t] = definition


# ---------------------------------------------------------------------
# Utility Functions for Service and File Handling
# ---------------------------------------------------------------------


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:] if word else word


def add_info_to_schema(services: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Enrich service definitions with metadata and build a mapping from type names to file paths.
    """
    type_to_json_file: Dict[str, str] = {}
    for service in services:
        service_name = service["name"].replace(" ", "_")
        service["service_name"] = service_name

        for rpc in service["rpcs"]:
            req_schema = rpc["request_type"]
            resp_schema = rpc["response_type"]

            # Add service-specific metadata.
            req_schema["route"] = rpc["route"]
            req_schema["unary_type"] = rpc["type"]
            req_schema["service"] = service_name

            # Standardize titles.
            response_type_name = "".join(
                capitalize_first_letter(word)
                for word in resp_schema["title"].split("_")
            )
            req_schema["response_type"] = response_type_name
            resp_schema["title"] = response_type_name

            req_title = "".join(
                capitalize_first_letter(word) for word in req_schema["title"].split("_")
            )
            req_schema["title"] = req_title

            type_to_json_file[req_title] = f"{service_name}/{req_title}.json"
            type_to_json_file[response_type_name] = (
                f"{service_name}/{response_type_name}.json"
            )
    return type_to_json_file


def write_json_file(data: Dict[Any, Any], path: str) -> None:
    with open(path, "w") as out_file:
        json.dump(data, out_file, indent=2)


def process_schema(
    schema: Dict[str, Any],
    definitions: Dict[str, Any],
    type_to_json_file: Dict[str, str],
    is_definitions_file: bool = False,
) -> Dict[str, Any]:
    """
    Process a schema by handling definitions and applying type fixes.
    """
    process_schema_definitions(schema, definitions, type_to_json_file)
    return apply_type_fixes(schema, is_definitions_file, type_to_json_file)


def process_service(
    service: Dict[str, Any],
    output_dir: str,
    definitions: Dict[str, Any],
    type_to_json_file: Dict[str, str],
) -> None:
    """
    Process each RPC within a service (both request and response) and write the resulting schema files.
    """
    service_name = service["service_name"]
    service_dir = os.path.join(output_dir, service_name)
    os.makedirs(service_dir, exist_ok=True)

    for rpc in service["rpcs"]:
        for key in ["request_type", "response_type"]:
            schema = rpc[key]
            processed_schema = process_schema(
                schema, definitions, type_to_json_file, False
            )
            schema_title = processed_schema["title"]
            file_path = os.path.join(service_dir, f"{schema_title}.json")
            write_json_file(processed_schema, file_path)


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by splitting each RPC's request and response schemas
    into separate JSON files and creating a unified definitions file.
    """
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, "r") as f:
        services = json.load(f)

    type_to_json_file = add_info_to_schema(services)
    definitions: Dict[str, Any] = {}

    for service in services:
        process_service(service, output_dir, definitions, type_to_json_file)

    fixed_definitions = apply_type_fixes(definitions, True, type_to_json_file)
    definitions_path = os.path.join(output_dir, "definitions.json")
    write_json_file(fixed_definitions, definitions_path)


# ---------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Process a gRPC JSON schema file.")
    parser.add_argument(
        "--architect_dir",
        type=str,
        default="~/architect",
        help="Path to the architect directory containing the api/schema.json file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="processed_schema",
        help="Path to output the extracted schema files.",
    )
    args = parser.parse_args()

    architect_dir = os.path.expanduser(args.architect_dir)
    input_file = os.path.join(architect_dir, "api/schema.json")
    preprocess_json(input_file, args.output_dir)


if __name__ == "__main__":
    main()
