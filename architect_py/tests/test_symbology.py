import re
from datetime import datetime

import pytest
from architect_py.async_client import AsyncClient
from dateutil.relativedelta import relativedelta

from architect_py.graphql_client.fragments import MarketFieldsKindExchangeMarketKind


@pytest.mark.asyncio
async def test_futures_series_populated(async_client: AsyncClient):
    markets = await async_client.search_markets(venue="CME")
    # list of popular CME futures series and the minimum
    # number of futures we expect to see per series
    popular_series = [("ES", 5), ("GC", 5), ("NQ", 5)]
    for series, min_count in popular_series:

        futures = [
            market
            for market in markets
            if isinstance(market.kind, MarketFieldsKindExchangeMarketKind)
            and market.kind.base.name.startswith(f"{series} ")
        ]
        assert (
            len(futures) > min_count
        ), f"not enough futures markets found in {series} series"


@pytest.mark.asyncio
async def test_search_for_es_front_month(async_client: AsyncClient):
    series = await async_client.get_cme_futures_series("ES")
    assert len(series) > 0, "no futures markets found in ES series"
    _, front_month_future = series[0]
    if isinstance(front_month_future.kind, MarketFieldsKindExchangeMarketKind):
        front_month_future.kind
        assert re.match(
            r"ES \d* CME Future", front_month_future.kind.base.name
        ), "front month future base name does not match regex"
        assert (
            front_month_future.kind.quote.name == "USD"
        ), "front month future quote is not USD"


@pytest.mark.asyncio
async def test_get_cme_future_from_root_month_year(async_client: AsyncClient):
    # BTC futures are monthly.  To avoid end-of-month weekend expiration,
    # check the next month from the current date.
    now = datetime.now() + relativedelta(months=+1)
    month = now.month
    year = now.year
    future = await async_client.get_cme_future_from_root_month_year(
        "BTC", month=month, year=year
    )

    assert isinstance(future.kind, MarketFieldsKindExchangeMarketKind)
    assert re.match(
        f"BTC {year}{month:02d}[0-9]{{2}} CME Future", future.kind.base.name
    ), "future base name does not match regex"


@pytest.mark.asyncio
async def test_cme_first_notice_date(async_client: AsyncClient):
    # Find the nearest GC futures contract and check the first notice date
    futures = await async_client.get_cme_futures_series("GC")
    exp_date, future = futures[0]
    notice_date = await async_client.get_cme_first_notice_date(future.id)
    assert notice_date is not None, "first notice date is None"
    assert notice_date < exp_date, "first notice date is not before expiration"
