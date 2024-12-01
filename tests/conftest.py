import os

import pytest_asyncio
from architect_py.async_client import AsyncClient
from dotenv import load_dotenv


@pytest_asyncio.fixture
async def async_client():
    load_dotenv()

    host = os.getenv("ARCHITECT_HOST") or "localhost"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    # test_account = os.getenv("ARCHITECT_TEST_ACCOUNT")

    if host == "app.architect.co":
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
