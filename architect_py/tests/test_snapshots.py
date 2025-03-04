import pytest

from architect_py.async_client import AsyncClient
from architect_py.scalars import TradableProduct

from pytest_lazy_fixtures import lf


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "symbol,venue",
    [
        (lf("front_ES_future"), "CME"),
        # (
        #     "BTC-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT",
        #     "BINANCE",
        # ),
        # (
        #     "BTC-USDT BYBIT Perpetual/USDT Crypto*BYBIT/DIRECT",
        #     "BYBIT",
        # ),
    ],
)
async def test_l2_snapshot(async_client: AsyncClient, symbol: str, venue: str):
    tp = TradableProduct(symbol, "USD")

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    snap = await async_client.get_l2_book_snapshot(
        tp,
        venue,
    )
    assert snap is not None, "snapshot should not be None"


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_marketdata_snapshots(async_client: AsyncClient, front_ES_future: str):
    venue = "CME"

    market = TradableProduct(front_ES_future, "USD")
    market_status = await async_client.get_market_status(market, venue)

    if not market_status.is_trading:
        pytest.skip("market is not trading")

    snap = await async_client.get_market_snapshot(
        symbol=TradableProduct(market), venue="CME"
    )
    assert snap is not None, "snapshot should not be None"
