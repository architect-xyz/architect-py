# architect-gql schema > ../architect-py/schema.graphql
poetry run ariadne-codegen --config ariadne-codegen.toml
python generate_protocol.py > architect_py/protocol/client_protocol.py

export $(cat pytest.env | xargs)
pytest tests/*