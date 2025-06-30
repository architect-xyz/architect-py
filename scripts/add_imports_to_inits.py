#!/usr/bin/env python3
import argparse
import ast
from pathlib import Path


def collect_definitions(py_file: Path) -> list[str]:
    """
    Parse the given .py file with ast and return a list of:
      - all top-level class names
      - all top-level names assigned via Annotated[...]
      - all top-level names assigned to a bare type alias (e.g. SomeAlias = str)
    """
    src = py_file.read_text()
    tree = ast.parse(src, filename=str(py_file))
    names: list[str] = []

    for node in tree.body:
        # 1) class definitions
        if isinstance(node, ast.ClassDef):
            names.append(node.name)

        # 2) Annotated aliases: e.g. OrderId = Annotated[...]
        elif (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            target = node.targets[0].id
            val = node.value
            # Annotated[...]?
            if (
                isinstance(val, ast.Subscript)
                and isinstance(val.value, ast.Name)
                and val.value.id == "Annotated"
            ):
                names.append(target)
            # simple alias: = SomeType (e.g. = str, = int, = UUID, etc.)
            elif isinstance(val, ast.Name):
                names.append(target)

    return names


def get_version(py_file: Path) -> str:
    prev = py_file.read_text()
    prev_lines = prev.splitlines()
    for line in prev_lines:
        if line.startswith("__version__"):
            return line
    raise ValueError("Could not find __version__ in the existing __init__.py file.")


def main(architect_path: Path, output: Path):
    """
    Generate static imports + __all__ (including definitions.py) for grpc/models

    This only works for the main request/response classes that the file is named after.
    The definitions.py file is not included for the grpc __init__ because it causes circular imports.
    """

    models_root = architect_path / "grpc" / "models"

    version = get_version(output)
    import_lines: list[str] = [
        "# ruff: noqa:I001\n",
        version,
        "",
        "from .utils.nearest_tick import TickRoundMethod",
        "from .async_client import AsyncClient",
        "from .client import Client",
        "from .common_types import OrderDir, TradableProduct, TimeInForce, Venue",
    ]

    all_names: list[str] = [
        "TickRoundMethod",
        "AsyncClient",
        "Client",
        "OrderDir",
        "TradableProduct",
        "TimeInForce",
        "Venue",
    ]

    # 1) definitions.py
    defs = models_root / "definitions.py"
    if defs.exists():
        defs_names = collect_definitions(defs)
        if defs_names:
            import_lines.append(
                f"from .grpc.models.definitions import {', '.join(defs_names)}"
            )
            all_names.extend(defs_names)

    # 2) sub-packages under models/

    model_lines: list[str] = []
    model_all: list[str] = []
    for sub in sorted(models_root.iterdir()):
        if not sub.is_dir() or not (sub / "__init__.py").exists():
            continue

        pkg = f"grpc.models.{sub.name}"

        for module_path in sorted(sub.iterdir()):
            if module_path.suffix != ".py" or module_path.name.startswith("_"):
                continue
            mod = module_path.stem

            import_lines.append(f"from .{pkg}.{mod} import {mod}")
            all_names.append(mod)

            model_lines.append(f"from .{sub.name}.{mod} import {mod}")
            model_all.append(mod)

    unique = sorted(set(model_all))
    model_lines.append("")

    model_lines_all_list = ", ".join(f'"{n}"' for n in model_all)
    model_lines.append(f"__all__ = [{model_lines_all_list}]")
    model_lines.append("")

    (models_root / "__init__.py").write_text("\n".join(model_lines))

    # 3) write __all__
    unique = sorted(set(all_names))
    import_lines.append("")  # blank line

    import_lines_all_list = ", ".join(f'"{n}"' for n in unique)
    import_lines.append(f"__all__ = [{import_lines_all_list}]")

    import_lines.append("")  # blank line

    output.write_text("\n".join(import_lines))


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Generate static imports + __all__ (including definitions.py) for grpc/models"
    )
    p.add_argument(
        "--architect-path",
        type=Path,
        default=Path("architect_py"),
        help="Path to your top-level architect_py folder",
    )
    args = p.parse_args()

    out = args.architect_path / "__init__.py"
    main(args.architect_path, out)
