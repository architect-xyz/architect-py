import argparse
import re

# Drop the entire __init__ block + docstring (indented 4 spaces or a tab)
INIT_BLOCK_RE = re.compile(
    r"""
    ^[ \t]+def[ \t]+__init__\(         # 1⃣  the signature line begins
        [^)]*                          #     params (no closing paren yet)
    \)[^\n]*:[ \t]*\n                  #  → return-type + colon + newline
    (?:                                # 2⃣  optional docstring
        [ \t]+(?:\"\"\"|\'\'\')        #     opening triple quotes
        [\s\S]*?                       #     body, any chars incl. newlines
        (?:\"\"\"|\'\'\')[ \t]*\n      #     closing triple quotes
    )?
    (?:                                # 3⃣  optional stub body
        [ \t]+(?:\.\.\.|pass)[^\n]*\n
    )?
    """,
    re.MULTILINE | re.VERBOSE,
)


def correct_sync_interface(content: str):
    """
    Correct the sync interface in the gRPC service definitions.

    These lines are sensitive to the order of the lines in the file.
    """

    content = f"# fmt: off\n# mypy: ignore-errors\n# ruff: noqa\n{content}"

    content = INIT_BLOCK_RE.sub("", content)

    # Remove all stream, orderflow, and subscribe methods
    lines = content.splitlines()
    i = 0
    delete_bool = False
    while i < len(lines):
        if "def" in lines[i]:
            delete_bool = False

        if delete_bool:
            del lines[i]
        else:
            line = lines[i]
            if "def" in line and (
                "stream" in line or "orderflow" in line or "subscribe" in line
            ):
                delete_bool = True
                del lines[i]
                if "@" in lines[i - 1]:
                    i = -1
                    del lines[i]
            else:
                i += 1
    content = "\n".join(lines)

    # Remove the @staticmethod decorator that precedes connect()
    # and then replace the connect() method with __init__()
    content = re.sub(
        r"^[ \t]*@staticmethod[ \t]*\n"  # decorator on its own line
        r"([ \t]*)async[ \t]+def[ \t]+connect\(",  # capture indent before 'async'
        r"\1def __init__(self, ",  # keep indent, add self-param
        content,
        flags=re.MULTILINE,
    )

    # turn the connect() method into __init__()
    content = re.sub(
        r"^([ \t]*)async[ \t]+def[ \t]+connect\(",
        r"\1def __init__(self, ",
        content,
        flags=re.MULTILINE,
    )

    # Change return annotation from -> AsyncClient  to -> None
    content = re.sub(
        r"->[ \t]*AsyncClient",
        "-> None",
        content,
    )

    # Replace the async method definitions with sync method definitions
    content = content.replace("async def", "def")
    content = content.replace("await ", "")
    content = content.replace("AsyncClient", "Client")

    # Write the corrected content back to the file
    with open(args.file_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process gRPC service definitions")
    parser.add_argument(
        "--file_path",
        type=str,
        help="Path to the Python folder with the gRPC service definitions",
    )
    args = parser.parse_args()

    with open(args.file_path, "r") as f:
        content = f.read()
    correct_sync_interface(content)
