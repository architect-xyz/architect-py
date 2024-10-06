from architect_py.async_client import AsyncClient
from architect_py.client import Client
from dotenv import load_dotenv
import os


def create_client():
    load_dotenv()
    host = os.environ["ARCHITECT_HOST"]
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    implicit_use_tls = api_key is not None or api_secret is not None
    explicit_use_tls = os.getenv("ARCHITECT_USE_TLS")
    use_tls = False
    if explicit_use_tls == "true" or explicit_use_tls == "1":
        use_tls = True
    elif explicit_use_tls is None:
        use_tls = implicit_use_tls

    c = Client(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        use_tls=use_tls,
    )
    return c


def create_async_client():
    load_dotenv()
    host = os.environ["ARCHITECT_HOST"]
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    implicit_use_tls = api_key is not None or api_secret is not None
    explicit_use_tls = os.getenv("ARCHITECT_USE_TLS")
    use_tls = False
    if explicit_use_tls == "true" or explicit_use_tls == "1":
        use_tls = True
    elif explicit_use_tls is None:
        use_tls = implicit_use_tls

    c = AsyncClient(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        use_tls=use_tls,
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
