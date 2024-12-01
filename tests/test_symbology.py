import re

import pytest


@pytest.mark.asyncio
async def test_search_for_es_front_month(async_client):
    series = await async_client.get_cme_futures_series("ES")
    assert len(series) > 0, "no futures markets found in ES series"
    _, front_month_future = series[0]
    assert re.match(
        r"ES \d* CME Future", front_month_future.kind.base.name
    ), "front month future base name does not match regex"
    assert front_month_future.kind.quote.name == "USD", "front month future quote is not USD"
