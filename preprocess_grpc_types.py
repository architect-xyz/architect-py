import argparse
import json
import os

import re


def replace_and_indent(m):
    indent = m.group(1)
    return f'{indent}"type": "string",\n{indent}"format": "decimal"'


def file_fixes(lines: str) -> str:
    lines = lines.replace("uint32", "default")
    lines = lines.replace("uint64", "default")
    lines = lines.replace('"format": "int"', '"format": "default"')
    # lines = lines.replace(
    #     '"$ref": "#/definitions',
    #     '"$ref": "../definitions.json#/',
    # )

    pattern = r'(^\s*)"\$ref": "#/definitions/Decimal"'
    lines = re.sub(pattern, replace_and_indent, lines, flags=re.MULTILINE)

    return lines


def generate_cleaned_schema(processed_schema_file: str) -> dict:
    with open(input_file, "r") as f:
        lines = f.read()

    lines = file_fixes(lines)

    with open(processed_schema_file, "w") as f:
        f.writelines(lines)

    with open(processed_schema_file, mode="r") as f:
        services = json.load(f)
    return services


def process_schema_definitions(schema: dict):
    if "definitions" not in schema:
        return

    if "Decimal" in schema["definitions"]:
        schema["definitions"]["Decimal"]["format"] = "decimal"


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    and writing them to separate JSON files.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    processed_schema_file = os.path.join(output_dir, "schema.json")
    services = generate_cleaned_schema(processed_schema_file)

    for service in services:
        service_name = service["name"].replace(" ", "_")

        output_sub_dir = os.path.join(output_dir, service_name)
        os.makedirs(output_sub_dir, exist_ok=True)

        rpcs = service.get("rpcs", [])
        for rpc in rpcs:

            # Process the request type schema.
            req_schema = rpc.get("request_type")
            resp_schema = rpc.get("response_type")

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
                print(f"Extracted response schema to: {resp_path}")


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
