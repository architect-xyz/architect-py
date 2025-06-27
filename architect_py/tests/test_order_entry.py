import asyncio
from decimal import Decimal

import pytest

from architect_py import AsyncClient, OrderDir, TickRoundMethod
from architect_py.common_types.tradable_product import TradableProduct
from architect_py.grpc.models.definitions import OrderType, SpreaderParams


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_place_limit_order(async_client: AsyncClient):
    venue = "CME"
    front_future = await async_client.get_front_future("ES CME Futures", venue)
    info = await async_client.get_execution_info(front_future, venue)
    assert info is not None
    assert info.tick_size is not None
    snap = await async_client.get_ticker(front_future, venue)
    assert snap is not None
    assert snap.bid_price is not None
    accounts = await async_client.list_accounts()
    account = accounts[0]

    # bid far below the best bid
    limit_price = TickRoundMethod.FLOOR(snap.bid_price * Decimal(0.9), info.tick_size)
    order = await async_client.place_order(
        symbol=front_future,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=OrderType.LIMIT,
        limit_price=limit_price,
        post_only=False,
        account=str(account.account.id),
    )

    assert order is not None
    await asyncio.sleep(1)
    await async_client.cancel_order(order.id)

    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_place_market_order(async_client: AsyncClient):
    venue = "CME"
    front_future = await async_client.get_front_future("ES CME Futures", venue)
    info = await async_client.get_execution_info(front_future, venue)
    assert info is not None
    assert info.tick_size is not None
    snap = await async_client.get_ticker(front_future, venue)
    assert snap is not None
    assert snap.bid_price is not None
    accounts = await async_client.list_accounts()
    account = accounts[0]

    # bid far below the best bid
    order = await async_client.place_order(
        symbol=front_future,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=OrderType.MARKET,
        account=str(account.account.id),
    )

    assert order is not None

    await asyncio.sleep(1.5)
    order = await async_client.get_order(order.id)
    assert order is not None

    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_equity_order(async_client: AsyncClient):
    tradable_product = TradableProduct(base_or_value="AAPL US Equity/USD")

    product_info = await async_client.get_product_info(tradable_product.base())
    assert product_info is not None
    venue = product_info.primary_venue
    assert venue is not None

    market_status = await async_client.get_market_status(tradable_product, venue)
    if not market_status.is_trading:
        pytest.skip(f"Market {venue} for {tradable_product} is not open")

    info = await async_client.get_execution_info(tradable_product, venue)
    assert info is not None
    # assert info.tick_size is not None

    tick_size = Decimal("0.01")

    snap = await async_client.get_ticker(tradable_product, venue)
    assert snap is not None
    assert snap.bid_price is not None
    accounts = await async_client.list_accounts()
    account = accounts[0]

    # bid far below the best bid
    limit_price = TickRoundMethod.FLOOR(snap.bid_price * Decimal(0.9), tick_size)
    order = await async_client.place_order(
        symbol=tradable_product,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=OrderType.LIMIT,
        limit_price=limit_price,
        post_only=False,
        account=str(account.account.id),
    )

    assert order is not None
    await asyncio.sleep(1)
    await async_client.cancel_order(order.id)

    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_spreader_algo(async_client: AsyncClient):
    accounts = await async_client.list_accounts()
    account = accounts[0]

    venue = "CME"

    front_ES_future = await async_client.get_front_future("ES CME Futures", venue)
    front_NQ_future = await async_client.get_front_future("NQ CME Futures", venue)

    params = SpreaderParams(
        dir=OrderDir.BUY,  # or OrderDir.SELL
        leg1_marketdata_venue=venue,
        leg1_price_offset=Decimal("0"),
        leg1_price_ratio=Decimal("1"),
        leg1_quantity_ratio=Decimal("1"),
        leg1_symbol=front_ES_future,
        leg2_marketdata_venue=venue,
        leg2_price_offset=Decimal("0"),
        leg2_price_ratio=Decimal("-1"),
        leg2_quantity_ratio=Decimal("-1"),
        leg2_symbol=front_NQ_future,
        limit_price=Decimal("0.25"),
        order_lockout="1s",
        quantity=Decimal("10"),
        leg1_account=account.account.id,
        leg1_execution_venue=venue,
        leg2_account=account.account.id,
        leg2_execution_venue=venue,
    )

    order = await async_client.place_algo_order(params=params)

    print(order)

    await async_client.close()
