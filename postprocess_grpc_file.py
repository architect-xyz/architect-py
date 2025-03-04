import argparse
import os
import json


def main(file_path: str, json_folder: str) -> None:
    modify_imports(file_path)
    generate_stub(file_path, json_folder)


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:]


def generate_stub(file_path: str, json_folder: str) -> None:
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)

    if "Request" not in name:
        return

    json_fp = os.path.join(json_folder, f"{name}.json")
    with open(json_fp, "r", encoding="utf-8") as json_file:
        j = json.load(json_file)

        service = j["service"]
        unary_type = j["unary_type"]
        response_file_name: str = j["response_type"]

        request_type_name = "".join(
            capitalize_first_letter(word) for word in name.split("_")
        )
        response_type_name = "".join(
            capitalize_first_letter(word) for word in response_file_name.split("_")
        )

        route = j["route"]

        with open(file_path, "r") as f:
            lines = f.readlines()

        if unary_type == "stream":
            request_import = (
                "from architect_py.grpc_client.request import RequestStream\n"
            )
            request_str = f'{request_type_name}RequestHelper = RequestStream({request_type_name}, {response_type_name}, "{route}")'
        else:
            request_import = (
                "from architect_py.grpc_client.request import RequestUnary\n"
            )
            request_str = f'{request_type_name}RequestHelper = RequestUnary({request_type_name}, {response_type_name}, "{route}")'

        lines.insert(
            4,
            (
                "import grpc\n"
                "import msgspec\n"
                f"from architect_py.grpc_client.{service}.{response_file_name} import {response_type_name}\n"
                f"{request_import}\n"
            ),
        )

        lines.append(
            f"""
    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.Unary{unary_type.title()}MultiCallable["{request_type_name}", {response_type_name}]:
        return channel.unary_{unary_type}(
            "{route}",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type={response_type_name}
            ),
        )
"""
        )
        lines.append(f"\n{request_str}\n")

        with open(file_path, "w") as f:
            f.writelines(lines)


def modify_imports(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(line.strip() == "Decimal = str" for line in lines):
        print(f"Updating: {file_path}")

        lines = [line for line in lines if line.strip() != "Decimal = str"]
        lines.insert(4, "from decimal import Decimal\n\n")

    if any(line.strip() == "def timestamp(self) -> int:" for line in lines):
        lines.insert(4, "from datetime import datetime, timezone\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


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
