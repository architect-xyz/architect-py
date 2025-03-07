import argparse
import json
import os
import re


def replace_and_indent(m):
    indent = m.group(1)
    return f'{indent}"type": "number",\n{indent}"format": "decimal"'


def fix_lines(lines: str, is_definitions_file: bool) -> str:
    lines = lines.replace("uint32", "default")
    lines = lines.replace("uint64", "default")
    lines = lines.replace('"format": "int"', '"format": "default"')

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


def fix_dict(d: dict, is_definitions_file: bool) -> dict:
    lines = json.dumps(d, indent=2)
    lines = fix_lines(lines, is_definitions_file)
    return json.loads(lines)


def process_schema_definitions(schema: dict) -> dict:
    if "definitions" not in schema:
        return {}

    if "Decimal" in schema["definitions"]:
        schema["definitions"]["Decimal"]["format"] = "decimal"

    return schema.pop("definitions")


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    and writing them to separate JSON files.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        lines = f.read()
    services = json.loads("".join(lines))

    definitions = {}
    for service in services:
        service_name = service["name"].replace(" ", "_")

        output_sub_dir = os.path.join(output_dir, service_name)
        os.makedirs(output_sub_dir, exist_ok=True)

        rpcs = service.get("rpcs", [])
        for rpc in rpcs:

            # Process the request type schema.
            req_schema: dict = rpc.get("request_type")
            resp_schema: dict = rpc.get("response_type")

            definitions.update(process_schema_definitions(req_schema))
            definitions.update(process_schema_definitions(resp_schema))

            req_schema = fix_dict(req_schema, False)
            resp_schema = fix_dict(resp_schema, False)

            route = rpc.get("route")
            unary_type = rpc.get("type")

            if req_schema:
                req_schema["route"] = route
                req_schema["unary_type"] = unary_type
                req_schema["service"] = service_name
                req_schema["response_type"] = resp_schema["title"]

                req_title = req_schema.get("title", "Request")
                req_filename = f"{req_title}.json"
                req_path = os.path.join(output_sub_dir, req_filename)
                with open(req_path, "w") as out_file:
                    json.dump(req_schema, out_file, indent=2)

            # Process the response type schema.
            if resp_schema:
                resp_title = resp_schema.get("title", "Response")
                resp_filename = f"{resp_title}.json"

                resp_path = os.path.join(output_sub_dir, resp_filename)
                with open(resp_path, "w") as out_file:
                    json.dump(resp_schema, out_file, indent=2)

    with open(os.path.join(output_dir, "definitions.json"), "w") as out_file:
        definitions = fix_dict(definitions, True)
        json.dump(definitions, out_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a JSON file.")
    parser.add_argument(
        "--input_file",
        type=str,
        nargs="?",
        default="~/architect/api/schema.json",
        help="Path to the JSON file with the gRPC service definitions",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        nargs="?",
        default="processed_schema",
        help="Path to output the extracted schema files.",
    )
    args = parser.parse_args()
    input_file = os.path.expanduser(args.input_file)
    preprocess_json(input_file, args.output_dir)
