import argparse
import os
import json


def main(file_path: str, json_folder: str) -> None:
    delete_decimal_equals_str(file_path)
    generate_stub(file_path, json_folder)


def generate_stub(file_path: str, json_folder: str) -> None:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)

    if "Request" not in name:
        return

    json_fp = os.path.join(json_folder, f"{name}.json")
    with open(json_fp, "r", encoding="utf-8") as json_file:
        j = json.load(json_file)

        service = j["service"]
        response_type = j["response_type"]
        request_type = j["request_type"]
        route = j["route"]

        with open(file_path, "r") as f:
            lines = f.readlines()

        lines.insert(4, "import grpc\nimport msgspec\n")
        lines.insert(
            4,
            f"from architect_py.grpc_client.{service}.{response_type} import {response_type}\n",
        )

        lines.extend(
            f"""
    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.Unary{request_type.title()}MultiCallable["{name}", {response_type}]:
        return channel.unary_{request_type}(
            "{route}",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type={response_type}
            ),
        )
"""
        )

        with open(file_path, "w") as f:
            f.writelines(lines)


def delete_decimal_equals_str(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(line.strip() == "Decimal = str" for line in lines):
        print(f"Updating: {file_path}")

        new_lines = [line for line in lines if line.strip() != "Decimal = str"]

        if not any(line.strip() == "from decimal import Decimal" for line in new_lines):
            new_lines.insert(4, "from decimal import Decimal\n\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)


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
