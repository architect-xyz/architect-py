import asyncio

from architect_py import AsyncClient, TradableProduct

from .config import connect_async_client


async def main():
    c: AsyncClient = await connect_async_client()

    async for snap in c.stream_l1_book_snapshots(
        symbols=[TradableProduct("ES 20250620 CME Future/USD")],
        venue="CME",
    ):
        best_bid_s = "<no bid>"
        best_ask_s = "<no ask>"
        if snap.best_bid:
            best_bid_s = f"{snap.best_bid[1]} x {snap.best_bid[0]}"  # size x price
        if snap.best_ask:
            best_ask_s = f"{snap.best_ask[0]} x {snap.best_ask[1]}"  # price x size
        print(f"{snap.symbol} {snap.timestamp} {best_bid_s} {best_ask_s}")

    await c.close()


asyncio.run(main())
