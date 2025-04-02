#!/bin/bash
set -euo pipefail

ARCHITECT_FOLDER_PATH="../architect"
if [[ ! -d "$ARCHITECT_FOLDER_PATH" ]]; then
    printf "Error: Directory $ARCHITECT_FOLDER_PATH does not exist."
    printf "Please update the ARCHITECT_FOLDER_PATH path in the update script."
    exit 1
fi

# this script is used to update the generated code in the project
# for both graphql and grpc

# -----------------------------
# Check graphql schema for changes
# -----------------------------
if ! cmp -s schema.graphql $ARCHITECT_FOLDER_PATH/gql/schema.graphql; then
    printf "Schema has changed. Updating schema (y/n)?"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp $ARCHITECT_FOLDER_PATH/gql/schema.graphql schema.graphql
        printf "Schema updated.\n"
    fi
fi


# -----------------------------
# GRPC codegen
# -----------------------------

GRPC_CLIENT_DIR="architect_py/grpc_client"
PROCESSED_DIR="processed_schemas"


# Preprocess the grpc types
printf "\nPreprocessing GRPC types into jsons\n"
rm -rf "${PROCESSED_DIR:?}"/*
find "$GRPC_CLIENT_DIR" -mindepth 1 -type d -exec rm -rf {} +
python preprocess_grpc_types.py --architect_dir "$ARCHITECT_FOLDER_PATH" --output_dir "$PROCESSED_DIR"

mkdir -p "$GRPC_CLIENT_DIR"

if [[ ! -d "$PROCESSED_DIR" ]]; then
    printf "Error: Directory $PROCESSED_DIR does not exist."
    exit 1
fi


printf "\nGenerating GRPC client code\n"

datamodel-codegen \
    --input "$PROCESSED_DIR" \
    --output "$GRPC_CLIENT_DIR" \
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
# do not use --reuse-model flag as it will not generate the correct code, even with template modification


python postprocess_grpc_file.py --file_path "$GRPC_CLIENT_DIR" --json_folder "$PROCESSED_DIR"


# the __init__.py file is overwritten by datamodel-code-generator so we need to re-import the files
echo "# datamodel-code-generator stomps on the __init__.py file so we import from adjacent file" > architect_py/grpc_client/__init__.py
echo "from .grpc_client import *" >> architect_py/grpc_client/__init__.py


# -----------------------------
# ariadne codegen
# -----------------------------
printf "\n\nGenerating GraphQL code\n"
poetry run ariadne-codegen --config ariadne-codegen.toml > /dev/null

printf "\nGenerating client protocol\n"
python generate_sync_client_protocol.py > architect_py/client_protocol.py

# ------------------------------
# Format code
# ------------------------------

black -q "$GRPC_CLIENT_DIR"

# -----------------------------
# Update README
# -----------------------------

python generate_functionsmd.py architect_py/async_client.py > FUNCTIONS.md


# -----------------------------
# Run black
# -----------------------------
black -q .


# -----------------------------
# Version check
# -----------------------------
VERSION_FILE="version"

if [ -f "$VERSION_FILE" ]; then
    printf "\nCurrent version: "
    cat "$VERSION_FILE"
else
    printf "Version file not found: $VERSION_FILE"
    exit 1
fi

printf "\n\nHave you updated the version in $VERSION_FILE?"
