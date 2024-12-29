import os

import pytest
from architect_py.async_client import AsyncClient
from architect_py.client import Client


@pytest.mark.asyncio
async def test_client_init():
    with pytest.raises(ValueError):
        client = AsyncClient(host="localhost", port=4567, api_key=" ", api_secret=" ")
    with pytest.raises(ValueError):
        client = AsyncClient(
            host="localhost", port=4567, api_key="something", api_secret='"alskjdf"'
        )


@pytest.mark.asyncio
async def test_client_jwt(async_client: AsyncClient):
    jwt = await async_client.create_jwt()
    assert jwt is not None, "jwt should not be None"


def test_sync_client():
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
