#!/usr/bin/env python3
"""
Strips unused object-types, enums, inputs, interfaces and unions
from a GraphQL schema, keeping only what is referenced by the operations
in queries.graphql.  Any root operation (mutation / subscription) whose
type definition is pruned away is also removed from the `schema { … }`
block.

As a part of the update_schema.py, this script is OPTIONAL but a good idea

Usage:
    python prune_schema.py full_schema.graphql queries.graphql schema.graphql
"""

import sys
from pathlib import Path
from typing import Set, cast

from graphql import (
    ListTypeNode,
    NonNullTypeNode,
    TypeInfo,
    build_ast_schema,
    get_named_type,
    parse,
    print_ast,
    visit,
)
from graphql.language import (
    DocumentNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    NamedTypeNode,
    ObjectTypeDefinitionNode,
    SchemaDefinitionNode,
    UnionTypeDefinitionNode,
    Visitor,
)
from graphql.utilities import TypeInfoVisitor

SDL_KINDS_TO_PRUNE = (
    ObjectTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    UnionTypeDefinitionNode,
)


# ───────────────────────── helpers ──────────────────────────
def _named(node) -> NamedTypeNode:
    """Strip List/NonNull wrappers and return the leaf NamedTypeNode."""
    while isinstance(node, (ListTypeNode, NonNullTypeNode)):
        node = node.type
    return cast(NamedTypeNode, node)


def fix_docstring_indentation(sdl: str) -> str:
    """Indent docstring bodies by two spaces so they remain readable."""
    lines = sdl.splitlines()
    in_doc = False
    for i, line in enumerate(lines):
        if line.startswith('"""'):
            in_doc = not in_doc
        elif in_doc:
            lines[i] = f"  {line}"
    return "\n".join(lines)


# ────────────── reachability (what types are used) ──────────────
def _reachable_types(schema_sdl: str, queries_sdl: str) -> Set[str]:
    schema_ast = parse(schema_sdl)
    schema = build_ast_schema(schema_ast)

    used: Set[str] = set()
    tinfo = TypeInfo(schema)

    class _Recorder(Visitor):
        def enter(self, *_):
            if typ := tinfo.get_type() or tinfo.get_input_type():
                used.add(get_named_type(typ).name)
            if (parent := tinfo.get_parent_type()) is not None:
                used.add(parent.name)

    visit(parse(queries_sdl), TypeInfoVisitor(tinfo, _Recorder()))

    used.update(
        x
        for x in (
            "Int",
            "Float",
            "String",
            "Boolean",
            "ID",
            schema.query_type and schema.query_type.name,
            schema.mutation_type and schema.mutation_type.name,
            schema.subscription_type and schema.subscription_type.name,
        )
        if x
    )
    return used


# ─────────────────────── pruning ──────────────────────────────
def _prune_ast(schema_ast: DocumentNode, keep: Set[str]) -> DocumentNode:
    # Pass 1 – drop defs never referenced
    schema_ast.definitions = tuple(
        d
        for d in schema_ast.definitions
        if not (isinstance(d, SDL_KINDS_TO_PRUNE) and d.name.value not in keep)
    )

    # Pass 2 – repeatedly:
    #   • remove fields whose types were pruned
    #   • drop container types left with zero fields
    changed = True
    while changed:
        changed = False

        new_defs = []
        for d in schema_ast.definitions:
            if isinstance(d, ObjectTypeDefinitionNode):
                kept_fields = tuple(
                    f for f in (d.fields or []) if _named(f.type).name.value in keep
                )
                if len(kept_fields) != len(d.fields or ()):
                    changed = True
                if kept_fields:
                    new_defs.append(
                        d.__class__(  # recreate node with surviving fields
                            name=d.name,
                            interfaces=d.interfaces,
                            directives=d.directives,
                            fields=kept_fields,
                            description=getattr(d, "description", None),
                            loc=d.loc,
                        )
                    )
                else:
                    changed = True  # container emptied → drop it
            else:
                new_defs.append(d)
        schema_ast.definitions = tuple(new_defs)

    # Pass 3 – trim mutation/subscription in the schema block
    live_names = {
        d.name.value
        for d in schema_ast.definitions
        if isinstance(d, SDL_KINDS_TO_PRUNE)
    }
    for defn in schema_ast.definitions:
        if isinstance(defn, SchemaDefinitionNode):
            defn.operation_types = tuple(
                op
                for op in defn.operation_types
                if op.operation == "query" or op.type.name.value in live_names
            )

    return schema_ast


# ─────────────────────── main entry-point ─────────────────────
def main(schema_path: str, queries_path: str, out_path: str | None = None) -> None:
    schema_src = Path(schema_path).read_text()
    query_src = Path(queries_path).read_text()

    keep = _reachable_types(schema_src, query_src)
    pruned_ast = _prune_ast(parse(schema_src), keep)

    sdl_out = "\n\n".join(print_ast(defn).strip() for defn in pruned_ast.definitions)
    sdl_out = fix_docstring_indentation(sdl_out)

    if out_path:
        Path(out_path).write_text(sdl_out)
    else:
        print(sdl_out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write(
            "USAGE: uv run prune_schema.py schema.graphql queries.graphql "
            "[pruned_schema.graphql]\n"
        )
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
