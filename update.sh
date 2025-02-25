# architect-gql schema > ../architect-py/schema.graphql
poetry run ariadne-codegen --config ariadne-codegen.toml

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
        --collapse-root-models \
        --use-title-as-name \
        --use-union-operator \
        # --reuse-model
        # --strip-default-none \
done

VERSION_FILE="version"

# Extract the current version from the file
if [ -f "$VERSION_FILE" ]; then
    echo "\nCurrent version:"
    cat "$VERSION_FILE"
else
    echo "Version file not found: $VERSION_FILE"
    exit 1
fi

echo "\n\nHave you updated the version in $VERSION_FILE?"
