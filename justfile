check-format:
    uv run ruff format --check

check-version:
    ./scripts/check_version.sh

format:
    uv run ruff format

lint:
    uv run ruff check

typecheck:
    uv run pyright

update-schema:
    ./scripts/update_schema.sh