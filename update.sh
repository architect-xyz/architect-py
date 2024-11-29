# architect-gql schema > ../architect-py/schema.graphql
poetry run ariadne-codegen --config ariadne-codegen.toml
python generate_protocol.py > architect_py/protocol/client_protocol.py

: <<'END'
to run the test, must have a pytest.env file with the following content:

HOST=staging.architect.co
API_KEY=...
API_SECRET=...
ACCOUNT=...
END

export $(cat pytest.env | xargs)
pytest tests/*