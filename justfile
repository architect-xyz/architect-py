check-format:
    uv run ruff format --check

check-version:
    ./scripts/check_version.sh

fix:
    uv run ruff check --fix

format:
    uv run ruff format

lint:
    uv run ruff check

test:
    uv run pytest --cov

typecheck:
    uv run pyright

update-schema:
    ./scripts/update_schema.sh