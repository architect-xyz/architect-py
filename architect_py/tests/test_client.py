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
    jwt = await async_client.graphql_client.create_jwt()
    assert jwt is not None, "jwt should not be None"


def test_sync_client(sync_client: Client):
    sync_result = sync_client.search_symbols(execution_venue="CME", search_string="ES")
    assert len(sync_result) > 5

    ES_future = sync_result[0]

    sync_result = sync_client.search_symbols(ES_future)
    assert sync_result is not None
