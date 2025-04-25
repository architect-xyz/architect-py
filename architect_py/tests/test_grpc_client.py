import pytest

from architect_py.async_client import AsyncClient
from architect_py.common_types import TradableProduct


@pytest.mark.asyncio
async def test_grpc(async_client: AsyncClient, front_ES_future: str):
    # endpoint = "binance.marketdata.architect.co"
    # endpoint = "bybit.marketdata.architect.co"
    # endpoint = "binance-futures-usd-m.marketdata.architect.co"
    # endpoint = "cme.marketdata.architect.co"

    tp = TradableProduct(front_ES_future, "USD")
    snapshot = await async_client.get_l2_book_snapshot(tp, "CME")
    assert snapshot is not None

    snapshot = await async_client.get_l1_book_snapshot(tp, "CME")
    assert snapshot is not None

    i = 0
    async for update in await async_client.stream_l1_book_snapshots([tp], "CME"):
        assert update is not None
        if i == 100:
            break
        i += 1
    return True
