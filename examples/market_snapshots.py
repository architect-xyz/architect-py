import asyncio
from graphql_client.client import Client
from graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client


async def get_market_snapshot(c: Client):
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        r = await c.get_market_snapshot(market_id)
        print(f"Market snapshot for {market_id}:")
        print(f"--> {r}")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def main():
    c = create_client()
    await get_market_snapshot(c)


asyncio.run(main())
