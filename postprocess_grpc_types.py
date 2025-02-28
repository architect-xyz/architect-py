import argparse
import os


def delete_decimal_equals_str(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check if the file contains "Decimal = str"
    if any(line.strip() == "Decimal = str" for line in lines):
        print(f"Updating: {file_path}")

        # Remove "Decimal = str" and ensure "from decimal import Decimal" is at the top
        new_lines = [line for line in lines if line.strip() != "Decimal = str"]

        # Insert import at the top if not already present
        if not any(line.strip() == "from decimal import Decimal" for line in new_lines):
            new_lines.insert(4, "from decimal import Decimal\n\n")

        # Rewrite the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)


def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                delete_decimal_equals_str(os.path.join(root, file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder of types")
    parser.add_argument(
        "--directory",
        type=str,
        nargs="?",
        default="architect_py/grpc_client",
        help="Path to the JSON file with the gRPC service definitions",
    )

    args = parser.parse_args()
    directory = os.path.expanduser(args.directory)

    scan_directory(directory)
