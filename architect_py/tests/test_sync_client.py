from dotenv import load_dotenv

from architect_py import Client
from architect_py.tests.conftest import GetEnvironment


def test_sync_client():
    load_dotenv()
    test_env = GetEnvironment.from_env()
    client = Client(
        api_key=test_env.api_key,
        api_secret=test_env.api_secret,
        paper_trading=test_env.paper_trading,
        endpoint=test_env.endpoint,
        graphql_port=test_env.graphql_port,
    )

    symbols = client.list_symbols(marketdata="CME")

    assert symbols is not None
    assert len(symbols) > 20

    client.close()


def test_creation():
    load_dotenv()
    test_env = GetEnvironment.from_env()
    client = Client(
        api_key=test_env.api_key,
        api_secret=test_env.api_secret,
        paper_trading=True,
        endpoint="app.architect.co",
    )

    symbols = client.list_symbols(marketdata="CME")

    assert symbols is not None
    assert len(symbols) > 20
    client.close()
