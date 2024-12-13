import pytest

from architect_py.async_client import AsyncClient, OrderDir


@pytest.mark.asyncio
async def test_orderflow_session(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_market_pro_order(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    "market_id",
    [
        "BTC Crypto/USDC Crypto*BINANCE/DIRECT",
        # "ETH Crypto/USDC Crypto*BINANCE/DIRECT",
    ],
)
async def test_basic_order(async_client: AsyncClient, market_id: str):
    # Assert market is available
    market = await async_client.get_market(market_id)
    assert market is not None, f"Market does not exist for {market_id}"

    # Hopefully we get some btc at this price!
    limit_price = 10.00

    # Make a very cheap
    order = await async_client.send_limit_order(
        market=market.id,
        odir=OrderDir.BUY,
        quantity=market.min_order_quantity,
        limit_price=limit_price,
    )

    assert order is not None
