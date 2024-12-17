import logging

import pytest

from architect_py.async_client import AsyncClient, OrderDir


@pytest.mark.asyncio
async def test_orderflow_session(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_market_pro_order(async_client: AsyncClient):
    pass


@pytest.mark.live_orderflow
@pytest.mark.asyncio
@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    "market_id",
    [
        "BTC Crypto/USDT Crypto*BINANCE/DIRECT",
        "ETH Crypto/USDT Crypto*BINANCE/DIRECT",
    ],
)
async def test_live_market_order(async_client: AsyncClient, market_id: str):
    # Get snapshot
    market = await async_client.get_market(market_id)
    assert market is not None, f"Market does not exist for {market_id}"

    snapshot = await async_client.get_market_snapshot(market_id)
    assert snapshot is not None, f"Snapshot does not exist for {market_id}"

    # Make a very cheap
    order = await async_client.send_limit_order(
        market=market_id,
        odir=OrderDir.BUY,
        quantity=market.min_order_quantity
        * 10,  # not sure what's going here with min qty not being accurate
        limit_price=snapshot.ask_price * 1.15,
    )

    assert order is not None
