import asyncio
from architect_py.client import Client
from architect_py.graphql_client.exceptions import GraphQLClientHttpError
from .common import create_client


async def lookup_single_market(c: Client):
    market_id = "BTC Crypto/USD*COINBASE/DIRECT"
    try:
        r = await c.get_market(market_id)
        print(f"Market information for {market_id}:")
        print(f"--> {r}")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def lookup_multiple_markets(c: Client):
    btc_usd_coinbase = "BTC Crypto/USD*COINBASE/DIRECT"
    sol_usdt_binance = "SOL Crypto/USDT Crypto*BINANCE/DIRECT"
    market_ids = [btc_usd_coinbase, sol_usdt_binance]
    try:
        r = await c.get_markets(market_ids)
        results = zip(market_ids, r.markets)
        for market_id, market in results:
            print(f"Market information for {market_id}:")
            print(f"--> {market}")
            print()
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def search_markets(c: Client):
    try:
        r = await c.get_filtered_markets(search_string="SOL", max_results=10)
        for market in r.filter_markets:
            print(f"--> {market.name}")
    except GraphQLClientHttpError as e:
        print(e.status_code)
        print(e.response.json())


async def main():
    c = create_client()
    await lookup_single_market(c)
    await lookup_multiple_markets(c)
    await search_markets(c)


asyncio.run(main())
