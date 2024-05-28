import asyncio
import time
from architect_py.client import Client
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client
from .book_subscription import print_book


async def main():
    c: Client = create_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        start = time.perf_counter()
        result = await c.get_book_snapshot(market_id, num_levels=100)
        elapsed = time.perf_counter() - start
        print_book(result.book_snapshot)
        print(f"Elapsed time: {elapsed:.4f} seconds")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
