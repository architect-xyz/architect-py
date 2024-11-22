import pytest
from architect_py.async_client import AsyncClient
from architect_py.scalars import OrderDir
from decimal import Decimal


# Read variables from pytest configuration
def pytest_configure(config):
    global HOST, API_KEY, API_SECRET
    HOST = config.getoption("host")
    API_KEY = OrderDir[config.getoption("api_key")]
    API_SECRET = Decimal(config.getoption("api_secret"))


@pytest.mark.asyncio
async def test_client_init():
    try:
        client = AsyncClient(host=HOST, api_key=" ", api_secret=" ")
    except ValueError:
        pass
    try:
        client = AsyncClient(host=HOST, api_key="asdlfkja", api_secret=";alskjdf")
    except ValueError:
        pass

    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET)


@pytest.mark.asyncio
async def get_market():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET)
    markets = await client.search_markets(glob="ES*", venue="CME")
    name = markets[0].name

    market = await client.get_market(name)
    assert market is not None


@pytest.mark.asyncio
async def search_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET)
    markets = await client.search_markets(glob="ES*", venue="CME")
    assert len(markets) > 0


@pytest.mark.asyncio
async def find_markets():
    client = AsyncClient(host=HOST, api_key=API_KEY, api_secret=API_SECRET)
    markets = await client.search_markets(glob="ES*", venue="CME")
    markets = client.find_markets(base=markets[0].name, venue="CME")

    assert markets is not None


@pytest.mark.asyncio
async def subscribe_l1_book_snapshots():
    pass


@pytest.mark.asyncio
async def subscribe_l2_book_snapshots():
    pass


@pytest.mark.asyncio
async def subscribe_l3_book_snapshots():
    pass


@pytest.mark.asyncio
async def subscribe_trades():
    pass


@pytest.mark.asyncio
async def get_open_orders():
    pass


@pytest.mark.asyncio
async def send_limit_order():
    pass


@pytest.mark.asyncio
async def send_twap_algo():
    pass


@pytest.mark.asyncio
async def send_pov_algo():
    pass


@pytest.mark.asyncio
async def send_smart_order_router_algo():
    pass


@pytest.mark.asyncio
async def preview_smart_order_router():
    pass


@pytest.mark.asyncio
async def send_mm_algo():
    pass


@pytest.mark.asyncio
async def send_spread_algo():
    pass


@pytest.mark.asyncio
async def get_cme_futures_series():
    pass


@pytest.mark.asyncio
async def get_cme_future_from_root_month_year():
    pass


@pytest.mark.asyncio
async def get_balances_and_positions():
    pass


@pytest.mark.asyncio
async def get_cme_first_notice_date():
    pass


if __name__ == "__main__":
    pytest.main()
