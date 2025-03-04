import pytest

from architect_py.async_client import AsyncClient
from architect_py.scalars import TradableProduct


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "symbol,venue",
    [
        ("ES 20251219 CME Future", "CME"),
        (
            "BTC-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT",
            "BINANCE",
        ),
        (
            "BTC-USDT BYBIT Perpetual/USDT Crypto*BYBIT/DIRECT",
            "BYBIT",
        ),
    ],
)
async def test_l2_snapshot(async_client: AsyncClient, symbol: str, venue: str):
    tp = TradableProduct(symbol, "USD")

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    snap = await async_client.get_l2_book_snapshot(
        symbol,
        venue,
    )
    assert snap is not None, "snapshot should not be None"


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_marketdata_snapshots(async_client: AsyncClient):
    venue = "CME"
    markets = await async_client.get_cme_futures_series("ES CME Futures")
    _, market = markets[0]

    market = TradableProduct(market)
    market_status = await async_client.get_market_status(market, venue)

    if not market_status.is_trading:
        pytest.skip("market is not trading")

    snap = await async_client.get_market_snapshot(
        symbol=TradableProduct(market), venue="CME"
    )
    assert snap is not None, "snapshot should not be None"
