import ast
import re
import sys
from collections import defaultdict


def extract_sections(source_lines):
    """
    Look for section header blocks that look like:

        # ------------------------------------------------------------
        # Some Section Name
        # ------------------------------------------------------------

    Returns a list of tuples (section_name, lineno) where lineno is the
    line number (1-indexed) of the section title.
    """
    sections = []
    # Regex for a dashed line
    dashed_re = re.compile(r"^\s*#\s*-{10,}\s*$")
    # Regex for a section title line (should start with "#")
    title_re = re.compile(r"^\s*#\s*(.+\S)\s*$")

    i = 0
    while i < len(source_lines):
        if dashed_re.match(source_lines[i]):
            if i + 1 < len(source_lines) and title_re.match(source_lines[i + 1]):
                groups = title_re.match(source_lines[i + 1])
                if groups is not None:
                    section_name = groups.group(1).strip()
                else:
                    continue
                # Check that the next line (i+2) is also a dashed line
                if i + 2 < len(source_lines) and dashed_re.match(source_lines[i + 2]):
                    sections.append(
                        (section_name, i + 2)
                    )  # record line number of closing dashed line, or i+1 as desired
                    i += 3
                    continue
        i += 1
    return sections


def find_section_for_lineno(lineno, sections):
    """
    Given a line number (1-indexed) and a list of sections (name, lineno),
    return the name of the last section that occurs before the given line number.
    If none found, return "No Section".
    """
    candidate = None
    for name, sec_line in sections:
        if sec_line < lineno:
            candidate = name
        else:
            break
    return candidate if candidate is not None else "No Section"


def get_asyncclient_methods(filename):
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()
    source_lines = source.splitlines()
    # Extract sections from source lines
    sections = extract_sections(source_lines)

    tree = ast.parse(source, filename)
    methods = []  # list of tuples (section, func_name, doc_summary, lineno)

    # Walk the AST to find the class AsyncClient
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "AsyncClient":
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Exclude typing overloads
                    is_fn_overload = False
                    for decorator in item.decorator_list:
                        decorator_name = ""
                        if isinstance(decorator, ast.Call):
                            decorator_name = (
                                decorator.func.attr
                                if isinstance(decorator.func, ast.Attribute)
                                else getattr(decorator.func, "id", "")
                            )
                        else:
                            decorator_name = (
                                decorator.attr
                                if isinstance(decorator, ast.Attribute)
                                else decorator.id
                                if isinstance(decorator, ast.Name)
                                else ""
                            )
                        if decorator_name == "overload":
                            is_fn_overload = True

                    if is_fn_overload:
                        continue

                    # Get docstring using ast.get_docstring
                    doc = ast.get_docstring(item)
                    if doc:
                        # Extract the first non-empty line from the docstring
                        first_line = next(
                            (line.strip() for line in doc.splitlines() if line.strip()),
                            "",
                        )
                    else:
                        first_line = ""
                    section = find_section_for_lineno(item.lineno, sections)
                    methods.append((section, item.name, first_line, item.lineno))
            break  # found our class, stop searching
    return methods


def group_methods_by_section(methods):
    grouped = defaultdict(list)
    for section, name, summary, lineno in methods:
        grouped[section].append((name, summary, lineno))
    # Optionally sort sections by the lowest lineno
    return dict(grouped)


def main(filename):
    methods = get_asyncclient_methods(filename)
    grouped = group_methods_by_section(methods)
    # For predictable order, sort sections by the minimum line number among its methods
    sorted_sections = sorted(
        grouped.items(),
        key=lambda item: min(m[2] for m in grouped[item[0]]) if grouped[item[0]] else 0,
    )
    # Alternatively, sort by section name alphabetically:
    # sorted_sections = sorted(grouped.items())
    print("# Client Methods")
    for section, funcs in sorted_sections:
        emoji = emoji_dict.get(section, "")
        if emoji == "":
            raise ValueError(f'Section "{section}" does not have an emoji.')
        print(f"### {emoji} {section}")
        print()
        # Sort functions by their line number
        for name, summary, lineno in sorted(funcs, key=lambda x: x[2]):
            # Exclude private methods
            if name.startswith("_"):
                continue
            # Only output if summary is non-empty
            if summary:
                if summary.startswith("@deprecated"):
                    continue
                print(f"- **`{name}`**: {summary}")
            else:
                print(f"- **`{name}`**")
        print("\n---\n")


emoji_dict: dict[str, str] = {
    "Initialization and configuration": "🚀",
    "Symbology": "🔍",
    "Portfolio management": "💹",
    "Order management": "📝",
    "Order entry": "📣",
    "Marketdata": "🧮",
    "Options": "🎯",
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_methods.py <filename>")
    else:
        main(sys.argv[1])
