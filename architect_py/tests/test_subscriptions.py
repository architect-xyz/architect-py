import asyncio
import pytest
from architect_py.async_client import AsyncClient
from architect_py.scalars import TradableProduct

from pytest_lazy_fixtures import lf


@pytest.mark.asyncio
@pytest.mark.timeout(3)
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

    await async_client.grpc_client.change_channel(endpoint)

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    symbols = [tp]

    [l1_book] = await async_client.subscribe_l1_book(symbols)

    i = 0
    async for snap in async_client.subscribe_l1_book_stream(symbols, venue):
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
@pytest.mark.timeout(3)
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
@pytest.mark.timeout(3)
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
    async for snap in async_client.grpc_client.subscribe_l2_books_stream(
        symbol=tp, venue=venue
    ):
        assert snap is not None
        if i > 5:
            break
        i += 1
    await asyncio.sleep(1)

    if ts >= l2_book.timestamp:
        raise ValueError(f"Timestamp should be increasing {l2_book}")


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_subscribe_cme_trades(async_client: AsyncClient):
    venue = "CME"
    markets = await async_client.get_cme_futures_series("ES CME Futures")
    _, market = markets[0]

    market = TradableProduct(market, "USD")
    market_status = await async_client.get_market_status(market, venue)

    if not market_status.is_trading:
        pytest.skip("market is not trading")

    i = 0
    async for trade in async_client.subscribe_trades_stream(market, venue):
        assert trade is not None, "trade from stream was None"
        if i > 3:
            break
        i += 1
