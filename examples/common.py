import os
from dataclasses import dataclass

from dotenv import load_dotenv

from architect_py.async_client import AsyncClient
from architect_py.client import Client


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
            "⚠️  .env file not found or had no new variables\n"
            "Please create a .env file with the following variables:\n"
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


buy_columns = "{:>15} {:>15} {:>15}"
sell_columns = "{:<15} {:<15} {:<15}"
green = "\033[32m"
red = "\033[31m"
normal = "\033[0m"


def print_book(book):
    print(
        (buy_columns + " " + sell_columns).format(
            "Total", "Size", "Bid", "Ask", "Size", "Total"
        )
    )
    for i in range(min(20, len(book.bids), len(book.asks))):
        b = book.bids[i]
        s = book.asks[i]
        print(
            (green + buy_columns).format(b.total, b.amount, b.price),
            (red + sell_columns).format(s.price, s.amount, s.total),
        )
    print(normal)


def print_open_orders(orders):
    if len(orders) == 0:
        print("No open orders")
    else:
        for o in orders:
            print(
                f"  • {o.order.market.name} {o.order.dir} {o.order.quantity} {o.order.order_type.limit_price}"
            )


def confirm(prompt: str):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(f"{prompt} [Y/N]? ").lower()
    return answer == "y"
