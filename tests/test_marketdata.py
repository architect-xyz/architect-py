import pytest
from architect_py.async_client import AsyncClient


# CR alee: this test only works if the market is open..
@pytest.mark.asyncio
@pytest.mark.timeout(2)
async def test_subscribe_trades(async_client: AsyncClient):
    markets = await async_client.search_markets(sort_by_volume_desc=True, max_results=1)
    market = markets[0]
    trades = async_client.subscribe_trades(market.name)
    for _ in range(5):
        trade = await anext(trades)
        assert trade is not None, "trade from stream was None"
