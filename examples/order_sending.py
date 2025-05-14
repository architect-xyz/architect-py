import asyncio
import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from architect_py.async_client import AsyncClient
from architect_py.common_types.order_dir import OrderDir
from architect_py.common_types.tradable_product import TradableProduct
from architect_py.grpc.models.definitions import GoodTilDate, OrderType, TimeInForceEnum
from examples.common import connect_async_client

LOGGER = logging.getLogger(__name__)


async def search_symbol(c: AsyncClient) -> tuple[str, TradableProduct]:
    venue = "CME"
    markets = await c.search_symbols(
        search_string="ES",
        execution_venue=venue,
    )
    market = markets[0]
    return venue, market


async def test_send_order(client: AsyncClient, account: str):
    venue, symbol = await search_symbol(client)

    snapshot = await client.get_market_snapshot(symbol=symbol, venue=venue)
    if snapshot is None:
        return ValueError(f"Market snapshot for {symbol} is None")

    if snapshot.best_ask is None or snapshot.best_bid is None:
        return ValueError(f"Market snapshot for {symbol} is None")

    best_bid_price, best_bid_quantity = snapshot.best_bid

    d = datetime.now(tz=timezone.utc) + timedelta(days=1)
    gtd = GoodTilDate(d)

    order = await client.place_limit_order(
        symbol=symbol,
        odir=OrderDir.BUY,
        quantity=best_bid_quantity,
        order_type=OrderType.LIMIT,
        execution_venue="CME",
        post_only=True,
        limit_price=best_bid_price
        - (snapshot.best_ask[0] - best_bid_price) * Decimal(10),
        account=account,
        time_in_force=gtd,
    )
    logging.critical(f"ORDER TEST: {order}")

    assert order is not None

    cancel = await client.cancel_order(order.id)

    return cancel


async def test_cancel_all_orders(client: AsyncClient):
    await client.cancel_all_orders()


async def test_send_market_pro_order(client: AsyncClient, account: str):
    venue, symbol = await search_symbol(client)
    print(symbol)

    await client.send_market_pro_order(
        symbol=symbol,
        execution_venue=venue,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=account,
        time_in_force=TimeInForceEnum.IOC,
    )


async def main():
    client: AsyncClient = await connect_async_client()
    accounts = await client.list_accounts()
    account: str = accounts[0].account.name

    await test_send_order(client, account)
    await test_send_market_pro_order(client, account)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
