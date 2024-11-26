import asyncio
import os
import pytest
from architect_py.async_client import AsyncClient
from architect_py.client import Client
from architect_py.graphql_client.enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
    OrderStateFlags,
)
from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.utils.dt import get_expiration_from_CME_name
from architect_py.scalars import OrderDir
from decimal import Decimal

from architect_py.utils.nearest_tick import TickRoundMethod

from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor


@pytest.fixture(scope="session", autouse=True)
def test_load_env():
    load_dotenv()
    global HOST, ACCOUNT, API_KEY, API_SECRET, PORT
    HOST = os.getenv("HOST")
    ACCOUNT = os.getenv("ACCOUNT")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    if HOST == "app.architect.co":
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )

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


def test_sync_search_markets():
    l = 5
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = client.search_markets(glob="ES*", venue="CME")
    assert len(markets) > l

    markets = client.search_markets(glob="GC*", venue="CME")
    assert len(markets) > l

    markets = client.search_markets(glob="NQ*", venue="CME", sort_by_volume_desc=True)
    assert len(markets) > l

    for i in range(10):
        markets = client.search_markets(
            search_string="NQ", venue="CME", sort_by_volume_desc=True, max_results=l
        )
        assert len(markets) == l


@pytest.mark.asyncio
async def test_search_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    markets = await client.search_markets(glob="ES*", venue="CME")
    assert len(markets) > 5

    markets = await client.search_markets(glob="GC*", venue="CME")
    assert len(markets) > 5

    markets = await client.search_markets(
        glob="NQ*", venue="CME", sort_by_volume_desc=True
    )
    assert len(markets) > 5


@pytest.mark.asyncio
async def test_find_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    markets = await client.search_markets(glob="ES*", venue="CME")
    markets = client.find_markets(base=markets[0].name, venue="CME")

    assert markets is not None


@pytest.mark.asyncio
async def test_subscribe_book_snapshots():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


@pytest.mark.asyncio
async def test_subscribe_trades():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = await client.search_markets(
        search_string="", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]

    i = 0
    async for trade in client.subscribe_trades(market.name):
        assert trade is not None
        i += 1

        if i == 5:
            break


@pytest.mark.asyncio
async def test_get_open_orders():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    orders = await client.get_open_orders()

    assert orders is not None


@pytest.mark.asyncio
async def test_send_limit_order():
    # check that sending strings for decimals works
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = await client.search_markets(
        search_string="ES", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]

    snapshot = await client.get_market_snapshot(market.id)
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
        market=market.id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        order_type=order_type,
        post_only=True,
        limit_price=price,
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.DAY,
        price_round_method=TickRoundMethod.TOWARD_ZERO,
        wait_for_confirm=False,
    )

    assert order is not None
    order_id = order.order.id

    assert order is not None
    assert order.reject_reason is None
    cancel = await client.cancel_order(order_id)
    assert cancel is not None

    order = await client.get_order(order_id)

    assert order is not None
    assert OrderStateFlags.OUT in order.order_state

    order = await client.send_limit_order(
        market=market.id,
        odir=OrderDir.BUY,
        quantity="1",  # type: ignore  # we do this on purpose to test that sending strings works
        order_type=order_type,
        post_only=True,
        limit_price=price,  # type: ignore  # we do this on purpose to test that sending strings works
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.GTC,
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
        market=market.id,
        odir=OrderDir.BUY,
        quantity=Decimal(-1),
        order_type=order_type,
        post_only=True,
        limit_price=price,
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.GTC,
        price_round_method=TickRoundMethod.TOWARD_ZERO,
    )

    assert order is not None


def test_sync_market_order():
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = client.search_markets(
        search_string="MES", venue="CME", sort_by_volume_desc=True
    )
    market = markets[0]
    market_id = market.id

    order = client.send_market_pro_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.IOC,
        fraction_through_market=Decimal(0.0005),
    )

    assert order is not None
    order_id = order.order.id
    order = client.get_order(order_id)
    assert order is not None
    assert order.reject_reason is None

    cancel = client.cancel_order(order_id)
    assert cancel is not None


@pytest.mark.asyncio
async def test_market_pro_order():
    # check that sending strings for decimals works
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = await client.search_markets(glob="MES*", venue="CME")
    market = markets[0]
    market_id = market.id

    order = await client.send_market_pro_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=Decimal(1),
        account=ACCOUNT,
        time_in_force_instruction=CreateTimeInForceInstruction.GTC,
        fraction_through_market=Decimal(0.0005),
    )

    await asyncio.sleep(0.2)

    assert order is not None
    order_id = order.order.id
    order = await client.get_order(order_id)
    assert order is not None
    assert order.reject_reason is None

    cancel = await client.cancel_order(order_id)
    assert cancel is not None


@pytest.mark.asyncio
async def test_send_twap_algo():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


@pytest.mark.asyncio
async def test_send_pov_algo():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


@pytest.mark.asyncio
async def test_send_smart_order_router_algo():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


@pytest.mark.asyncio
async def test_preview_smart_order_router():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


@pytest.mark.asyncio
async def test_send_mm_algo():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)


def sync_get_cme_futures_series():
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    series = client.get_cme_futures_series("ES")
    assert series is not None
    return series


@pytest.mark.asyncio
async def test_get_cme_futures_series():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    series = await client.get_cme_futures_series("ES")

    with ThreadPoolExecutor() as executor:
        future = executor.submit(sync_get_cme_futures_series)
        series_sync = future.result()

    assert series is not None
    assert series == series_sync


@pytest.mark.asyncio
async def test_get_cme_future_from_root_month_year():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    markets = await client.search_markets(glob="ES*", venue="CME")
    market = markets[0]
    assert market.name.startswith("ES")

    expiration = get_expiration_from_CME_name(market.name)

    fut = await client.get_cme_future_from_root_month_year(
        "ES", month=expiration.month, year=expiration.year
    )

    assert fut == market


def sync_get_account_summaries():
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    summaries = client.get_account_summaries()

    assert summaries is not None
    return summaries


@pytest.mark.asyncio
async def test_get_account_summaries():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    summaries = await client.get_account_summaries()

    with ThreadPoolExecutor() as executor:
        future = executor.submit(sync_get_account_summaries)
        summaries_sync = future.result()

    assert summaries is not None
    assert summaries == summaries_sync


def sync_get_balances_and_positions():
    client_sync = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    balances = client_sync.get_balances_and_positions()

    assert balances is not None

    return balances


@pytest.mark.asyncio
async def test_get_balances_and_positions():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)

    balances = await client.get_balances_and_positions()

    with ThreadPoolExecutor() as executor:
        future = executor.submit(sync_get_balances_and_positions)
        balances_sync = future.result()

    assert balances is not None
    assert balances == balances_sync


def sync_get_cme_first_notice_date():
    client = Client(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    name = "GC"

    markets = client.search_markets(glob=f"{name}*", venue="CME")
    nearest_market = markets[0]
    d = get_expiration_from_CME_name(nearest_market.name)
    for market in markets:
        d2 = get_expiration_from_CME_name(market.name)
        if d2 < d:
            d = d2
            nearest_market = market

    notice_date = client.get_cme_first_notice_date(nearest_market.id)

    assert markets is not None
    assert len(markets) > 5, f"There should be more than 5 {name} futures contracts"
    assert nearest_market.name.startswith(name)
    assert notice_date is not None
    assert notice_date < d

    return nearest_market, notice_date


@pytest.mark.asyncio
async def test_get_cme_first_notice_date():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET, port=PORT)
    name = "GC"

    markets = await client.search_markets(glob=f"{name}*", venue="CME")
    nearest_market = markets[0]
    d = get_expiration_from_CME_name(nearest_market.name)
    for market in markets:
        d2 = get_expiration_from_CME_name(market.name)
        if d2 < d:
            d = d2
            nearest_market = market

    notice_date = await client.get_cme_first_notice_date(nearest_market.id)

    assert markets is not None
    assert len(markets) > 5, f"There should be more than 5 {name} futures contracts"
    assert nearest_market.name.startswith(name)
    assert notice_date is not None
    assert notice_date < d

    with ThreadPoolExecutor() as executor:
        future = executor.submit(sync_get_cme_first_notice_date)
        notice_date_sync = future.result()

    assert (nearest_market, notice_date) == notice_date_sync


if __name__ == "__main__":
    pytest.main()
