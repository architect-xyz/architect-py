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
    # list of popular CME futures series and the minimum
    # number of futures we expect to see per series
    popular_series = [("ES", 5), ("GC", 5), ("NQ", 5)]
    for series, min_count in popular_series:
        futures = [
            market
            for market in markets
            if market.kind.base.name.startswith(f"{series} ")
        ]
        assert (
            len(futures) > min_count
        ), f"not enough futures markets found in {series} series"
