import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from pytest_lazy_fixtures import lf

from architect_py.async_client import AsyncClient
from architect_py.common_types import TradableProduct


@pytest.mark.asyncio
@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    "endpoint,symbol,venue",
    [
        ("cme.marketdata.architect.co", lf("front_ES_future_tp"), "CME"),
        # (
        #     "https://usdm.binance.marketdata.architect.co",
        #     "BTC-USDT BINANCE Perpetual/USDT Crypto",
        #     "BINANCE",
        # ),
        # (
        #     "https://bybit.marketdata.architect.co",
        #     "BTC-USDT BYBIT Perpetual/USDT Crypto",
        #     "BYBIT",
        # ),
    ],
)
@pytest.mark.asyncio
async def test_subscribe_l1_stream(
    async_client: AsyncClient,
    endpoint: str,
    symbol: str,
    venue: str,
):
    tp = TradableProduct(symbol)

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    symbols = [tp]

    l1_book = await async_client.subscribe_l1_book(tp, venue)

    i = 0
    async for snap in await async_client.stream_l1_book_snapshots(symbols, venue):
        assert snap.best_bid is not None, f"{symbol} should always be bid"
        assert snap.best_ask is not None, f"{symbol} should always be offered"
        assert snap.best_bid[0] > 1_000, f"{symbol} should be > $1000"
        assert snap.best_ask[0] < 10_000_000, f"{symbol} should be < $10000000"
        i += 1
        if i > 5:
            break

    if l1_book.timestamp == 0:
        raise ValueError(f"Timestamp should be increasing {l1_book}")


@pytest.mark.asyncio
@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    "endpoint,symbol,venue",
    [
        ("cme.marketdata.architect.co", lf("front_ES_future_tp"), "CME"),
        # (
        #     "https://usdm.binance.marketdata.architect.co",
        #     "BTC-USDT BINANCE Perpetual/USDT Crypto",
        #     "BINANCE",
        # ),
        # (
        #     "https://bybit.marketdata.architect.co",
        #     "BTC-USDT BYBIT Perpetual/USDT Crypto",
        #     "BYBIT",
        # ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_subscribe_l2_stream(
    async_client: AsyncClient, endpoint: str, symbol: str, venue: str
):
    tp = TradableProduct(symbol)

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    l2_book = await async_client.subscribe_l2_book(tp, venue)
    ts = l2_book.timestamp

    i = 0
    async for snap in await async_client.stream_l2_book_updates(symbol=tp, venue=venue):
        assert snap is not None
        if i > 5:
            break
        i += 1
    await asyncio.sleep(1)

    if ts >= l2_book.timestamp:
        raise ValueError(f"Timestamp should be increasing {l2_book}")


@pytest.mark.asyncio
@pytest.mark.timeout(15)
async def test_subscribe_cme_trades(async_client: AsyncClient, front_ES_future_tp: str):
    venue = "CME"
    market = TradableProduct(front_ES_future_tp)
    market_status = await async_client.get_market_status(market, venue)

    if not market_status.is_trading:
        pytest.skip("market is not trading")
    elif not 9 <= datetime.now(ZoneInfo("America/Chicago")).hour < 17:
        pytest.skip("market is not liquid")

    i = 0
    async for trade in await async_client.stream_trades(market, venue):
        assert trade is not None, "trade from stream was None"
        if i > 3:
            break
        i += 1
