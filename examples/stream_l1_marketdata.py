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
    markets = await c.search_markets(venue="BYBIT")
    markets_by_id = {}
    for market in markets:
        markets_by_id[UUID(market.id)] = market
    print(f"Loaded {len(markets)} markets")

    channel = await c.grpc_channel("spot.bybit.marketdata.architect.co")
    stub = JsonMarketdataStub(channel)
    req = SubscribeL1BookSnapshotsRequest(market_ids=None)
    async for snap in stub.SubscribeL1BookSnapshots(req):
        market_name = "<unknown>"
        if snap.market_id in markets_by_id:
            market = markets_by_id[snap.market_id]
            market_name = market.name
        best_bid_s = "<no bid>"
        best_ask_s = "<no ask>"
        if snap.best_bid:
            best_bid_s = f"{snap.best_bid[1]} x {snap.best_bid[0]}"  # size x price
        if snap.best_ask:
            best_ask_s = f"{snap.best_ask[0]} x {snap.best_ask[1]}"  # price x size
        print(f"{market.name} {snap.timestamp()} {best_bid_s} {best_ask_s}")


asyncio.run(main())
