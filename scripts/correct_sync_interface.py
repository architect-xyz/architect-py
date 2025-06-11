import argparse
import inspect
import re
import textwrap

from architect_py import Client


def delete_method_and_docstring(names: list[str], lines: list[str]) -> list[str]:
    """
    Delete a method and its docstring from the lines of a file if the method name
    contains any of the names in the provided list.
    """
    i = 0
    delete_flag = False
    while i < len(lines):
        line = lines[i]
        if "def" in line or "@" in line:
            delete_flag = False

        if delete_flag:
            del lines[i]
        else:
            if "def" in line and (any(word in line for word in names)):
                delete_flag = True
                del lines[i]
                if "@" in lines[i - 1]:
                    del lines[i - 1]
                    i -= 1
            else:
                i += 1
    return lines


def add_correct_docstring_and_correct_the_init(content: str):
    lines = content.splitlines()

    cls_doc = inspect.getdoc(Client)
    indented_cls_doc = textwrap.indent(f'"""\n{cls_doc}\n"""', "    ")

    init_method = Client.__init__
    init_sig = inspect.signature(init_method)
    init_doc = inspect.getdoc(init_method)
    indented_init_doc = textwrap.indent(f'"""\n{init_doc}\n"""', " " * 8)

    params = list(init_sig.parameters.values())
    if params and params[0].name == "self":
        params = params[1:]

    pos_params = [
        p
        for p in params
        if p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]
    kwonly_params = [p for p in params if p.kind is inspect.Parameter.KEYWORD_ONLY]
    if kwonly_params:
        param_parts = (
            [str(p) for p in pos_params] + ["*"] + [str(p) for p in kwonly_params]
        )
    else:
        param_parts = [str(p) for p in pos_params]

    # turn Optional[Type] into Type | None
    opt_re = re.compile(r"\b(?:Optional|Option)\[(.+)]", re.DOTALL)
    param_parts = [
        opt_re.sub(lambda m: f"{m.group(1)} | None", s)  # Optional[T] → T | None
        for s in param_parts
    ]

    param_str = ", ".join(param_parts)

    return_str = (
        "None"
        if init_sig.return_annotation is inspect.Signature.empty
        else init_sig.return_annotation
    )

    i = 0
    while i < len(lines):
        if "class" in lines[i]:
            lines.insert(i + 1, indented_cls_doc)
            break
        i += 1

    i = 0
    while i < len(lines):
        if "def __init__" in lines[i]:
            break
        i += 1

    delete_method_and_docstring(["__init__"], lines)

    lines.insert(i - 1, indented_init_doc)
    init_params = f", {param_str}" if param_str else ""
    lines.insert(i - 1, f"    def __init__(self{init_params}) -> {return_str}:")

    return "\n".join(lines)


def correct_sync_interface(content: str):
    """
    Correct the sync interface in the gRPC service definitions.

    These lines are sensitive to the order of the lines in the file.
    """

    content = f"# fmt: off\n# mypy: ignore-errors\n# ruff: noqa\n{content}"

    # Remove all stream, orderflow, and subscribe methods
    lines = content.splitlines()
    delete_method_and_docstring(["stream", "orderflow", "subscribe", "connect"], lines)
    content = "\n".join(lines)

    # Replace the async method definitions with sync method definitions
    content = content.replace("async def", "def")
    content = content.replace("await ", "")
    content = content.replace("AsyncClient", "Client")

    return content


def main(content: str) -> str:
    content = correct_sync_interface(content)
    content = add_correct_docstring_and_correct_the_init(content)

    return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process gRPC service definitions")
    parser.add_argument(
        "--file_path",
        type=str,
        help="Path to the async_client.pyi file",
    )
    args = parser.parse_args()

    with open(args.file_path, "r") as f:
        content = f.read()
    content = main(content)
    with open(args.file_path, "w") as f:
        f.write(content)
