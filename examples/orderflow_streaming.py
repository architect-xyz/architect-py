"""
Example of streaming orderflow events from the Architect OEMS.

This code example sends a series of orders to Architect in one asyncio
task, while concurrently listening to orderflow events in another.
"""

import asyncio
from decimal import Decimal

from architect_py import AsyncClient, OrderDir

from .config import connect_async_client


async def send_orders(client: AsyncClient):
    symbol = await client.get_front_future("ES CME Futures")
    print(f"symbol={symbol}")

    while True:
        await asyncio.sleep(1)
        snap = await client.get_l1_book_snapshot(symbol, "CME")
        if snap.best_ask is not None:
            limit_price = snap.best_ask[0]
            print(f"\nPlacing buy order at {limit_price}\n")
            await client.place_limit_order(
                symbol=symbol,
                execution_venue="CME",
                dir=OrderDir.BUY,
                quantity=Decimal(1),
                limit_price=limit_price,
                post_only=True,
            )
        else:
            print("\nNo ask price from snapshot, doing nothing\n")


async def main():
    client = await connect_async_client()

    asyncio.create_task(send_orders(client))

    async for event in client.stream_orderflow():
        print(f" --> {event}")


asyncio.run(main())
