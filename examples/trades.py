import asyncio

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from architect_py.scalars import TradableProduct

from .common import connect_async_client


async def main():
    c: AsyncClient = await connect_async_client()
    market_id = TradableProduct("BTC Crypto", "USD")
    try:
        async for trade in c.subscribe_trades_stream(market_id, venue="COINBASE"):
            print(trade)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
