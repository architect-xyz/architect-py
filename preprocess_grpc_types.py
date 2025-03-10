import argparse
import json
import os
import re
from typing import Any


def replace_and_indent(m):
    indent = m.group(1)
    return f'{indent}"type": "number",\n{indent}"format": "decimal"'


def fix_types_in_json_lines(lines: str, is_definitions_file: bool) -> str:
    lines = lines.replace("uint32", "default")
    lines = lines.replace("uint64", "default")
    lines = lines.replace('"format": "int"', '"format": "default"')
    lines = lines.replace(
        '"format": "partial-date-time"', '"format": "time"'
    )  # NaiveTime -> partial-date-time
    # NaiveDate goes to "format": "date"

    pattern = r'(^\s*)"\$ref": "#/definitions/Decimal"'
    lines = re.sub(pattern, replace_and_indent, lines, flags=re.MULTILINE)

    # all of pattern
    pattern = (
        r'"allOf":\s*\[\s*\{\s*'
        r'(?P<indent>[ \t]*)"type":\s*"number",\s*'
        r'(?P=indent)"format":\s*"decimal"\s*'
        r"\}\s*\]"
    )
    lines = re.sub(pattern, replace_and_indent, lines, flags=re.MULTILINE)

    if is_definitions_file:
        lines = lines.replace("#/definitions", "#")
    else:
        lines = lines.replace("#/definitions", "../definitions.json#")

    return lines


def fix_types_in_dict(d: dict, is_definitions_file: bool) -> dict:
    lines = json.dumps(d, indent=2)
    lines = fix_types_in_json_lines(lines, is_definitions_file)
    return json.loads(lines)


def parse_class_description(text: str) -> tuple[dict[str, str], str]:
    # Use regex to capture the content after "py:" up to the closing comment marker.
    pattern = r"<!--\s*py:\s*(.*?)\s*-->"
    match = re.search(r"<!--\s*py:\s*(.*?)\s*-->", text, re.DOTALL)
    if not match:
        raise ValueError("No valid 'py:' comment found in the text.")

    inner_content = match.group(1)
    parsed_dict = {}
    for pair in inner_content.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"Malformed key-value pair: '{pair}'")
        key, value = map(str.strip, pair.split("=", 1))
        parsed_dict[key] = value

    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)

    return parsed_dict, cleaned_text


def correct_enums(
    schema: dict[str, Any], definitions: dict[str, Any], type_to_json: dict[str, str]
):
    """
    This parses the tag from the description of the schema and puts it in the dictionary

    The keys accessed in this function *must* exist.
    For the oneOf schema, we remove the tag from the required list and the properties.

    We point any of the definitions in the oneOf with a title, we put it as a $ref pointing
    to the definition in the definitions file, to reduce code duplication.
    """
    one_of = "oneOf"
    if one_of in schema:
        if "required" in schema:
            # this is a flatten and not an enum
            return
        description = schema["description"]
        description_metadata, new_description = parse_class_description(description)
        if new_description:
            schema["description"] = new_description
        else:
            schema.pop("description")

        tag = description_metadata["tag"]

        new_one_of = []
        for item in schema[one_of]:
            item["required"].remove(tag)

            tag_field = item["properties"].pop(tag)

            title = item.pop("title")  # this is to stay consistent with the definitions
            if "|" not in title:
                continue
            [variant_name, type_name] = title.split("|", 1)

            if type_name in definitions:
                if definitions[type_name] != item:
                    print(f"ERROR: Conflicting definitions for {type_name}.")
                    print(item)
                    print(definitions[type_name])
                    for key in item.keys():
                        if item[key] != definitions[type_name].get(key):
                            print(f"\n{key}:")
                            print(f"{item[key]}")
                            print(definitions[type_name])
                    raise ValueError(f"Conflicting definitions for {type_name}.")
            else:
                definitions[type_name] = item

            if type_name in type_to_json:
                ref = f"../{type_to_json[type_name]}/#"
            else:
                ref = f"../definitions.json#/{type_name}"

            new_one_of.append(
                {
                    "$ref": ref,
                    "tag": tag,
                    "tag_field": tag_field,
                    "variant_name": variant_name,
                }
            )  # this info is used for post-processing to add the tag / tag_field

        schema[one_of] = new_one_of


def process_schema_definitions(
    schema: dict[str, Any], definitions: dict[str, Any], type_to_json: dict[str, str]
):
    """
    We pop the definitions because we want to keep the definitions in a separate file.
    This will lead to the creation of a definitions.json file that will be used to
    reference the definitions in the other files.
    We do this because the defintions are repeated in the schema files and we want to
    avoid duplicate class definitions.

    The keys accessed in this function *must* exist.
    """

    if "definitions" not in schema:
        return

    if "Decimal" in schema["definitions"]:
        schema["definitions"]["Decimal"]["format"] = "decimal"

    try:
        correct_enums(schema, definitions, type_to_json)
    except Exception as e:
        print("ERROR: ")
        print(schema)
        raise

    definitions.update(schema.pop("definitions"))


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:]


def add_info_to_schema(schema: list[dict[str, Any]]) -> dict[str, str]:
    # returns request type to json location

    type_to_file = {}
    for service in schema:
        service_name = service["name"].replace(" ", "_")
        service["service_name"] = service_name

        rpcs = service.get("rpcs", [])
        for rpc in rpcs:
            # Process the request type schema.
            req_schema: dict[str, Any] = rpc.get("request_type")
            resp_schema: dict[str, Any] = rpc.get("response_type")

            assert req_schema and resp_schema

            route = rpc.get("route")
            unary_type = rpc.get("type")

            # these dict keys will later be referenced in the post-processing for
            # linking the request and response types to the service and route
            req_schema["route"] = route
            req_schema["unary_type"] = unary_type
            req_schema["service"] = service_name

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

            type_to_file[req_title] = f"{service_name}/{req_title}.json"
            type_to_file[response_type_name] = (
                f"{service_name}/{response_type_name}.json"
            )

    return type_to_file


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    and writing them to separate JSON files.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        schema = json.load(f)

    type_to_json = add_info_to_schema(schema)

    definitions = {}  # for definitions.json
    for service in schema:
        service_name = service["service_name"]
        output_sub_dir = os.path.join(output_dir, service_name)
        os.makedirs(output_sub_dir, exist_ok=True)

        rpcs = service.get("rpcs", [])
        for rpc in rpcs:

            # Process the request type schema.
            req_schema: dict[str, Any] = rpc.get("request_type")
            resp_schema: dict[str, Any] = rpc.get("response_type")

            process_schema_definitions(req_schema, definitions, type_to_json)
            process_schema_definitions(resp_schema, definitions, type_to_json)

            req_schema = fix_types_in_dict(req_schema, False)
            resp_schema = fix_types_in_dict(resp_schema, False)

            if req_schema:
                # these dict keys will later be referenced in the post-processing for
                # linking the request and response types to the service and route
                req_title = req_schema["title"]
                req_filename = f"{req_title}.json"
                req_path = os.path.join(output_sub_dir, req_filename)
                with open(req_path, "w") as out_file:
                    json.dump(req_schema, out_file, indent=2)

            # Process the response type schema.
            if resp_schema:
                resp_title = resp_schema["title"]

                resp_filename = f"{resp_title}.json"
                resp_path = os.path.join(output_sub_dir, resp_filename)
                with open(resp_path, "w") as out_file:
                    json.dump(resp_schema, out_file, indent=2)

    with open(os.path.join(output_dir, "definitions.json"), "w") as out_file:
        definitions = fix_types_in_dict(definitions, True)
        json.dump(definitions, out_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a JSON file.")
    parser.add_argument(
        "--architect_dir",
        type=str,
        nargs="?",
        default="~/architect",
        help="Path to architect directory containing the api/schema.json file.",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        nargs="?",
        default="processed_schema",
        help="Path to output the extracted schema files.",
    )
    args = parser.parse_args()
    input_file = os.path.expanduser(args.architect_dir)

    input_file = os.path.join(input_file, "api/schema.json")
    preprocess_json(input_file, args.output_dir)
