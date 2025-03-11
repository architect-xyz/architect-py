import argparse
import json
import os
import re
from typing import Any, Dict, Tuple, List


decimal_re = re.compile(r'(^\s*)"\$ref": "#/definitions/Decimal"', flags=re.MULTILINE)

single_all_of_decimal = re.compile(
    r'"allOf":\s*\[\s*\{\s*'
    r'(?P<indent>[ \t]*)"type":\s*"number",\s*'
    r'(?P=indent)"format":\s*"decimal"\s*'
    r"\}\s*\]",
    flags=re.MULTILINE,
)


# camel case regex
camel_case_re = re.compile(r"(?<!^)(?=[A-Z])")


extract_type_from_ref_re = re.compile(r'("\$ref":\s*"#/definitions/)([^"]+)(")')


def replace_and_indent(match: re.Match) -> str:
    """Helper function to replace matched ref lines with a formatted JSON snippet."""
    indent = match.group(1)
    return f'{indent}"type": "number",\n{indent}"format": "decimal"'


def fix_types_in_json_lines(
    text: str, is_definitions_file: bool, type_to_json: dict[str, str]
) -> str:
    """
    Apply various string replacements and regex substitutions on JSON text.

    Replaces type names and formats with standardized values and adjusts JSON $ref links.
    """
    replacements = {
        "uint32": "default",
        "uint64": "default",
        '"format": "int"': '"format": "default"',
        '"format": "partial-date-time"': '"format": "time"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Replace "$ref": "#/definitions/Decimal" with proper indenting.
    text = decimal_re.sub(replace_and_indent, text)

    # Process "allOf" to be Decimal
    text = single_all_of_decimal.sub(replace_and_indent, text)

    """
        if type_name in type_to_json:
            ref = f"../{type_to_json[type_name]}/#"
            ref_correction = type_name
        else:
            ref = f"../definitions.json#/{type_name}"
            ref_correction = None
    """

    def replace_ref(mtch):
        prefix, class_title, suffix = mtch.groups()

        if class_title in type_to_json:
            if is_definitions_file:
                ref = f"{type_to_json[class_title]}/#"
            else:
                ref = f"../{type_to_json[class_title]}/#"
        else:
            if is_definitions_file:
                ref = f"#/{class_title}"
            else:
                ref = f"../definitions.json#/{class_title}"
        return f'"$ref": "{ref}"'

    text = extract_type_from_ref_re.sub(replace_ref, text)

    return text


def fix_types_in_dict(
    d: Dict, is_definitions_file: bool, type_to_json: dict[str, str]
) -> Dict:
    """
    Convert a dictionary to a JSON string, fix types using string operations,
    and then parse back to a dictionary.
    """
    json_text = json.dumps(d, indent=2)
    fixed_text = fix_types_in_json_lines(json_text, is_definitions_file, type_to_json)
    return json.loads(fixed_text)


def parse_class_description(text: str) -> Tuple[Dict[str, str], str]:
    """
    Parse metadata from a special comment in the description.

    Expected format: <!-- py: key1=value1, key2=value2 -->
    Returns a tuple of the parsed metadata dictionary and the remaining text.
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

    # Remove the metadata comment from the original text.
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return metadata, cleaned_text


def correct_enums(
    schema: Dict[str, Any],
    definitions: Dict[str, Any],
    type_to_json: Dict[str, str],
) -> None:
    """
    Process enum-like schema entries.

    If the schema contains a "oneOf" entry without a top-level "required", parse the
    metadata from the description to adjust enum definitions and store unique definitions.
    """
    one_of_key = "oneOf"
    if one_of_key not in schema:
        return

    # Skip processing if the schema is a flattened type rather than an enum.
    if "required" in schema:
        # this should be in a separate function

        # see Order class for example
        one_of: list[dict[str, str | dict[str, Any]]] = schema.pop(one_of_key)

        sets = [set(group) for group in one_of]
        common_keys: list[str] = list(set().intersection(*sets))
        additional_properties: dict[str, dict[str, Any]] = {}

        enum_tag: str | None = None
        enum_value_to_required: dict[str, list[str]] = {}

        enum_tag_title = camel_case_re.sub("_", schema["title"]).lower()
        enum_tag_property: dict[str, str | list[str]] = {
            "type": "string",
            "title": f"{enum_tag_title}_type",
            "enum": [],
        }
        assert isinstance(enum_tag_property["enum"], list)

        for obj in one_of:
            assert obj["type"] == "object"
            assert "properties" in obj and isinstance(obj["properties"], dict)
            assert "required" in obj and isinstance(obj["required"], list)
            properties: dict[str, dict[str, Any]] = obj["properties"]
            required: list[str] = obj["required"]
            for key, ppty in properties.items():
                if "enum" in ppty:
                    key_type: str = ppty["type"]
                    assert (
                        key_type == "string"
                    ), f"Field {key} in {schema['title']} is not a string"
                    if enum_tag is None:
                        enum_tag = key
                    else:
                        assert (
                            enum_tag == key
                        ), f"Field {key} with property {ppty} in {schema['title']} broke assumptions: enum values differ"
                    [enum_value] = ppty["enum"]
                    enum_tag_property["enum"].append(enum_value)
                    enum_value_to_required[enum_value] = required
                else:
                    if key in additional_properties:
                        assert (
                            additional_properties[key] == ppty
                        ), f"Conflicting properties for {key} in {schema['title']}"
                    else:
                        additional_properties[key] = ppty
        assert enum_tag is not None, f"Enum value not found in {schema['title']}"

        assert isinstance(schema["required"], list)

        schema["required"].extend(common_keys)
        schema["properties"].update(additional_properties)

        schema["properties"][enum_tag] = enum_tag_property
        schema["enum_tag"] = enum_tag
        schema["enum_tag_to_other_required_keys"] = enum_value_to_required
        return

    description = schema["description"]
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
                print(f"ERROR: Conflicting definitions for {type_name}.")
                print("New item:", item)
                print("Existing definition:", definitions[type_name])
                for key in item:
                    if item[key] != definitions[type_name].get(key):
                        print(f"\n{key}:")
                        print(item[key])
                        print(definitions[type_name].get(key))
                raise ValueError(f"Conflicting definitions for {type_name}.")
        else:
            definitions[type_name] = item

        if type_name in type_to_json:
            ref = f"../{type_to_json[type_name]}/#"
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
    type_to_json: Dict[str, str],
) -> None:
    """
    Process the "definitions" in a schema and separate them to avoid duplication.

    This function also updates the "Decimal" definition and handles enum corrections.
    """
    if "definitions" not in schema:
        return

    if "Decimal" in schema["definitions"]:
        schema["definitions"]["Decimal"]["format"] = "decimal"

    try:
        correct_enums(schema, definitions, type_to_json)
    except Exception:
        print("ERROR processing schema:")
        print(json.dumps(schema, indent=2))
        raise

    # Merge processed definitions into the global definitions dictionary.
    definitions.update(schema.pop("definitions"))


def capitalize_first_letter(word: str) -> str:
    """Return the word with its first letter capitalized."""
    return word[0].upper() + word[1:] if word else word


def add_info_to_schema(services: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Enrich service definitions with additional metadata and build a mapping from type names to file paths.

    This mapping is later used to generate $ref links.
    """
    type_to_file: Dict[str, str] = {}
    for service in services:
        service_name = service["name"].replace(" ", "_")
        service["service_name"] = service_name

        for rpc in service["rpcs"]:
            req_schema: Dict[str, Any] = rpc["request_type"]
            resp_schema: Dict[str, Any] = rpc["response_type"]

            # Add service-specific metadata.
            req_schema["route"] = rpc["route"]
            req_schema["unary_type"] = rpc["type"]
            req_schema["service"] = service_name

            # Standardize the response type title.
            response_type_name = "".join(
                capitalize_first_letter(word)
                for word in resp_schema["title"].split("_")
            )
            req_schema["response_type"] = response_type_name
            resp_schema["title"] = response_type_name

            # Standardize the request type title.
            req_title = "".join(
                capitalize_first_letter(word) for word in req_schema["title"].split("_")
            )
            req_schema["title"] = req_title

            type_to_file[req_title] = f"{service_name}/{req_title}.json"
            type_to_file[response_type_name] = (
                f"{service_name}/{response_type_name}.json"
            )
    return type_to_file


def write_json_file(data: Dict[Any, Any], path: str) -> None:
    """Write a dictionary as a pretty-printed JSON file to the given path."""
    with open(path, "w") as out_file:
        json.dump(data, out_file, indent=2)


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    into separate JSON files and creating a unified definitions file.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        services = json.load(f)

    type_to_json = add_info_to_schema(services)
    definitions: Dict[str, Any] = {}

    for service in services:
        service_name = service["service_name"]
        service_dir = os.path.join(output_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)

        for rpc in service["rpcs"]:
            req_schema: Dict[str, Any] = rpc["request_type"]
            resp_schema: Dict[str, Any] = rpc["response_type"]

            process_schema_definitions(req_schema, definitions, type_to_json)
            process_schema_definitions(resp_schema, definitions, type_to_json)

            # Fix type formats in the schemas.
            req_schema = fix_types_in_dict(req_schema, False, type_to_json)
            resp_schema = fix_types_in_dict(resp_schema, False, type_to_json)

            # Write request schema.
            req_title = req_schema["title"]
            req_path = os.path.join(service_dir, f"{req_title}.json")
            write_json_file(req_schema, req_path)

            # Write response schema.
            resp_title = resp_schema["title"]
            resp_path = os.path.join(service_dir, f"{resp_title}.json")
            write_json_file(resp_schema, resp_path)

    # Process and write the consolidated definitions.
    definitions = fix_types_in_dict(definitions, True, type_to_json)
    definitions_path = os.path.join(output_dir, "definitions.json")
    write_json_file(definitions, definitions_path)


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
