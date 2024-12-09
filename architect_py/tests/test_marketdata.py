import pytest
import pytz
from datetime import datetime
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
@pytest.mark.parametrize(
    "endpoint,market_id", 
    [
        ("binance-futures-usd-m.marketdata.architect.co", "BTC-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT"),
        ("bybit.marketdata.architect.co", "BTC-USDT BYBIT Perpetual/USDT Crypto*BYBIT/DIRECT"),
        ("okx.marketdata.architect.co", "BTC-USDT OKX Perpetual/USDT Crypto*OKX/DIRECT")
    ]
)
async def test_subscribe_l1_stream(async_client: AsyncClient, endpoint: str, market_id: str):
    i = 0
    async for snap in await async_client.subscribe_l1_book_snapshots(
        endpoint,
        market_ids=[market_id]
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


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_l2_snapshot(async_client: AsyncClient):
    snap = await async_client.l2_book_snapshot(
        "okx.marketdata.architect.co",
        "BTC Crypto/USD*OKX/DIRECT"
    )
    assert snap is not None, "snapshot should not be None"


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_marketdata_snapshots(async_client: AsyncClient):
    # TODO: what is the actual expectation here?
    # Check if market should be open based on CME hours
    now = datetime.now(pytz.timezone('US/Central'))
    weekday = now.weekday()
    if weekday == 5:  # Saturday
        pytest.skip("CME is closed on Saturday")
    elif weekday == 4:  # Friday
        if now.hour >= 21:  # After 9 PM
            pytest.skip("CME is closed after 9 PM CT on Friday")
    elif weekday == 6:  # Sunday
        if now.hour < 17:  # Before 5 PM
            pytest.skip("CME opens at 5 PM CT on Sunday")

    markets = await async_client.get_cme_futures_series("ES")
    _, market = markets[0]
    snap = await async_client.get_market_snapshot(market.id)
    assert snap is not None, "snapshot should not be None"
