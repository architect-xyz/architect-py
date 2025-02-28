import argparse
import json
import os


def preprocess_json(input_file: str, output_dir: str) -> None:
    """
    Preprocess the gRPC JSON file by extracting each RPC's request and response schemas
    and writing them to separate JSON files.

    :param input_file: Path to the input JSON file containing an array of service definitions.
    :param output_dir: Directory where extracted schema files will be saved.
    """
    with open(input_file, "r") as f:
        services = json.load(f)

    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each service in the input array.
    for service in services:
        service_name = service["name"].replace(" ", "_")

        output_sub_dir = os.path.join(output_dir, service_name)
        os.makedirs(output_sub_dir, exist_ok=True)

        rpcs = service.get("rpcs", [])
        for rpc in rpcs:
            # Process the request type schema.
            req_schema = rpc.get("request_type")
            if req_schema:
                req_title = req_schema.get("title", "Request").replace(" ", "_")
                req_filename = f"{service_name}_{req_title}.json"
                req_path = os.path.join(output_sub_dir, req_filename)
                with open(req_path, "w") as out_file:
                    json.dump(req_schema, out_file, indent=2)
                print(f"Extracted request schema to: {req_path}")

            # Process the response type schema.
            resp_schema = rpc.get("response_type")
            if resp_schema:
                resp_title = resp_schema.get("title", "Response").replace(" ", "_")
                resp_filename = f"{service_name}_{resp_title}.json"

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
