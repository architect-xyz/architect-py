import asyncio
from decimal import Decimal

import pytest

from architect_py.async_client import AsyncClient, OrderDir, OrderType


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_positions(async_client: AsyncClient):
    if not async_client.paper_trading:
        return

    accounts = await async_client.list_accounts()

    assert len(accounts) == 1, (
        f"Expected exactly one account in paper trading mode, got {len(accounts)}"
    )
    account_id = accounts[0].account.id
    front_ES_future = await async_client.get_front_future("ES CME Futures", "CME")
    positions = await async_client.get_positions(accounts=[account_id])
    ES_position = positions.get(front_ES_future)

    # flatten position
    if ES_position is not None:
        flatten_direction = OrderDir.SELL if ES_position > Decimal(0) else OrderDir.BUY

        order = await async_client.place_order(
            symbol=front_ES_future,
            venue="CME",
            dir=flatten_direction,
            quantity=Decimal(value="1"),
            account=account_id,
            order_type=OrderType.MARKET,
        )
        while True:
            open_orders = await async_client.get_open_orders(order_ids=[order.id])
            if not open_orders:
                break
            await asyncio.sleep(0.2)

        fills = await async_client.get_fills(order_id=order.id)
        assert len(fills.fills) == 1, "Expected exactly one fill for the order"
        assert fills.fills[0].dir == flatten_direction, (
            "Fill direction does not match order direction"
        )

    # go long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(5), (
        f"Expected position in {front_ES_future} to be 5, got {positions.get(front_ES_future)}"
    )

    # go long to flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="8"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(8), (
        f"Expected position in {front_ES_future} to be 8, got {positions.get(front_ES_future)}"
    )

    # go long to short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.SELL,
        quantity=Decimal(value="10"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-2), (
        f"Expected position in {front_ES_future} to be -2, got {positions.get(front_ES_future)}"
    )

    # go flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="2"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-5), (
        f"Expected position in {front_ES_future} to be -5, got {positions.get(front_ES_future)}"
    )

    # go short to flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-5), (
        f"Expected position in {front_ES_future} to be -5, got {positions.get(front_ES_future)}"
    )

    # go short to long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="10"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(5), (
        f"Expected position in {front_ES_future} to be 5, got {positions.get(front_ES_future)}"
    )
