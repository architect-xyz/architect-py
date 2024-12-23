import os

import pytest_asyncio
from architect_py.client import Client
from architect_py.async_client import AsyncClient
from dotenv import load_dotenv


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

    # if ACCOUNT is not None and "PAPER" in ACCOUNT:
    #     PORT = 6789
    # else:
    #     PORT = 4567

    async with AsyncClient(
        host=host, port=port, api_key=api_key, api_secret=api_secret
    ) as client:
        yield client


def test_sync_client(async_client: AsyncClient):
    # this test should not have any market orders or any other side effects

    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")

    client = Client(host=host, api_key=api_key, api_secret=api_secret, port=port)

    sync_result = client.search_markets(max_results=5, venue="CME")
    assert len(sync_result) == 5

    sync_result = client.search_markets(glob="ES*", venue="CME")
    assert sync_result is not None

    ES_future = sync_result[0]

    sync_result = client.get_market(ES_future.id)

    assert sync_result is not None
