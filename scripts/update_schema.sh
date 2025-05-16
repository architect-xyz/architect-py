#!/bin/bash
set -euo pipefail

BASE_DIR=$(dirname "$(cd "$(dirname "$0")" && pwd)")
# rm -rf "$BASE_DIR/.venv"

# --------------------------------
# Find the architect monorepo root 
# by looking for cargo magic.
# --------------------------------

CANDIDATES=("../.." "../architect")
for location in "${CANDIDATES[@]}"; do
    if [[ -f "$location/Cargo.toml" ]] && grep -q 'magic = "architect"' "$location/Cargo.toml"; then
        ARCHITECT_ROOT="$location"
        break
    fi
done

if [[ ! -d "$ARCHITECT_ROOT" ]]; then
    echo "Error: could not find architect monorepo root."
    exit 1
fi

# --------------------------------
# Check graphql schema for changes
# --------------------------------

if ! cmp -s schema.graphql $ARCHITECT_ROOT/gql/schema.graphql; then
    printf "GraphQL schema has changed. Update schema (y/n)? "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp $ARCHITECT_ROOT/gql/schema.graphql schema.graphql
        printf "GraphQL schema updated.\n"
    fi
fi

# --------------------------------
# Generate GraphQL client 
# --------------------------------

printf "Generating GraphQL client...\n"
uv run ariadne-codegen --config ariadne-codegen.toml > /dev/null


# --------------------------------
# Generate gRPC client
# --------------------------------

SCHEMAS_DIR="architect_py/grpc/schemas"
MODELS_DIR="architect_py/grpc/models"

# Preprocess the gRPC JSON schema
printf "\nPre-processing gRPC schema...\n"
rm -rf "${SCHEMAS_DIR:?}"/*
uv run scripts/preprocess_grpc_schema.py \
    --schema "$ARCHITECT_ROOT/api/schema.json" \
    --output-dir "$SCHEMAS_DIR"

if [[ ! -d "$SCHEMAS_DIR" ]]; then
    printf "Error: directory $SCHEMAS_DIR does not exist."
    exit 1
fi

printf "Generating gRPC models...\n"
uv run datamodel-codegen \
    --input "$SCHEMAS_DIR" \
    --output "$MODELS_DIR" \
    --input-file-type jsonschema \
    --output-model-type msgspec.Struct \
    --custom-template-dir templates \
    --use-title-as-name \
    --output-datetime-class datetime \
    --enum-field-as-literal one \
    --use-subclass-enum \
    --use-field-description \
    --use-schema-description \
    --disable-timestamp
# NB: do not use --reuse-model flag as it will not generate the 
# correct code, even with template modification

# suppress ./architect_py/__init__.py for the duration of post-processing;
# otherwise imports will fail since their referents will not exist
mv ./architect_py/__init__.py ./architect_py/__init__.py.bak
touch ./architect_py/__init__.py
export PYTHONPATH="$BASE_DIR"
printf "PYTHONPATH: $PYTHONPATH\n"

printf "Post-processing gRPC client code...\n"
uv run scripts/postprocess_grpc.py \
    --file_path "$MODELS_DIR" \
    --json_folder "$SCHEMAS_DIR"


# restore ./architect_py/__init__.py
mv ./architect_py/__init__.py.bak ./architect_py/__init__.py

printf "\nFormatting code...\n"
# format generated code 
uv run ruff format ./architect_py/grpc/models

# Update FUNCTIONS.md
uv run scripts/generate_functions_md.py architect_py/async_client.py \
    > FUNCTIONS.md

printf "\nGenerating sync client interface from async...\n"
uv run stubgen architect_py/async_client.py -o temp --include-docstrings
uv run scripts/correct_sync_interface.py --file_path temp/architect_py/async_client.pyi
mv temp/architect_py/async_client.pyi architect_py/client.pyi
rm -rf temp
uv run ruff format

uv run ruff check . --select F401 --fix --isolated