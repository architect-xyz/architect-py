# architect-gql schema > ../architect-py/schema.graphql
poetry run ariadne-codegen --config ariadne-codegen.toml
python generate_protocol.py > architect_py/protocol/client_protocol.py


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