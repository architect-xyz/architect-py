import asyncio

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.enums import CandleWidth
from architect_py.graphql_client.exceptions import GraphQLClientHttpError

from .common import create_async_client


async def main():
    c: AsyncClient = create_async_client()
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        stream = c.subscribe_candles(
            market_id, width=CandleWidth.ONE_MINUTE, ping_interval=None
        )
        async for candle in stream:
            print(candle)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
