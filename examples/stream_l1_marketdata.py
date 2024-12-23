import asyncio
from uuid import UUID

from architect_py.async_client import AsyncClient
from architect_py.protocol.marketdata import (
    JsonMarketdataStub,
    SubscribeL1BookSnapshotsRequest,
)

from .common import create_async_client


async def main():
    c: AsyncClient = create_async_client()
    markets = await c.search_markets(venue="BINANCE-FUTURES-USD-M")
    markets_by_id = {}
    for market in markets:
        markets_by_id[UUID(market.id)] = market
    print(f"Loaded {len(markets)} markets")

    async for snap in c.subscribe_l1_book_snapshots(
        "binance-futures-usd-m.marketdata.architect.co",
        market_ids=[
            "POPCAT-USDT BINANCE Perpetual/USDT Crypto*BINANCE-FUTURES-USD-M/DIRECT"
        ],
    ):
        if snap.market_id in markets_by_id:
            market = markets_by_id[snap.market_id]
            market_name = market.name
        else:
            market_name = "<unknown>"

        best_bid_s = "<no bid>"
        best_ask_s = "<no ask>"
        if snap.best_bid:
            best_bid_s = f"{snap.best_bid[1]} x {snap.best_bid[0]}"  # size x price
        if snap.best_ask:
            best_ask_s = f"{snap.best_ask[0]} x {snap.best_ask[1]}"  # price x size
        print(f"{market_name} {snap.timestamp()} {best_bid_s} {best_ask_s}")


asyncio.run(main())
