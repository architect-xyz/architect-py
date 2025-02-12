from decimal import Decimal

import pytest

from architect_py.async_client import AsyncClient, OrderDir


@pytest.mark.asyncio
async def test_orderflow_session(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_market_pro_order(async_client: AsyncClient):
    pass


# Place a far order and then cancel it
# loosely based off code in examples
@pytest.mark.live_orderflow
@pytest.mark.asyncio
@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    "symbol,venue",
    [
        ("BTC Crypto/USDT Crypto*BINANCE/DIRECT", "BINANCE"),
        ("ETH Crypto/USDT Crypto*BINANCE/DIRECT", "BINANCE"),
        ("SOL Crypto/USDT Crypto*BINANCE/DIRECT", "BINANCE"),
    ],
)
async def test_live_far_order_cancel(
    async_client: AsyncClient, symbol: str, venue: str
):
    """
    Place's a book far above the spread, waits for placement, then should successfully cancel order
    """

    # Get snapshot
    market = await async_client.get_execution_info(symbol, venue)
    assert market is not None, f"execution_info does not exist for {symbol}, {venue}"

    snapshot = await async_client.market_snapshot(venue, symbol)
    assert (
        snapshot is not None
    ), f"Snapshot does not exist for {symbol} at venue {venue}"

    min_qty = Decimal(market.min_order_quantity)

    if last_price := snapshot.last_price:
        far_price = last_price * Decimal("1.1")
    else:
        raise ValueError("No last price in snapshot")

    assert (
        min_qty * far_price < 10
    )  # ensure we are spending more than $10 on this (even though we will cancel the order)

    # Make a very cheap
    order = await async_client.send_limit_order(
        symbol=symbol,
        odir=OrderDir.BUY,
        quantity=min_qty,  # not sure what's going here with min qty not being accurate
        limit_price=far_price,
    )

    assert order is not None

    cancel = await async_client.cancel_order(order.id)

    assert cancel
