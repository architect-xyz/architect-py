# this script is used to update the generated code in the project


# check sdchema
if ! cmp -s schema.graphql ../architect/gql/schema.graphql; then
    echo "Schema has changed. Updating schema (y/n)?"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp ../architect/gql/schema.graphql schema.graphql
        echo "Schema updated.\n"
    else
        echo "Update skipped.\n"
    fi
else
    echo "Schema matches backend.\n"
fi


# ariadne codegen
poetry run ariadne-codegen --config ariadne-codegen.toml


# GRPC codegen
echo "\nGenerating client protocol"
python generate_sync_client_protocol.py > architect_py/protocol/client_protocol.py


GRPC_CLIENT_DIR="architect_py/grpc_client"
PROCESSED_DIR="processed_schemas"

echo "\nGenerating gRPC models"
python preprocess_grpc_types.py  --output_dir $PROCESSED_DIR


mkdir -p "$GRPC_CLIENT_DIR"

# cp templates/grpc_template.py "$GRPC_CLIENT_DIR"/__init__.py

if [[ ! -d "$PROCESSED_DIR" ]]; then
    echo "Error: Directory $PROCESSED_DIR does not exist."
    exit 1
fi

for folder in "$PROCESSED_DIR"/*/; do
    # Check if it's a directory
    if [[ -d "$folder" ]]; then
        service_name=$(basename "$folder")
        echo "Processing folder: $service_name"
        out_dir="${GRPC_CLIENT_DIR}/${service_name}"

        mkdir -p "${out_dir}"

        for filepath in "$folder"/*.json; do
            echo "\tProcessing file: $filepath"

            filename=$(basename "$filepath" .json)
            output_file="${out_dir}/$filename.py"

            datamodel-codegen
                --input "$filepath" \
                --output "$output_file" \
                --input-file-type jsonschema \
                --output-model-type msgspec.Struct \
                --use-title-as-name \
                --enum-field-as-literal one \
                --use-subclass-enum \
                --field-include-all-keys \
                --custom-template-dir templates \
                --disable-timestamp

            python postprocess_grpc_types.py  --file_path $output_file

        done
    fi
done


# version check
VERSION_FILE="version"

if [ -f "$VERSION_FILE" ]; then
    echo "\nCurrent version:"
    cat "$VERSION_FILE"
else
    echo "Version file not found: $VERSION_FILE"
    exit 1
fi

echo "\n\nHave you updated the version in $VERSION_FILE?"
