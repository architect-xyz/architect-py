"""
Example of using a bidirectional orderflow channel with the Architect OEMS.

This connection style is ~equivalent to having a websocket.

This code example sends a series of orders to Architect while concurrently
listening to orderflow events.  Compare to `examples/orderflow_streaming.py`,
which accomplishes the same thing but using a separate asyncio task.


See funding_rate_mean_reversion_algo.py for a more complete example of
using the orderflow channel to implement a trading strategy.
"""

import asyncio
from decimal import Decimal

from architect_py import (
    AsyncClient,
    OrderDir,
    OrderType,
    TimeInForce,
)
from architect_py.grpc.orderflow import OrderflowChannel, PlaceOrder

from .config import connect_async_client


async def send_orders(client: AsyncClient, orderflow_channel: OrderflowChannel):
    symbol = await client.get_front_future("ES CME Futures")
    print(f"symbol={symbol}")

    while True:
        await asyncio.sleep(1)
        snap = await client.get_l1_book_snapshot(symbol, "CME")
        if snap.best_ask is not None:
            limit_price = snap.best_ask[0]
            print(f"\nPlacing buy order at {limit_price}\n")
            try:
                # can also CancelOrder
                req = PlaceOrder.new(
                    symbol=symbol,
                    execution_venue="CME",
                    dir=OrderDir.BUY,
                    quantity=Decimal(1),
                    limit_price=limit_price,
                    post_only=True,
                    time_in_force=TimeInForce.DAY,
                    order_type=OrderType.LIMIT,
                )
                print(f"req={req}")
                await orderflow_channel.send(req)
            except Exception as e:
                print(f"Error placing order: {e}")
        else:
            print("\nNo ask price from snapshot, doing nothing\n")


async def read_events(orderflow_channel: OrderflowChannel):
    async for event in orderflow_channel:
        print(f" --> {event}")


async def main():
    client = await connect_async_client()

    orderflow_channel = await client.orderflow()

    await asyncio.gather(
        send_orders(client, orderflow_channel),
        read_events(orderflow_channel),
    )


asyncio.run(main())
