import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from architect_py.async_client import AsyncClient


def is_truthy(value: str | None) -> bool:
    return value is not None and value.lower() in ("1", "true", "yes")


@pytest_asyncio.fixture
async def async_client():
    load_dotenv()

    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    # test_account = os.getenv("ARCHITECT_TEST_ACCOUNT")
    dangerous_allow_app_architect_co = os.getenv("DANGEROUS_ALLOW_APP_ARCHITECT_CO")

    if host == "app.architect.co" and not is_truthy(dangerous_allow_app_architect_co):
        raise ValueError(
            "You have set the HOST to the production server. Please change it to the sandbox server."
        )

    # if ACCOUNT is not None and "PAPER" in ACCOUNT:
    #     PORT = 6789
    # else:
    #     PORT = 4567

    async with AsyncClient(
        host=host, port=port, api_key=api_key, api_secret=api_secret
    ) as client:
        yield client


def pytest_addoption(parser):
    parser.addoption(
        "--live_orderflow",
        action="store_true",
        default=False,
        help="Run orderflow tests",
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "live_orderflow: runs live orders against Binance and other cptys")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--live_orderflow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_liveorderflow = pytest.mark.skip(reason="need --live_orderflow option to run")
    for item in items:
        if "live_orderflow" in item.keywords:
            item.add_marker(skip_liveorderflow)
