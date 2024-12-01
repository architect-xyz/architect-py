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
