import asyncio
from graphql_client.client import Client
from graphql_client.enums import CandleWidth
from graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client

async def main():
    c: Client = create_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        stream = c.subscribe_candles(market_id, width=CandleWidth.ONE_MINUTE)
        async for item in stream:
            print(item.candles)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())

asyncio.run(main())
