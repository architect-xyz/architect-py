import pytest

from architect_py.async_client import AsyncClient
from architect_py.scalars import TradableProduct


@pytest.mark.asyncio
async def test_grpc(async_client: AsyncClient, front_ES_future: str):

    endpoint = "binance.marketdata.architect.co"
    endpoint = "bybit.marketdata.architect.co"
    endpoint = "binance-futures-usd-m.marketdata.architect.co"
    endpoint = "cme.marketdata.architect.co"

    tp = TradableProduct(front_ES_future, "USD")
    snapshot = await async_client.grpc_client.l2_book_snapshot("CME", tp)
    assert snapshot is not None

    i = 0
    async for update in async_client.grpc_client.stream_l1_books([front_ES_future]):
        assert update is not None
        if i == 100:
            break
        i += 1
    return True
