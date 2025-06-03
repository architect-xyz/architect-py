import asyncio
import os

from pydantic import ValidationError

from architect_py import AsyncClient, TradableProduct
from architect_py.graphql_client.exceptions import GraphQLClientHttpError

from .config import connect_async_client

buy_columns = "{:>15} {:>15} {:>15}"
sell_columns = "{:<15} {:<15} {:<15}"
green = "\033[32m"
red = "\033[31m"
normal = "\033[0m"


def print_book(book):
    os.system("clear")
    print(
        (buy_columns + " " + sell_columns).format(
            "Total", "Size", "Bid", "Ask", "Size", "Total"
        )
    )
    for i in range(min(20, len(book.bids), len(book.asks))):
        b = book.bids[i]
        s = book.asks[i]
        print(
            (green + buy_columns).format(b.total, b.amount, b.price),
            (red + sell_columns).format(s.price, s.amount, s.total),
        )
    print(normal)


async def main():
    c: AsyncClient = await connect_async_client()
    symbol = TradableProduct("SOL-USDC BINANCE Perpetual/USDC Crypto")
    try:
        stream = c.stream_l1_book_snapshots(symbols=[symbol], venue="BINANCE")
        # it is better to do `Decimal("0.1")` instead of Decimal(0.1) to avoid floating point errors
        async for book in stream:
            print_book(book)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())
    except ValidationError as e:
        print(e)

    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
