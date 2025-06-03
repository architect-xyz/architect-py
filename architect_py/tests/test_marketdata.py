from datetime import datetime, timedelta, timezone

import pytest
from pytest_lazy_fixtures import lf

from architect_py import AsyncClient, CandleWidth


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_get_market_status(async_client: AsyncClient, venue: str, symbol: str):
    market_status = await async_client.get_market_status(symbol, venue)
    assert market_status is not None
    # CR alee: this is broken upstream
    # assert market_status.is_trading
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("CME", lf("front_ES_future_usd")),
    ],
)
async def test_get_historical_candles(
    async_client: AsyncClient, venue: str, symbol: str
):
    start = datetime.now(timezone.utc)
    candles = await async_client.get_historical_candles(
        symbol, venue, CandleWidth.OneHour, start - timedelta(hours=24), start
    )
    assert len(candles) > 0
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_get_l1_book_snapshot(async_client: AsyncClient, venue: str, symbol: str):
    snap = await async_client.get_l1_book_snapshot(symbol, venue)
    assert snap is not None
    assert snap.best_bid is not None
    assert snap.best_ask is not None
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_get_l2_book_snapshot(async_client: AsyncClient, venue: str, symbol: str):
    snap = await async_client.get_l2_book_snapshot(symbol, venue)
    assert snap is not None
    assert len(snap.bids) > 0
    assert len(snap.asks) > 0
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_get_ticker(async_client: AsyncClient, venue: str, symbol: str):
    ticker = await async_client.get_ticker(symbol, venue)
    assert ticker is not None
    assert ticker.last_price is not None
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_stream_l1_book_snapshots(
    async_client: AsyncClient, venue: str, symbol: str
):
    i = 0
    async for snap in async_client.stream_l1_book_snapshots([symbol], venue):
        assert snap is not None
        assert snap.best_bid is not None
        assert snap.best_ask is not None
        i += 1
        if i > 20:
            break
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_stream_l2_book_updates(
    async_client: AsyncClient, venue: str, symbol: str
):
    from architect_py.grpc.models.Marketdata.L2BookUpdate import Diff, Snapshot

    i = 0
    sid = None
    sn = None
    async for up in async_client.stream_l2_book_updates(symbol, venue):
        assert up is not None
        if isinstance(up, Snapshot):
            assert len(up.bids) > 0
            assert len(up.asks) > 0
            assert i == 0, "snapshot should be the first update"
            sid = up.sequence_id
            sn = up.sequence_number
        elif isinstance(up, Diff):
            assert i > 0, "diff should not be the first update"
            assert sid == up.sequence_id, "sequence number reset on diff"
            assert sn is not None, "sequence number should be set"
            assert up.sequence_number == sn + 1, (
                "sequence number not monotonically increasing"
            )
            sn = up.sequence_number
        i += 1
        if i > 20:
            break
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "venue,symbol",
    [
        ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
    ],
)
async def test_stream_trades(async_client: AsyncClient, venue: str, symbol: str):
    i = 0
    async for trade in async_client.stream_trades(symbol, venue):
        assert trade is not None
        i += 1
        if i > 20:
            break

    await async_client.close()


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "venue,symbol",
#     [
#         ("BINANCE/USDM", "BTC-USDT BINANCE Perpetual/USDT Crypto"),
#     ],
# )
# async def test_stream_candles(async_client: AsyncClient, venue: str, symbol: str):
#     i = 0
#     async for candle in async_client.stream_candles(
#         symbol, venue, [CandleWidth.OneSecond]
#     ):
#         assert candle is not None
#         i += 1
#         if i > 3:
#             break
