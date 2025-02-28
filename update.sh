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


GRPC_MODELS_DIR="architect_py/grpc_models"
PROCESSED_DIR="processed_schemas"

echo "\nGenerating gRPC models"
python preprocess_grpc_types.py  --output_dir $PROCESSED_DIR


mkdir -p "$GRPC_MODELS_DIR"
touch "$GRPC_MODELS_DIR/__init__.py"

find "${PROCESSED_DIR}" -name "*.json" | while read -r filepath; do
    service_dir=$(dirname "$filepath")
    service_name=$(basename "$service_dir")
    out_dir="${GRPC_MODELS_DIR}/${service_name}"
    
    mkdir -p "${out_dir}"
    
    datamodel-codegen \
        --input "$filepath" \
        --output "${out_dir}/$(basename "$filepath" .json).py" \
        --input-file-type jsonschema \
        --output-model-type msgspec.Struct \
        --use-title-as-name \
        --enum-field-as-literal one \
        --use-subclass-enum \
        --custom-template-dir templates \
        --disable-timestamp
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
