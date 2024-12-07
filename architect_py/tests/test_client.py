import pytest
from architect_py.async_client import AsyncClient


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
