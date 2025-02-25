import argparse
from collections import defaultdict
import json
import os
from pathlib import Path


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    and writing them to separate JSON files.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    with open(input_file, "r") as f:
        services: list = json.load(f)

    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)
    # Collect all definitions across services
    global_defs = defaultdict(dict)
    for service in services:
        for rpc in service["rpcs"]:
            for schema_type in ["request_type", "response_type"]:
                if schema := rpc.get(schema_type):
                    global_defs[service["name"]].update(schema.get("definitions", {}))

    # Process each service
    for service in services:
        service_name = service["name"]
        service_dir = Path(output_dir) / service_name
        service_dir.mkdir(parents=True, exist_ok=True)

        # Create definitions file for the service
        defs_path = service_dir / "_definitions.json"
        with open(defs_path, "w") as f:
            json.dump(
                {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "definitions": global_defs[service["name"]],
                },
                f,
                indent=2,
            )

        # Process each RPC with references to definitions
        for rpc in service["rpcs"]:
            for schema_type in ["request_type", "response_type"]:
                if not (schema := rpc.get(schema_type)):
                    continue

                # Create standalone schema with ref to definitions
                full_schema = {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "$ref": f"#/definitions/{schema['title']}",
                    "definitions": {
                        **global_defs[service["name"]],
                        schema["title"]: {
                            k: v for k, v in schema.items() if k != "definitions"
                        },
                    },
                }

                # Clean filename
                route = rpc["route"].split("/")[-1]
                filename = f"{route}_{schema_type}.json"
                output_path = service_dir / filename

                with open(output_path, "w") as f:
                    json.dump(full_schema, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a JSON file.")
    parser.add_argument(
        "input_file",
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
