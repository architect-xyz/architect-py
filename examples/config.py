import os
from dataclasses import dataclass

from dotenv import load_dotenv

from architect_py import AsyncClient, Client


@dataclass
class Config:
    api_key: str
    api_secret: str
    paper_trading: bool
    endpoint: str


def load_config() -> Config:
    loaded = load_dotenv()

    if not loaded:
        raise ValueError(
            "⚠️  .env file not found or had no new variables\n\n"
            "Please create a .env file with the following variables:\n\n"
            "ARCHITECT_ENDPOINT=your_endpoint (e.g. app.architect.co)\n"
            "ARCHITECT_API_KEY=your_api_key (get from https://app.architect.co/user/account)\n"
            "ARCHITECT_API_SECRET=your_api_secret\n"
            "ARCHITECT_PAPER_TRADING=true/false\n"
        )

    endpoint = os.environ["ARCHITECT_ENDPOINT"]
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    paper_trading_str = os.getenv("ARCHITECT_PAPER_TRADING")
    paper_trading: bool = paper_trading_str is not None and (
        paper_trading_str.lower() == "true"
    )

    if api_key is None:
        raise ValueError("API key is required in .env file")

    if api_secret is None:
        raise ValueError("API secret is required in .env file")

    return Config(
        api_key,
        api_secret,
        paper_trading,
        endpoint,
    )


def connect_client():
    config = load_config()
    c = Client(
        endpoint=config.endpoint,
        api_key=config.api_key,
        api_secret=config.api_secret,
        paper_trading=config.paper_trading,
    )
    return c


async def connect_async_client():
    config = load_config()
    c = await AsyncClient.connect(
        endpoint=config.endpoint,
        api_key=config.api_key,
        api_secret=config.api_secret,
        paper_trading=config.paper_trading,
    )
    return c
