import logging

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
    "market_id",
    [
        "BTC Crypto/USDT Crypto*BINANCE/DIRECT",
        "ETH Crypto/USDT Crypto*BINANCE/DIRECT",
        "SOL Crypto/USDT Crypto*BINANCE/DIRECT",
    ],
)
async def test_live_far_order_cancel(async_client: AsyncClient, market_id: str):
    """
    Place's a book far above the spread, waits for placement, then should successfully cancel order
    """

    # Get snapshot
    market = await async_client.get_market(market_id)
    assert market is not None, f"Market does not exist for {market_id}"

    snapshot = await async_client.get_market_snapshot(market_id)
    assert snapshot is not None, f"Snapshot does not exist for {market_id}"

    min_qty = float(market.min_order_quantity)
    far_price = float(snapshot.last_price) * 0.1

    assert (
        min_qty * far_price < 10
    )  # ensure we are spending more than $10 on this (even though we will cancel the order)

    # Make a very cheap
    order = await async_client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=min_qty,  # not sure what's going here with min qty not being accurate
        limit_price=far_price,
    )

    assert order is not None

    cancel = await async_client.cancel_order(order.order.id)

    assert cancel
