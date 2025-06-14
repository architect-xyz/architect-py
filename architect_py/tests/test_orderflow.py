import asyncio
from decimal import Decimal

import pytest

from architect_py import *
from architect_py.grpc.models.Orderflow.Orderflow import TaggedOrderAck
from architect_py.grpc.models.Orderflow.OrderflowRequest import (
    CancelOrder,
    OrderflowRequestUnannotatedResponseType,
    PlaceOrder,
)


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_orderflow(async_client: AsyncClient):
    venue = "CME"
    front_future = await async_client.get_front_future("ES CME Futures", venue)
    async with await async_client.orderflow() as om:
        l1_snapshot = await async_client.get_l1_book_snapshot(front_future, venue=venue)
        assert l1_snapshot.best_bid is not None
        assert l1_snapshot.best_ask is not None
        spread = l1_snapshot.best_ask[0] - l1_snapshot.best_bid[0]
        price: Decimal = l1_snapshot.best_bid[0] - spread * 10

        accounts = await async_client.list_accounts()
        account = next(
            acc.account.name
            for acc in accounts
            if not acc.account.name.startswith("RQD")
        )

        await om.send(
            PlaceOrder.new(
                dir=OrderDir.BUY,
                symbol=front_future,
                time_in_force=TimeInForce.DAY,
                quantity=Decimal(1),
                execution_venue=venue,
                order_type=OrderType.LIMIT,
                limit_price=price,
                post_only=False,
                account=account,
            )
        )
        print("Order placed, waiting for updates...")
        i = 0
        async for update in om:
            assert isinstance(update, OrderflowRequestUnannotatedResponseType)

            if isinstance(update, TaggedOrderAck):
                await om.send(
                    CancelOrder(
                        id=update.id,
                    )
                )
            i += 1
            if i > 1:
                break

    await async_client.cancel_all_orders()
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(4)
async def test_stream_orderflow(async_client: AsyncClient):
    print("Starting to stream Orderflow events...")

    asyncio.create_task(send_order(async_client))
    i = 0
    async for event in async_client.stream_orderflow():
        print(f"Received Orderflow event: {event}")
        assert isinstance(event, OrderflowRequestUnannotatedResponseType)

        if isinstance(event, OrderAck):
            await async_client.cancel_order(event.order_id)

        i += 1
        if i > 1:
            break

    await async_client.close()


async def send_order(client: AsyncClient):
    venue = "CME"
    front_future = await client.get_front_future("ES CME Futures", venue)

    l1_snapshot = await client.get_l1_book_snapshot(front_future, venue=venue)
    assert l1_snapshot.best_bid is not None
    assert l1_snapshot.best_ask is not None
    spread = l1_snapshot.best_ask[0] - l1_snapshot.best_bid[0]
    price: Decimal = l1_snapshot.best_bid[0] - spread * 10

    accounts = await client.list_accounts()
    account = next(
        acc.account.name for acc in accounts if not acc.account.name.startswith("RQD")
    )

    await asyncio.sleep(0.5)
    await client.place_order(
        dir=OrderDir.BUY,
        symbol=front_future,
        time_in_force=TimeInForce.DAY,
        quantity=Decimal(1),
        execution_venue=venue,
        order_type=OrderType.LIMIT,
        limit_price=price,
        post_only=False,
        account=account,
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async_client = loop.run_until_complete(
        AsyncClient.connect(
            api_key="",
            api_secret="",
            paper_trading=True,
            endpoint="https://app.architect.co",
        )
    )

    loop.run_until_complete(test_stream_orderflow(async_client))
    # loop.run_until_complete(test_orderflow(async_client))
