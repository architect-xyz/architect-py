import asyncio

from decimal import Decimal
import logging

from architect_py.async_client import AsyncClient
from architect_py.graphql_client.enums import OrderType, TimeInForce
from architect_py.scalars import OrderDir, TradableProduct

LOGGER = logging.getLogger(__name__)

api_key = None
api_secret = None
HOST = None
ACCOUNT = None


if api_key is None or api_secret is None or HOST is None or ACCOUNT is None:
    raise ValueError(
        "Please set the api_key, api_secret, HOST, and ACCOUNT variables before running this script"
    )


client = AsyncClient(host=HOST, api_key=api_key, api_secret=api_secret)


async def search_symbol() -> tuple[str, TradableProduct]:
    venue = "CME"
    markets = await client.search_symbols(
        search_string="ES",
        execution_venue=venue,
    )
    market = markets[0]
    return venue, market


async def test_send_order():
    venue, symbol = await search_symbol()

    snapshot = await client.get_market_snapshot(symbol=symbol, venue=venue)
    if snapshot is None:
        return ValueError(f"Market snapshot for {symbol} is None")

    if snapshot.ask_price is None or snapshot.bid_price is None:
        return ValueError(f"Market snapshot for {symbol} is None")

    order = await client.send_limit_order(
        symbol=symbol,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=PlaceOrderRequestType.LIMIT,
        execution_venue="CME",
        post_only=True,
        limit_price=snapshot.bid_price
        - (snapshot.ask_price - snapshot.bid_price) * Decimal(10),
        account=ACCOUNT,
        time_in_force=TimeInForce.IOC,
    )
    logging.critical(f"ORDER TEST: {order}")

    assert order is not None

    cancel = await client.cancel_order(order.id)

    return cancel


async def test_cancel_all_orders():
    await client.cancel_all_orders()


async def test_send_market_pro_order():
    venue, symbol = await search_symbol()
    print(symbol)

    await client.send_market_pro_order(
        symbol=symbol,
        execution_venue=venue,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force=TimeInForce.IOC,
    )


async def main():
    await test_send_market_pro_order()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
