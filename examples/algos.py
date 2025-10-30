import asyncio
from decimal import Decimal

from architect_py import *
from examples.config import connect_async_client


async def send_oto_order():
    client: AsyncClient = await connect_async_client()

    ES_front_future = await client.get_front_future("ES CME Futures")
    accounts = await client.list_accounts()

    account = accounts[0].account.id
    venue = "CME"
    snap = await client.get_l1_book_snapshot(ES_front_future, venue)

    assert snap.a and snap.b, "Order book snapshot must have bids and asks"

    bid = snap.b[0]

    execution_info = await client.get_execution_info(ES_front_future, venue)

    assert execution_info is not None, "Execution info must be available"

    assert execution_info.min_order_quantity_unit is MinOrderQuantityUnit.unit

    primary = OrderInfo.new(
        symbol=ES_front_future,
        dir=OrderDir.BUY,
        quantity=Decimal("5"),
        order_type=OrderType.LIMIT,
        limit_price=bid,
        post_only=False,
        time_in_force=TimeInForce.DAY,
        execution_venue=venue,
    )

    secondary1 = OrderInfo.new(
        symbol=ES_front_future,
        dir=OrderDir.BUY,
        quantity=Decimal("4"),
        order_type=OrderType.LIMIT,
        limit_price=bid,
        post_only=False,
        time_in_force=TimeInForce.DAY,
        execution_venue=venue,
    )

    secondary2 = OrderInfo.new(
        symbol=ES_front_future,
        dir=OrderDir.SELL,
        quantity=Decimal("3"),
        order_type=OrderType.LIMIT,
        limit_price=bid,
        post_only=False,
        time_in_force=TimeInForce.DAY,
        execution_venue=venue,
    )

    params = OneTriggersOtherParams(
        primary=primary,
        secondary=[secondary1, secondary2],
        trigger_in_proportion=True,
    )

    order = await client.place_algo_order(params=params, account=account)
    print(order)

    status = await client.get_algo_order_status(order.id)
    assert status is not None, "Status details must be available"
    print(status.status_details)

    await client.get_open_orders()

    await asyncio.sleep(1)
    status = await client.get_algo_order_status(order.id)
    assert status is not None, "Status details must be available"

    print(status.status_details.primary_fills)
    print(status.status_details.secondary_fills)

    await client.stop_algo_order(order.id)

    await client.get_open_orders()
