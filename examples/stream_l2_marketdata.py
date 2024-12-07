import asyncio
import os
from uuid import UUID
from architect_py.async_client import AsyncClient
from .common import create_async_client

buy_columns = "{:>15} {:>15}"
sell_columns = "{:<15} {:<15}"
green = "\033[32m"
red = "\033[31m"
normal = "\033[0m"


async def watch_l2_book(c: AsyncClient, endpoint: str, market_id: str):
    async for seq_id, seq_num in c.watch_l2_book(
        endpoint,
        market_id
    ):
        print(f"seq_id: {seq_id}, seq_num: {seq_num}")


async def print_l2_book(c: AsyncClient, market_id: str):
    while True:
        if market_id in c.l2_books:
            book = c.l2_books[market_id].snapshot()
            print(f"book timestamp: {book.timestamp()}")
            print(
                (buy_columns + " " + sell_columns).format(
                    "Size", "Bid", "Ask", "Size"
                )
            )
            for i in range(min(20, len(book.bids), len(book.asks))):
                b = book.bids[i]
                s = book.asks[i]
                print(
                    (green + buy_columns).format(b[1], b[0]),
                    (red + sell_columns).format(s[0], s[1]),
                )
            print(normal)
        await asyncio.sleep(2)


async def main():
    c: AsyncClient = create_async_client()
    endpoint = "https://coinbase.marketdata.architect.co"
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    await asyncio.gather(
        watch_l2_book(c, endpoint, market_id),
        print_l2_book(c, market_id)
    )


asyncio.run(main())
