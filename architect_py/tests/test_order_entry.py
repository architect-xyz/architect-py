import asyncio
from decimal import Decimal

import pytest

from architect_py import AsyncClient, OrderDir, TickRoundMethod


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_place_limit_order(async_client: AsyncClient):
    # CR alee: there's no good way to get the front month future
    symbol = "MET 20250530 CME Future/USD"
    venue = "CME"
    info = await async_client.get_execution_info(symbol, venue)
    assert info is not None
    assert info.tick_size is not None
    snap = await async_client.get_ticker(symbol, venue)
    assert snap is not None
    assert snap.bid_price is not None
    accounts = await async_client.list_accounts()
    account = accounts[0]

    # bid far below the best bid
    limit_price = TickRoundMethod.FLOOR(snap.bid_price * Decimal(0.9), info.tick_size)
    order = await async_client.place_limit_order(
        symbol=symbol,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        limit_price=limit_price,
        account=str(account.account.id),
    )
    assert order is not None
    await asyncio.sleep(1)
    await async_client.cancel_order(order.id)

    await async_client.close()
