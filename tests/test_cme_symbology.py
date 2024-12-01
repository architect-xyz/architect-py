import re

import pytest
from architect_py.async_client import AsyncClient


@pytest.mark.asyncio
async def test_search_for_es_front_month(async_client: AsyncClient):
    series = await async_client.get_cme_futures_series("ES")
    assert len(series) > 0, "no futures markets found in ES series"
    _, front_month_future = series[0]
    assert re.match(
        r"ES \d* CME Future", front_month_future.kind.base.name
    ), "front month future base name does not match regex"
    assert (
        front_month_future.kind.quote.name == "USD"
    ), "front month future quote is not USD"


@pytest.mark.asyncio
async def test_popular_cme_futures_exist(async_client: AsyncClient):
    markets = await async_client.search_markets(venue="CME")
    popular_series = ["ES", "GC", "NQ"]
    for series in popular_series:
        futures = [market for market in markets if market.kind.base.name.startswith(f"{series} ")]
        assert len(futures) > 1, f"not enough futures markets found in {series} series"
