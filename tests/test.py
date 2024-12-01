import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest
from architect_py.async_client import AsyncClient
from architect_py.client import Client
from architect_py.graphql_client.enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
    OrderStateFlags,
)
from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.scalars import OrderDir
from architect_py.utils.dt import get_expiration_from_CME_name
from architect_py.utils.nearest_tick import TickRoundMethod
from dotenv import load_dotenv


# async def flatten_position():
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     [account_summary] = await client.get_account_summaries()

#     for account in account_summary.by_account:

#         for position in account.positions:
#             if position.market and position.account and position.quantity:
#                 position_id = position.market.id
#                 account_id = position.account.id
#                 flatten_dir = position.dir.get_opposite()
#                 quantity = position.quantity

#                 await client.send_market_pro_order(
#                     market=position_id,
#                     odir=flatten_dir,
#                     quantity=quantity,
#                     account=account_id,
#                 )


# @pytest.mark.asyncio
# async def test_get_open_orders():
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     orders = await client.get_open_orders()

#     assert orders is not None


# @pytest.mark.asyncio
# async def test_send_limit_order():
#     # check that sending strings for decimals works
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     markets = await client.search_markets(
#         search_string="MGC", venue="CME", sort_by_volume_desc=True
#     )
#     market = markets[0]

#     snapshot = await client.get_market_snapshot(market.id)
#     if snapshot is None:
#         # return ValueError(f"Market snapshot for {market.name} is None")
#         price = Decimal(10)
#     elif snapshot.ask_price is None or snapshot.bid_price is None:
#         price = Decimal(10)
#         # return ValueError(f"Market snapshot for {market.name} is None")
#     else:
#         price = (
#             float(snapshot.bid_price)
#             - (float(snapshot.ask_price) - float(snapshot.bid_price)) * 10
#         )
#         price = Decimal(price)

#     order_type: CreateOrderType = CreateOrderType.LIMIT

#     order = await client.send_limit_order(
#         market=market.id,
#         odir=OrderDir.BUY,
#         quantity=Decimal(1),
#         order_type=order_type,
#         limit_price=price,
#         account=ACCOUNT,
#         time_in_force_instruction=CreateTimeInForceInstruction.DAY,
#         price_round_method=TickRoundMethod.TOWARD_ZERO,
#         wait_for_confirm=False,
#     )

#     assert order is not None
#     order_id = order.order.id

#     assert order is not None
#     assert order.reject_reason is None
#     cancel = await client.cancel_order(order_id)
#     assert cancel is not None

#     order = await client.get_order(order_id)

#     assert order is not None
#     assert OrderStateFlags.OUT in order.order_state

#     order = await client.send_limit_order(
#         market=market.id,
#         odir=OrderDir.BUY,
#         quantity="1",  # type: ignore  # we do this on purpose to test that sending strings works
#         order_type=order_type,
#         limit_price=price,  # type: ignore  # we do this on purpose to test that sending strings works
#         account=ACCOUNT,
#         time_in_force_instruction=CreateTimeInForceInstruction.GTC,
#         price_round_method=TickRoundMethod.TOWARD_ZERO,
#     )

#     assert order is not None
#     order_id = order.order.id
#     await asyncio.sleep(0.3)
#     order = await client.get_order(order_id)

#     assert order is not None
#     assert order.reject_reason is None
#     cancel = await client.cancel_order(order_id)
#     assert cancel is not None

#     order = await client.send_limit_order(
#         market=market.id,
#         odir=OrderDir.BUY,
#         quantity=Decimal(-1),
#         order_type=order_type,
#         limit_price=price,
#         account=ACCOUNT,
#         time_in_force_instruction=CreateTimeInForceInstruction.GTC,
#         price_round_method=TickRoundMethod.TOWARD_ZERO,
#     )

#     assert order is not None


# @pytest.mark.asyncio
# async def test_market_pro_order():
#     # check that sending strings for decimals works
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     await client.cancel_all_orders()

#     markets = await client.search_markets(glob="MGC*", venue="CME")
#     market = markets[0]
#     market_id = market.id

#     order = await client.send_market_pro_order(
#         market=market_id,
#         odir=OrderDir.BUY,
#         quantity=Decimal(1),
#         account=ACCOUNT,
#         time_in_force_instruction=CreateTimeInForceInstruction.GTC,
#         fraction_through_market=Decimal(0.0005),
#     )

#     await asyncio.sleep(0.2)

#     assert order is not None
#     order_id = order.order.id
#     order = await client.get_order(order_id)
#     assert order is not None
#     assert order.reject_reason is None

#     cancel = await client.cancel_order(order_id)
#     assert cancel is not None


# def sync_get_account_summaries():
#     client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     summaries = client.get_account_summaries()

#     assert summaries is not None
#     return summaries


# @pytest.mark.asyncio
# async def test_get_account_summaries():
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
#     summaries = await client.get_account_summaries()

#     with ThreadPoolExecutor() as executor:
#         future = executor.submit(sync_get_account_summaries)
#         summaries_sync = future.result()

#     assert summaries is not None
#     assert summaries == summaries_sync


# def sync_get_balances_and_positions():
#     client_sync = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     balances = client_sync.get_balances_and_positions()

#     assert balances is not None

#     return balances


# @pytest.mark.asyncio
# async def test_get_balances_and_positions():
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

#     balances = await client.get_balances_and_positions()

#     with ThreadPoolExecutor() as executor:
#         future = executor.submit(sync_get_balances_and_positions)
#         balances_sync = future.result()

#     assert balances is not None
#     assert balances == balances_sync


# @pytest.mark.asyncio
# async def test_cancel_orders():
#     client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
#     await client.cancel_all_orders()


if __name__ == "__main__":
    pytest.main()
