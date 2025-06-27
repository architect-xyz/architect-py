import asyncio
from decimal import Decimal

import pytest

from architect_py import AsyncClient, OrderDir, OrderType, TradableProduct

ES_MULTIPLIER = Decimal("50.0")  # ES futures multiplier


@pytest.mark.asyncio
async def test_paper_setup(async_client: AsyncClient):
    accounts = await async_client.list_accounts()

    assert len(accounts) == 1, (
        f"Expected exactly one account in paper trading mode, got {len(accounts)}"
    )

    front_ES_future = await async_client.get_front_future("ES CME Futures", "CME")

    product_info = await async_client.get_product_info(front_ES_future.base())
    assert product_info is not None, (
        f"Expected product info for {front_ES_future.base()} to be not None"
    )
    assert product_info.multiplier == ES_MULTIPLIER, (
        f"Expected multiplier for {front_ES_future.base()} to be {ES_MULTIPLIER}, got {product_info.multiplier}"
    )
    await async_client.close()


@pytest.mark.asyncio
async def test_flattening_position(async_client: AsyncClient):
    if not async_client.paper_trading:
        return

    front_ES_future = await async_client.get_front_future("ES CME Futures", "CME")
    [account] = await async_client.list_accounts()
    account_id = account.account.id

    market_status = await async_client.get_market_status(front_ES_future, "CME")
    if not market_status.is_trading:
        await async_client.close()
        pytest.skip(
            f"Market for {front_ES_future} is not trading, skipping test_flattening_position"
        )

    await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=Decimal(value="100"),
        account=account_id,
        order_type=OrderType.MARKET,
    )

    positions = await async_client.get_positions(accounts=[account_id])

    for tp, position in positions.items():
        tradable_product = TradableProduct(tp)
        product_info = await async_client.get_product_info(tradable_product.base())
        assert product_info is not None, (
            f"Expected product info for {tradable_product.base()} to be not None"
        )
        venue = product_info.primary_venue
        assert venue is not None, (
            f"Expected primary venue for {tradable_product.base()} to be not None"
        )

        market_status = await async_client.get_market_status(
            symbol=tp,
            venue=venue,
        )
        if not market_status.is_trading:
            continue

        if position != Decimal(0):
            flatten_direction = OrderDir.SELL if position > Decimal(0) else OrderDir.BUY

            await async_client.place_order(
                symbol=tp,
                dir=flatten_direction,
                quantity=abs(position),
                account=account_id,
                order_type=OrderType.MARKET,
            )

    await asyncio.sleep(1.5)  # wait for orders to be processed

    positions = await async_client.get_positions(accounts=[account_id])
    assert len(positions) == 0, (
        f"Expected no positions in paper trading mode, got {len(positions)}"
    )
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_paper_positions(async_client: AsyncClient):
    venue = "CME"
    if not async_client.paper_trading:
        return

    [account] = await async_client.list_accounts()
    account_id = account.account.id
    front_ES_future = await async_client.get_front_future("ES CME Futures", venue)
    positions = await async_client.get_positions(accounts=[account_id])
    ES_position = positions.get(front_ES_future)

    market_status = await async_client.get_market_status(
        symbol=front_ES_future,
        venue=venue,
    )
    if not market_status.is_trading:
        await async_client.close()
        pytest.skip(
            f"Market for {front_ES_future} is not trading, skipping test_paper_pnl"
        )

    # flatten position
    if ES_position is not None:
        flatten_direction = OrderDir.SELL if ES_position > Decimal(0) else OrderDir.BUY

        order = await async_client.place_order(
            symbol=front_ES_future,
            venue=venue,
            dir=flatten_direction,
            quantity=Decimal(value="1"),
            account=account_id,
            order_type=OrderType.MARKET,
        )
        while True:
            open_orders = await async_client.get_open_orders(order_ids=[order.id])
            if not open_orders:
                break
            await asyncio.sleep(0.2)

        fills = await async_client.get_fills(order_id=order.id)
        assert len(fills.fills) == 1, "Expected exactly one fill for the order"
        assert fills.fills[0].dir == flatten_direction, (
            "Fill direction does not match order direction"
        )

    # go long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(5), (
        f"Expected position in {front_ES_future} to be 5, got {positions.get(front_ES_future)}"
    )

    # go long to flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(value="8"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(8), (
        f"Expected position in {front_ES_future} to be 8, got {positions.get(front_ES_future)}"
    )

    # go long to short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.SELL,
        quantity=Decimal(value="10"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-2), (
        f"Expected position in {front_ES_future} to be -2, got {positions.get(front_ES_future)}"
    )

    # go flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(value="2"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-5), (
        f"Expected position in {front_ES_future} to be -5, got {positions.get(front_ES_future)}"
    )

    # go short to flat
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) is None, (
        f"Expected position in {front_ES_future} to be 0, got {positions.get(front_ES_future)}"
    )

    # go short
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.SELL,
        quantity=Decimal(value="5"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(-5), (
        f"Expected position in {front_ES_future} to be -5, got {positions.get(front_ES_future)}"
    )

    # go short to long
    order = await async_client.place_order(
        symbol=front_ES_future,
        venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(value="10"),
        account=account_id,
        order_type=OrderType.MARKET,
    )
    positions = await async_client.get_positions(accounts=[account_id])
    assert positions.get(front_ES_future) == Decimal(5), (
        f"Expected position in {front_ES_future} to be 5, got {positions.get(front_ES_future)}"
    )
    await async_client.close()


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_paper_pnl(async_client: AsyncClient):
    if not async_client.paper_trading:
        return

    [account] = await async_client.list_accounts()
    account_id = account.account.id
    front_ES_future = await async_client.get_front_future("ES CME Futures", "CME")
    positions = await async_client.get_positions(accounts=[account_id])
    ES_position = positions.get(front_ES_future)

    market_status = await async_client.get_market_status(
        symbol=front_ES_future,
        venue="CME",
    )
    if not market_status.is_trading:
        await async_client.close()
        pytest.skip(
            f"Market for {front_ES_future} is not trading, skipping test_paper_pnl"
        )

    # flatten position
    if ES_position is not None:
        flatten_direction = OrderDir.SELL if ES_position > Decimal(0) else OrderDir.BUY

        quantity = abs(ES_position)

        order = await async_client.place_order(
            symbol=front_ES_future,
            venue="CME",
            dir=flatten_direction,
            quantity=quantity,
            account=account_id,
            order_type=OrderType.MARKET,
        )
        while True:
            open_orders = await async_client.get_open_orders(order_ids=[order.id])
            if not open_orders:
                break
            await asyncio.sleep(0.2)

    position = await async_client.get_positions(accounts=[account_id])
    assert len(position) == 0, (
        f"Expected no positions in paper trading mode, got {position}"
    )

    account_summary = await async_client.get_account_summary(account_id)
    assert account_summary.purchasing_power is not None, (
        "Expected purchasing power after trades to be set, got None"
    )

    pre_purchasing_power = account_summary.purchasing_power

    quantity = Decimal(value="7")

    sell_order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.SELL,
        quantity=quantity,
        account=account_id,
        order_type=OrderType.MARKET,
    )

    buy_order = await async_client.place_order(
        symbol=front_ES_future,
        venue="CME",
        dir=OrderDir.BUY,
        quantity=quantity,
        account=account_id,
        order_type=OrderType.MARKET,
    )
    await asyncio.sleep(1.5)  # wait for order to be processed

    sell_fill = await async_client.get_fills(order_id=sell_order.id)
    sell_fill_price = sell_fill.fills[0].price

    buy_fill = await async_client.get_fills(order_id=buy_order.id)
    buy_fill_price = buy_fill.fills[0].price

    pnl = (sell_fill_price - buy_fill_price) * ES_MULTIPLIER * quantity

    account_summary = await async_client.get_account_summary(account_id)
    assert account_summary.purchasing_power is not None, (
        "Expected purchasing power after trades to be set, got None"
    )
    post_purchasing_power = account_summary.purchasing_power

    assert post_purchasing_power == pre_purchasing_power + pnl, (
        f"Expected purchasing power to be {pre_purchasing_power + pnl}, got {post_purchasing_power}.\n"
        f"Buy fill price: {buy_fill_price}, Sell fill price: {sell_fill_price}, quantity: {quantity}, pnl: {pnl}, pre_purchasing_power: {pre_purchasing_power}, post_purchasing_power: {post_purchasing_power}"
    )
    await async_client.close()
