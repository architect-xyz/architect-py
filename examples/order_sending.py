import asyncio

from decimal import Decimal
import logging
from datetime import datetime, timedelta

from architect_py.async_client import AsyncClient
from architect_py.scalars import OrderDir

from architect_py.graphql_client.enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
    ReferencePrice,
)
from architect_py.graphql_client.fragments import (
    MarketFieldsKindExchangeMarketKind,
)
from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets

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


async def get_market() -> SearchMarketsFilterMarkets:
    markets = await client.search_markets(
        search_string="", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]
    return market


async def test_send_order():
    market = await get_market()
    market_id = market.id

    snapshot = await client.get_market_snapshot(market_id)
    if snapshot is None:
        return ValueError(f"Market snapshot for {market.name} is None")

    if snapshot.ask_price is None or snapshot.bid_price is None:
        return ValueError(f"Market snapshot for {market.name} is None")

    order_type: CreateOrderType = CreateOrderType.LIMIT

    order = await client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=order_type,
        post_only=True,
        limit_price=snapshot.bid_price
        - (snapshot.ask_price - snapshot.bid_price) * Decimal(10),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
    )
    logging.critical(f"ORDER TEST: {order}")

    assert order is not None

    cancel = await client.cancel_order(order.order.id)

    return cancel


async def test_create_twap_algo():
    market = await get_market()
    market_id = market.id

    order = await client.send_twap_algo(
        name="test_TWAP",
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(10),
        interval_ms=1000,
        account=ACCOUNT,
        reject_lockout_ms=1000,
        take_through_frac=Decimal(
            "0.1"
        ),  # we use a string here to avoid floating point errors
        end_time=datetime.now() + timedelta(minutes=10),
    )
    logging.critical(f"TWAP TEST: {order}")
    if order is not None:
        order = await client.cancel_order(order)


async def test_create_pov_algo():
    market = await get_market()
    market_id = market.id

    order = await client.send_pov_algo(
        name="test_POV",
        market=market_id,
        odir=OrderDir.BUY,
        target_volume_frac=Decimal("0.1"),
        min_order_quantity=Decimal(1),
        max_quantity=Decimal(10),
        order_lockout_ms=1000,
        end_time=datetime.now() + timedelta(minutes=10),
        account=ACCOUNT,
    )
    logging.critical(f"POV TEST: {order}")
    if order is not None:
        order = await client.cancel_order(order)


async def test_create_smart_order_router_algo():
    market = await get_market()
    market_id = market.id

    snapshot = await client.get_market_snapshot(market_id)
    if snapshot is None:
        return ValueError(f"Market snapshot for {market.name} is None")

    if snapshot.ask_price is None or snapshot.bid_price is None:
        return ValueError(f"Market snapshot for {market.name} is None")

    lp = snapshot.bid_price - (snapshot.ask_price - snapshot.bid_price) * 50
    assert isinstance(market, SearchMarketsFilterMarkets)
    assert isinstance(market.kind, MarketFieldsKindExchangeMarketKind)

    market.kind

    order = await client.preview_smart_order_router(
        markets=[market_id],
        base=market.kind.base.id,
        quote=market.kind.quote.id,
        odir=OrderDir.BUY,
        limit_price=lp,
        target_size=Decimal(5),
        execution_time_limit_ms=1000,
    )
    logging.critical(f"SOR TEST: {order}")


async def test_create_mm_algo():
    market = await get_market()
    market_id = market.id

    order = await client.send_mm_algo(
        name="test_MM",
        market=market_id,
        buy_quantity=Decimal(1),
        sell_quantity=Decimal(1),
        min_position=Decimal(1),
        max_position=Decimal(10),
        max_improve_bbo=Decimal("0.1"),
        position_tilt=Decimal("0.1"),
        reference_price=ReferencePrice.MID,
        ref_dist_frac=Decimal("0.1"),
        tolerance_frac=Decimal("0.1"),
        fill_lockout_ms=1000,
        order_lockout_ms=1000,
        reject_lockout_ms=1000,
    )
    logging.critical(f"MM TEST: {order}")
    if order is not None:
        order = await client.cancel_order(order)


async def test_cancel_all_orders():
    await client.cancel_all_orders()


async def test_send_market_pro_order():
    market = await get_market()
    print(market)
    market_id = market.id

    await client.send_market_pro_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
    )


async def main():
    await test_send_market_pro_order()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
