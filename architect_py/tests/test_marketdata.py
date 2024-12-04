import pytest
from architect_py.async_client import AsyncClient


# CR alee: this test only works if the market is open and trading actively..
# @pytest.mark.asyncio
# @pytest.mark.timeout(2)
# async def test_subscribe_cme_trades(async_client: AsyncClient):
#     markets = await async_client.get_cme_futures_series("ES")
#     _, market = markets[0]
#     trades = async_client.subscribe_trades(market.name)
#     for _ in range(5):
#         trade = await anext(trades)
#         assert trade is not None, "trade from stream was None"
