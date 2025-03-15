import os

import pytest
import pytest_asyncio
from architect_py.client import Client
from architect_py.async_client import AsyncClient
from dotenv import load_dotenv

from architect_py.async_client import AsyncClient


"""
if you have a file named ".env" in your working directory with:

ARCHITECT_API_KEY=your_key
ARCHITECT_API_SECRET=your_secret
PAPER_TRADING=False
"""


def is_truthy(value: str | None) -> bool:
    return value is not None and value.lower() in ("1", "true", "yes")


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    load_dotenv()

    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = os.getenv(key="ARCHITECT_PORT")
    if port is not None:
        port = int(port)

    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    paper_trading = os.getenv("ARCHITECT_PAPER_TRADING")
    if paper_trading is None:
        paper_trading = True
    else:
        paper_trading = is_truthy(paper_trading)

    dangerous_allow_app_architect_co = os.getenv("DANGEROUS_ALLOW_APP_ARCHITECT_CO")

    if host == "app.architect.co" and not is_truthy(dangerous_allow_app_architect_co):
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )
    if api_key is None or api_secret is None:
        raise ValueError(
            "You must set ARCHITECT_API_KEY and ARCHITECT_API_SECRET to run tests"
        )

    return await AsyncClient.connect(
        host=host,
        _port=port,
        api_key=api_key,
        api_secret=api_secret,
        paper_trading=paper_trading,
    )


@pytest.fixture
def sync_client():
    load_dotenv()
    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = os.getenv(key="ARCHITECT_PORT")
    if port is not None:
        port = int(port)

    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")

    paper_trading = os.getenv("ARCHITECT_PAPER_TRADING")
    if paper_trading is None:
        paper_trading = True
    else:
        paper_trading = is_truthy(paper_trading)

    dangerous_allow_app_architect_co = os.getenv("DANGEROUS_ALLOW_APP_ARCHITECT_CO")

    if host == "app.architect.co" and not is_truthy(dangerous_allow_app_architect_co):
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )
    if api_key is None or api_secret is None:
        raise ValueError(
            "You must set ARCHITECT_API_KEY and ARCHITECT_API_SECRET to run tests"
        )
    return Client(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        _port=port,
        paper_trading=paper_trading,
    )


@pytest_asyncio.fixture
async def front_ES_future(async_client: AsyncClient) -> str:
    series = await async_client.get_cme_futures_series("ES CME Futures")

    return series[0][1]


@pytest_asyncio.fixture
async def front_ES_future_tp(async_client: AsyncClient) -> str:
    series = await async_client.get_cme_futures_series("ES CME Futures")

    return f"{series[0][1]}/USD"
