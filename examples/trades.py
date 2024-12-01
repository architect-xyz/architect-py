import asyncio

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError

from .common import create_async_client


async def main():
    c: AsyncClient = create_async_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        stream = c.subscribe_trades(market_id, ping_interval=None)
        async for trade in stream:
            print(trade)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
