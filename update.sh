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

process_file() {
    local filepath="$1"
    local folder service_name filename out_dir output_file
    folder=$(dirname "$filepath")
    service_name=$(basename "$folder")
    filename=$(basename "$filepath" .json)
    out_dir="${GRPC_CLIENT_DIR}/${service_name}"
    mkdir -p "${out_dir}"

    output_file="${out_dir}/${filename}.py"
    printf "Processing folder: ${service_name}, file: ${filepath}"
    datamodel-codegen \
        --input "$folder" \
        --output "$out_dir" \
        --input-file-type jsonschema \
        --output-model-type msgspec.Struct \
        --use-title-as-name \
        --enum-field-as-literal one \
        --use-subclass-enum \
        --use-field-description \
        --use-schema-description \
        --custom-template-dir templates \
        --disable-timestamp
}

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

export -f process_file
export -f post_process_file
export GRPC_CLIENT_DIR

if command -v nproc >/dev/null 2>&1; then
    NUM_JOBS=$(nproc)
else
    NUM_JOBS=$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)
fi

# Capture list of JSON files to process
json_files=()
while IFS= read -r file; do
    json_files+=("$file")
done < <(find "$PROCESSED_DIR" -mindepth 2 -name '*.json')


# Process JSON files either using GNU parallel or a normal for loop.
if command -v parallel >/dev/null 2>&1; then
    printf "\n\e[31mGNU parallel found, processing files in parallel.\e[0m\n\n"

    printf "%s\n" "${json_files[@]}" | parallel --bar -j "$NUM_JOBS" process_file {}
    printf "%s\n" "${json_files[@]}" | parallel --bar -j "$NUM_JOBS" post_process_file {}
else
    printf "\n\e[31mGNU parallel not found, processing files sequentially.\e[0m\n\n\n"
    for file in "${json_files[@]}"; do
        process_file "$file"
    done
    for file in "${json_files[@]}"; do
        post_process_file "$file"
    done
fi

printf "\n\nGenerating GraphQL code\n"

# ariadne codegen
poetry run ariadne-codegen --config ariadne-codegen.toml

printf "\nGenerating client protocol"
python generate_sync_client_protocol.py > architect_py/protocol/client_protocol.py

# Version check
VERSION_FILE="version"

if [ -f "$VERSION_FILE" ]; then
    printf "\nCurrent version:"
    cat "$VERSION_FILE"
else
    printf "Version file not found: $VERSION_FILE"
    exit 1
fi

printf "\n\nHave you updated the version in $VERSION_FILE?"
