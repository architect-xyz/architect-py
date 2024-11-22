import asyncio
import os
import pytest
from architect_py.async_client import AsyncClient
from architect_py.client import Client
from architect_py.graphql_client.enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
)
from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.scalars import OrderDir
from decimal import Decimal

from architect_py.utils.nearest_tick import TickRoundMethod

from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def test_load_env():
    load_dotenv()
    global HOST, ACCOUNT, API_KEY, API_SECRET, PORT
    HOST = os.getenv("HOST")
    ACCOUNT = os.getenv("ACCOUNT")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    if ACCOUNT is not None and "PAPER" in ACCOUNT:
        PORT = 6789
    else:
        PORT = 4567


@pytest.mark.asyncio
async def test_client_init():
    try:
        client = AsyncClient(host=HOST, api_key=" ", api_secret=" ", port=PORT)
    except ValueError:
        pass
    try:
        client = AsyncClient(
            host=HOST, api_key="asdlfkja", api_secret=";alskjdf", port=PORT
        )
    except ValueError:
        pass

    print(API_KEY, API_SECRET)
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET)


@pytest.mark.asyncio
async def test_get_market():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    markets = await client.search_markets(glob="ES*", venue="CME")
    name = markets[0].name

    market = await client.get_market(name)
    assert market is not None


@pytest.mark.asyncio
async def test_search_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    markets = await client.search_markets(glob="ES*", venue="CME")
    assert len(markets) > 0


@pytest.mark.asyncio
async def test_find_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    markets = await client.search_markets(glob="ES*", venue="CME")
    markets = client.find_markets(base=markets[0].name, venue="CME")

    assert markets is not None


@pytest.mark.asyncio
async def test_subscribe_l1_book_snapshots():
    pass


@pytest.mark.asyncio
async def test_subscribe_l2_book_snapshots():
    pass


@pytest.mark.asyncio
async def test_subscribe_l3_book_snapshots():
    pass


@pytest.mark.asyncio
async def test_subscribe_trades():
    pass


@pytest.mark.asyncio
async def test_get_open_orders():
    pass


async def _get_market(client: AsyncClient) -> SearchMarketsFilterMarkets:
    markets = await client.search_markets(
        search_string="", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]
    return market


def _sync_get_market(client: Client) -> SearchMarketsFilterMarkets:
    markets = client.search_markets(
        search_string="", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]
    return market


@pytest.mark.asyncio
async def test_send_limit_order():
    # check that sending strings for decimals works
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    market = await _get_market(client)
    market_id = market.id

    snapshot = await client.get_market_snapshot(market_id)
    if snapshot is None:
        # return ValueError(f"Market snapshot for {market.name} is None")
        price = Decimal(10)
    elif snapshot.ask_price is None or snapshot.bid_price is None:
        price = Decimal(10)
        # return ValueError(f"Market snapshot for {market.name} is None")
    else:
        price = (
            float(snapshot.bid_price)
            - (float(snapshot.ask_price) - float(snapshot.bid_price)) * 10
        )
        price = Decimal(price)

    order_type: CreateOrderType = CreateOrderType.LIMIT

    order = await client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=order_type,
        post_only=True,
        limit_price=price,
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
        price_round_method=TickRoundMethod.TOWARD_ZERO,
    )

    assert order is not None
    order_id = order.order.id
    await asyncio.sleep(0.3)
    order = await client.get_order(order_id)

    assert order is not None
    assert order.reject_reason is None
    cancel = await client.cancel_order(order_id)
    assert cancel is not None

    order = await client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity="1",  # type: ignore  # we do this on purpose to test that sending strings works
        order_type=order_type,
        post_only=True,
        limit_price=price,  # type: ignore  # we do this on purpose to test that sending strings works
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
        price_round_method=TickRoundMethod.TOWARD_ZERO,
    )

    assert order is not None
    order_id = order.order.id
    await asyncio.sleep(0.3)
    order = await client.get_order(order_id)

    assert order is not None
    assert order.reject_reason is None
    cancel = await client.cancel_order(order_id)
    assert cancel is not None

    order = await client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(-1),
        order_type=order_type,
        post_only=True,
        limit_price=price,
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
        price_round_method=TickRoundMethod.TOWARD_ZERO,
    )

    assert order is not None


def test_sync_market_order():
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    market = _sync_get_market(client)
    market_id = market.id

    order = client.send_market_pro_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
    )

    assert order is not None
    order_id = order.order.id
    order = client.get_order(order_id)
    assert order is not None
    assert order.reject_reason is None


@pytest.mark.asyncio
async def test_market_pro_order():
    # check that sending strings for decimals works
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    market = await _get_market(client)
    market_id = market.id

    order = await client.send_market_pro_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
    )

    await asyncio.sleep(0.2)

    assert order is not None
    order_id = order.order.id
    order = await client.get_order(order_id)
    assert order is not None
    assert order.reject_reason is None


@pytest.mark.asyncio
async def test_send_twap_algo():
    pass


@pytest.mark.asyncio
async def test_send_pov_algo():
    pass


@pytest.mark.asyncio
async def test_send_smart_order_router_algo():
    pass


@pytest.mark.asyncio
async def test_preview_smart_order_router():
    pass


@pytest.mark.asyncio
async def test_send_mm_algo():
    pass


@pytest.mark.asyncio
async def test_send_spread_algo():
    pass


@pytest.mark.asyncio
async def test_get_cme_futures_series():
    pass


@pytest.mark.asyncio
async def test_get_cme_future_from_root_month_year():
    pass


@pytest.mark.asyncio
async def test_get_account_summaries():
    pass


@pytest.mark.asyncio
async def test_get_balances_and_positions():
    pass


@pytest.mark.asyncio
async def test_get_cme_first_notice_date():
    pass


if __name__ == "__main__":
    pytest.main()
