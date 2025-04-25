import asyncio

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from architect_py.grpc_client.definitions import CandleWidth
from architect_py.scalars import TradableProduct

from .common import connect_async_client


async def main():
    c: AsyncClient = await connect_async_client()
    symbol = "ES 20250321 CME Future"
    quote = "USD"
    tradable_product = TradableProduct(symbol, quote)
    venue = "CME"
    try:
        stream = c.subscribe_candles_stream(
            tradable_product,
            venue,
            candle_widths=[CandleWidth.OneHour],
        )
        async for candle in stream:
            print(candle)
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


asyncio.run(main())
