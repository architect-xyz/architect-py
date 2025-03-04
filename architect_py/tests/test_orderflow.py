from decimal import Decimal

import pytest

from architect_py.async_client import AsyncClient, OrderDir
from architect_py.scalars import TradableProduct
from architect_py.utils.nearest_tick_2 import TickRoundMethod


@pytest.mark.asyncio
@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    "symbol,venue",
    [
        ("MES 20260320 CME Future", "CME"),
    ],
)
async def test_live_far_order_cancel(
    async_client: AsyncClient, symbol: str, venue: str
):
    """
    Places a bid order far below best bid, waits for placement, then should successfully cancel order
    """

    tp = TradableProduct(symbol, "USD")

    # Get snapshot
    execution_info = await async_client.get_execution_info(tp, venue)
    assert (
        execution_info is not None
    ), f"execution_info does not exist for {symbol}, {venue}"

    assert execution_info.min_order_quantity is not None
    assert execution_info.tick_size is not None

    snapshot = await async_client.get_market_snapshot(tp, venue)
    assert (
        snapshot is not None
    ), f"Snapshot does not exist for {symbol} at venue {venue}"

    min_qty = Decimal(execution_info.min_order_quantity)

    if last_price := snapshot.bid_price:
        far_price = last_price * Decimal("0.8")
    else:
        raise ValueError("No last price in snapshot")
    limit_price = TickRoundMethod.FLOOR(far_price, execution_info.tick_size)

    # Make a very cheap bid
    order = await async_client.send_limit_order(
        symbol=tp,
        odir=OrderDir.BUY,
        execution_venue=venue,
        quantity=min_qty,
        limit_price=limit_price,
    )

    assert order is not None

    cancel = await async_client.cancel_order(order.id)

    assert cancel
