import asyncio

from architect_py import AsyncClient, TradableProduct

from .config import connect_async_client

buy_columns = "{:>15} {:>15}"
sell_columns = "{:<15} {:<15}"
green = "\033[32m"
red = "\033[31m"
normal = "\033[0m"


async def print_l2_book(c: AsyncClient, symbol: TradableProduct, venue: str):
    book = await c.subscribe_l2_book(symbol, venue)
    while True:
        print(f"book timestamp: {book.timestamp}")
        print((buy_columns + " " + sell_columns).format("Size", "Bid", "Ask", "Size"))
        for i in range(min(20, len(book.bids), len(book.asks))):
            b = book.bids[i]
            s = book.asks[i]
            print(
                (green + buy_columns).format(b[1], b[0]),
                (red + sell_columns).format(s[0], s[1]),
            )
        print(normal)
        await asyncio.sleep(1)


async def main():
    c: AsyncClient = await connect_async_client()

    ES_front_future = await c.get_front_future("ES CME Futures")
    market_symbol = TradableProduct(ES_front_future)
    venue = "CME"
    await print_l2_book(c, market_symbol, venue=venue)

    await c.close()


asyncio.run(main())
