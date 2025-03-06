#!/bin/bash
# this script is used to update the generated code in the project

set -euo pipefail

# Check schema
if ! cmp -s schema.graphql ../architect/gql/schema.graphql; then
    printf "Schema has changed. Updating schema (y/n)?"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp ../architect/gql/schema.graphql schema.graphql
        printf "Schema updated.\n"
    else
        printf "Update skipped.\n"
    fi
else
    printf "Schema matches backend.\n"
fi


# GRPC codegen
GRPC_CLIENT_DIR="architect_py/grpc_client"
PROCESSED_DIR="processed_schemas"

printf "\nRegenerating gRPC models"
rm -rf "${PROCESSED_DIR:?}"/*
find "$GRPC_CLIENT_DIR" -mindepth 1 -type d -exec rm -rf {} +
python preprocess_grpc_types.py --output_dir "$PROCESSED_DIR"

mkdir -p "$GRPC_CLIENT_DIR"

if [[ ! -d "$PROCESSED_DIR" ]]; then
    printf "Error: Directory $PROCESSED_DIR does not exist."
    exit 1
fi

post_process_file() {
    local filepath="$1"
    local folder service_name filename out_dir output_file

    folder=$(dirname "$filepath")
    service_name=$(basename "$folder")
    filename=$(basename "$filepath" .json)
    out_dir="${GRPC_CLIENT_DIR}/${service_name}"
    output_file="${out_dir}/${filename}.py"

    python postprocess_grpc_file.py --file_path "$output_file" --json_folder "$folder"
}

export -f post_process_file
export GRPC_CLIENT_DIR


# Capture list of JSON files to process
json_files=()
while IFS= read -r file; do
    json_files+=("$file")
done < <(find "$PROCESSED_DIR" -mindepth 2 -name '*.json')

datamodel-codegen \
    --input "$PROCESSED_DIR" \
    --output "$GRPC_CLIENT_DIR" \
    --input-file-type jsonschema \
    --output-model-type msgspec.Struct \
    --custom-template-dir templates \
    --use-title-as-name \
    --enum-field-as-literal one \
    --use-subclass-enum \
    --use-field-description \
    --use-schema-description \
    --disable-timestamp

printf "\nPost processing files\n"
for file in "${json_files[@]}"; do
    post_process_file "$file"
done

cp -r templates/grpc_client.py architect_py/grpc_client/__init__.py


# ariadne codegen
printf "\n\nGenerating GraphQL code\n"
poetry run ariadne-codegen --config ariadne-codegen.toml

printf "\nGenerating client protocol"
python generate_sync_client_protocol.py > architect_py/client_protocol.py

# Version check
VERSION_FILE="version"

if [ -f "$VERSION_FILE" ]; then
    printf "\nCurrent version: "
    cat "$VERSION_FILE"
else
    printf "Version file not found: $VERSION_FILE"
    exit 1
fi

printf "\n\nHave you updated the version in $VERSION_FILE?"
