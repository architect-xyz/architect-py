import asyncio

from architect_py import AsyncClient, TradableProduct
from architect_py.graphql_client.exceptions import GraphQLClientHttpError

from .config import connect_async_client


async def main():
    c: AsyncClient = await connect_async_client()
    market_id = TradableProduct("BTC Crypto", "USD")
    try:
        async for trade in c.stream_trades(market_id, venue="COINBASE"):
            print(trade)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())

    await c.close()


asyncio.run(main())
