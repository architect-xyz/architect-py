import asyncio
from decimal import Decimal

import pytest

from architect_py import AsyncClient, OrderDir, TickRoundMethod
from architect_py.grpc.models.definitions import OrderType


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_place_limit_order(async_client: AsyncClient):
    venue = "CME"
    front_future = await async_client.get_front_future("ES CME Futures", venue)
    info = await async_client.get_execution_info(front_future, venue)
    assert info is not None
    assert info.tick_size is not None
    snap = await async_client.get_ticker(front_future, venue)
    assert snap is not None
    assert snap.bid_price is not None
    accounts = await async_client.list_accounts()
    account = accounts[0]

    # bid far below the best bid
    limit_price = TickRoundMethod.FLOOR(snap.bid_price * Decimal(0.9), info.tick_size)
    order = await async_client.place_order(
        symbol=front_future,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=OrderType.LIMIT,
        limit_price=limit_price,
        post_only=False,
        account=str(account.account.id),
    )

    assert order is not None
    await asyncio.sleep(1)
    await async_client.cancel_order(order.id)

    await async_client.close()
