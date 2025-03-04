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
        ("cme.marketdata.architect.co", lf("front_ES_future"), "CME"),
        # (
        #     "binance-futures-usd-m.marketdata.architect.co",
        #     "BTC-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT",
        #     "BINANCE",
        # ),
        # (
        #     "bybit.marketdata.architect.co",
        #     "BTC-USDT BYBIT Perpetual/USDT Crypto*BYBIT/DIRECT",
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
    tp = TradableProduct(symbol, "USD")

    await async_client.grpc_client.change_channel(endpoint)

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    symbols = [tp]

    [l1_book] = await async_client.subscribe_l1_book(symbols)
    ts = l1_book.timestamp

    i = 0
    async for snap in async_client.grpc_client.subscribe_l1_book_snapshots(
        symbols=symbols
    ):
        # CR alee: really these should WARN a few times before failing;
        # think about how this interacts with presence
        assert snap.best_bid is not None, f"{symbol} should always be bid"
        assert snap.best_ask is not None, f"{symbol} should always be offered"
        assert snap.best_bid[0] > 1_000, f"{symbol} should be > $1000"
        assert snap.best_ask[0] < 10_000_000, f"{symbol} should be < $10000000"
        i += 1
        if i > 5:
            break
    await asyncio.sleep(1)

    if ts >= l1_book.timestamp:
        raise ValueError(f"Timestamp should be increasing {l1_book}")


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_subscribe_l2_stream(async_client: AsyncClient, front_ES_future: str):
    venue = "CME"
    tp = TradableProduct(front_ES_future, "USD")

    market_status = await async_client.get_market_status(tp, venue)
    if not market_status.is_trading:
        pytest.skip("market is not trading")

    l2_book = await async_client.subscribe_l2_book(tp, venue)
    ts = l2_book.timestamp

    i = 0
    async for snap in async_client.grpc_client.subscribe_l2_book_updates(
        symbol=tp, venue=venue
    ):
        assert snap is not None
        i += 1
        if i > 5:
            break
    await asyncio.sleep(1)

    if ts >= l2_book.timestamp:
        raise ValueError(f"Timestamp should be increasing {l2_book}")


@pytest.mark.asyncio
@pytest.mark.timeout(2)
async def test_subscribe_cme_trades(async_client: AsyncClient):
    venue = "CME"
    markets = await async_client.get_cme_futures_series("ES CME Futures")
    _, market = markets[0]

    market = TradableProduct(market, "USD")
    market_status = await async_client.get_market_status(market, venue)

    if not market_status.is_trading:
        pytest.skip("market is not trading")

    trades = await async_client.subscribe_trades(market, venue)
    for _ in range(5):
        trade = await anext(trades)
        assert trade is not None, "trade from stream was None"
