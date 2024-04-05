import asyncio
import os
from graphql_client.client import Client
from graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client

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
    c: Client = create_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    # market_id = "SOL-USDC Perpetual/USDC Crypto*BINANCE-FUTURES-USD-M/DIRECT"
    try:
        stream = c.subscribe_book(market_id, precision="0.1", ping_interval=None)
        async for item in stream:
            print_book(item.book)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
