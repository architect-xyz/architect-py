import asyncio
from graphql_client.client import Client
from graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client


async def main():
    c: Client = create_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        stream = c.subscribe_trades(market_id, ping_interval=None)
        async for item in stream:
            print(item.trades)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
