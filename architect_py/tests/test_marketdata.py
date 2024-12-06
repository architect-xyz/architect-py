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


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_subscribe_l1_stream(async_client: AsyncClient):
    i = 0
    async for snap in await async_client.subscribe_l1_book_snapshots(
        "binance-futures-usd-m.marketdata.architect.co",
        market_ids=[
            "BTC-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT"
        ],
    ):
        # CR alee: really these should WARN a few times before failing;
        # think about how this interacts with presence
        assert snap.best_bid is not None, "BTC-USDT should always be bid"
        assert snap.best_ask is not None, "BTC-USDT should always be offered"
        assert snap.best_bid[0] > 1_000, "BTC should be > $1000"
        assert snap.best_ask[0] < 10_000_000, "USDT should be < $10000000"
        i += 1
        if i > 5:
            break
