import argparse
import os
import json
import importlib.util
import os
from typing import Annotated, get_args, get_origin


def main(file_path: str, json_folder: str) -> None:
    fix_lines(file_path)
    generate_stub(file_path, json_folder)


def capitalize_first_letter(word: str) -> str:
    return word[0].upper() + word[1:]


def import_class_from_filename(filename: str, class_name: str):
    module_name = os.path.splitext(os.path.basename(filename))[0]

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(module_name, filename)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"File '{filename}' not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    cls = getattr(module, class_name, None)

    if cls is None:
        raise AttributeError(f"Class '{class_name}' not found in {filename}")

    return cls


def extract_base_type(annotated_type) -> str:
    if get_origin(annotated_type) is Annotated:
        return get_args(annotated_type)[0]  # The first argument is the actual type
    else:
        return annotated_type.__name__  # If not Annotated, return as is


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
        response_file_root_name: str = j["response_type"]  # no extension
        route = j["route"]

        # the split("_") is for files like Array_of_L1BookSnapshot.json
        request_type_name = "".join(
            capitalize_first_letter(word) for word in name.split("_")
        )
        response_type_name = "".join(
            capitalize_first_letter(word) for word in response_file_root_name.split("_")
        )

        """
        This is for the case where the response type is an annotated union type such as
        L2BookUpdate = Annotated[
            Union[Snapshot, Diff],
            Meta(
                title='L2BookUpdate',
            ),
        ]
        This creates errors with the GRPCClient.subscribe types
        because it thinks the type is Annotated
        so we want to remove the Annotated part for the Helper class
        """
        response_file_path = (
            f"{file_path.replace(base_name, response_file_root_name)}.py"
        )
        c = import_class_from_filename(response_file_path, response_type_name)
        response_base_type_str = extract_base_type(c)

        with open(file_path, "r") as f:
            lines = f.readlines()

        if unary_type == "stream":
            request_import = (
                "from architect_py.grpc_client.request import RequestStream\n"
            )
        else:
            request_import = (
                "from architect_py.grpc_client.request import RequestUnary\n"
            )
        request_str = f"""
request_helper = Request{unary_type.title()}({request_type_name}, {response_base_type_str}, "{route}")
"""

        lines.insert(
            4,
            (
                f"from architect_py.grpc_client.{service}.{response_file_root_name} import {response_type_name}\n"
                f"{request_import}\n"
            ),
        )
        lines.append(f"\n{request_str}\n")

        with open(file_path, "w") as f:
            f.writelines(lines)


def fix_line(line: str) -> str:
    line = line.replace("DecimalModel", "Decimal")
    return line


def fix_lines(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines = [
        fix_line(line) for line in lines if line.strip() != "DecimalModel = Decimal"
    ]

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
