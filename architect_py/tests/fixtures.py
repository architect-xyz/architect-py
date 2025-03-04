import os

import pytest
import pytest_asyncio
from architect_py.client import Client
from architect_py.async_client import AsyncClient
from dotenv import load_dotenv

from architect_py.async_client import AsyncClient


def is_truthy(value: str | None) -> bool:
    return value is not None and value.lower() in ("1", "true", "yes")


@pytest_asyncio.fixture
async def async_client():
    load_dotenv()

    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    # test_account = os.getenv("ARCHITECT_TEST_ACCOUNT")
    dangerous_allow_app_architect_co = os.getenv("DANGEROUS_ALLOW_APP_ARCHITECT_CO")

    if host == "app.architect.co" and not is_truthy(dangerous_allow_app_architect_co):
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )
    if api_key is None or api_secret is None:
        raise ValueError(
            "You must set ARCHITECT_API_KEY and ARCHITECT_API_SECRET to run tests"
        )

    return AsyncClient(host=host, port=port, api_key=api_key, api_secret=api_secret)


@pytest.fixture
def sync_client():
    load_dotenv()
    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")

    dangerous_allow_app_architect_co = os.getenv("DANGEROUS_ALLOW_APP_ARCHITECT_CO")

    if host == "app.architect.co" and not is_truthy(dangerous_allow_app_architect_co):
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )
    if api_key is None or api_secret is None:
        raise ValueError(
            "You must set ARCHITECT_API_KEY and ARCHITECT_API_SECRET to run tests"
        )
    return Client(host=host, api_key=api_key, api_secret=api_secret, port=port)
