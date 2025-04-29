"""
Tests for architect-py can be run against any particular environment.

Set the following environments variables before running pytest:

- ARCHITECT_ENDPOINT
- ARCHITECT_API_KEY
- ARCHITECT_API_SECRET
- ARCHITECT_PAPER_TRADING

Optional environment varaibles:

- ARCHITECT_GRAPHQL_PORT (default=4567)
- DANGEROUS_ALLOW_LIVE_TRADING (default=False)

Environment variables may be set in a `.env` file.
"""

import os

import pytest_asyncio
from dotenv import load_dotenv

from architect_py import AsyncClient


def is_truthy(value: str | None) -> bool:
    return value is not None and value.lower() in ("1", "true", "yes")


class TestEnvironment:
    @classmethod
    def from_env(cls):
        endpoint = os.getenv("ARCHITECT_ENDPOINT")
        api_key = os.getenv("ARCHITECT_API_KEY")
        api_secret = os.getenv("ARCHITECT_API_SECRET")

        assert endpoint is not None
        assert api_key is not None
        assert api_secret is not None

        paper_trading = is_truthy(os.getenv("ARCHITECT_PAPER_TRADING"))
        dangerous_allow_live_trading = is_truthy(
            os.getenv("DANGEROUS_ALLOW_LIVE_TRADING")
        )
        graphql_port = os.getenv("ARCHITECT_GRAPHQL_PORT")
        if graphql_port is not None:
            graphql_port = int(graphql_port)

        if not paper_trading and not dangerous_allow_live_trading:
            raise ValueError(
                "You must set ARCHITECT_PAPER_TRADING=True or DANGEROUS_ALLOW_LIVE_TRADING=True to run live tests"
            )

        return cls(
            endpoint=endpoint,
            api_key=api_key,
            api_secret=api_secret,
            paper_trading=paper_trading,
            graphql_port=graphql_port,
        )

    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str,
        api_secret: str,
        paper_trading: bool,
        graphql_port: int | None,
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_trading = paper_trading
        self.graphql_port = graphql_port


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    load_dotenv()
    test_env = TestEnvironment.from_env()
    async_client = await AsyncClient.connect(
        api_key=test_env.api_key,
        api_secret=test_env.api_secret,
        paper_trading=test_env.paper_trading,
        endpoint=test_env.endpoint,
        graphql_port=test_env.graphql_port,
    )

    marketdata_endpoints = (("BINANCE/USDM", "usdm.binance.marketdata.architect.co"),)
    for venue, endpoint in marketdata_endpoints:
        await async_client.set_marketdata(venue, endpoint)

    return async_client


@pytest_asyncio.fixture
async def front_ES_future(async_client: AsyncClient) -> str:
    """
    Fixture for getting the name of the front month ES CME future.
    """
    series = await async_client.get_cme_futures_series("ES CME Futures")
    series.sort()
    return series[-1][1]


@pytest_asyncio.fixture
async def front_ES_future_usd(async_client: AsyncClient) -> str:
    """
    Fixture for getting the name of the front month ES CME future/USD pair.
    """
    series = await async_client.get_cme_futures_series("ES CME Futures")
    series.sort()
    future = series[-1][1]
    return f"{future}/USD"


# CR alee: add sync Client tests
