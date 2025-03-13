from enum import Enum
from typing import Literal, Optional

from datetime import datetime, timezone


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from architect_py.graphql_client.base_model import UnsetType


"""
Custom Serialize / Deserializing functions for the scalars
"""


def serialize(value) -> str:
    return value.serialize()


class TradableProduct(str):
    """
    Example instantiations:
        TradableProduct("ES 20250321 CME Future", "USD")
        TradableProduct("ES 20250321 CME Future/USD")
        (these are equivalent)

    This type exists to enforce the
    {base}/{quote} format for strings

    A base is the product that is being priced in terms of the quote.
    For example,
    "ES 20250321 CME Future/USD" means that the ES 20250321 CME Future is priced in USD.
    "ES 20250321 CME Future/EUR" means that the ES 20250321 CME Future is priced in EUR.
    "ES 20250321 CME Future/BTC" means that the ES 20250321 CME Future is priced in BTC
        (such a product does not exist on any exchange though).

    For example in a currency pair, the base is the first currency and the quote is the second currency.
    In the currency pair USD/EUR, USD is the base and EUR is the quote.
    USD/EUR = 1.1234 means that 1 USD = 1.1234 EUR
    EUR/USD = 0.8901 means that 1 EUR = 0.8901 USD
    """

    def __new__(
        cls, base_or_value: str, quote: Optional[str] = None
    ) -> "TradableProduct":
        """
        These are equivalent:
            TradableProduct("ES 20250321 CME Future", "USD")
            TradableProduct("ES 20250321 CME Future/USD")
        """
        if quote is None:
            value = base_or_value
        else:
            value = f"{base_or_value}/{quote}"

        assert (
            "/" in value
        ), f"TradableProduct must be in the form of 'base/quote'. Got: {base_or_value}"
        return super().__new__(cls, value)

    def base_quote(self) -> list[str]:
        return self.split("/")

    def base(self) -> str:
        return self.split("/", 1)[0]

    def quote(self) -> str:
        return self.split("/", 1)[1]


def parse_tradable_product(value: str) -> TradableProduct:
    # for ariadne
    return TradableProduct(value)


class OrderDir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

    def __int__(self):
        if self == OrderDir.BUY:
            return 1
        elif self == OrderDir.SELL:
            return -1
        else:
            raise ValueError(f"Unknown Dir: {self}")

    def get_opposite(self) -> "OrderDir":
        """
        NOTE: ENUMS ARE IMMUTABLE SO THIS DOES NOT MUTATE THE STATE OF THE ENUM
        """
        if self == OrderDir.BUY:
            return OrderDir.SELL
        elif self == OrderDir.SELL:
            return OrderDir.BUY
        else:
            raise ValueError(f"Unknown Dir: {self}")

    def __str__(self) -> str:
        return self.value
    
    def lower(self) -> str:
        return self.value.lower()
    
    @classmethod
    def from_string(cls, value: str) -> "OrderDir":
        lower = value.lower()
        if lower == "buy":
            return cls.BUY
        elif lower == "sell":
            return cls.SELL
        elif lower == "bid":
            return cls.BUY
        elif lower == "ask":
            return cls.SELL
        elif lower == "b":
            return cls.BUY
        elif lower == "a" or lower == "s":
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    @classmethod
    def from_unit(cls, value: Literal[1, -1]) -> "OrderDir":
        if value == 1:
            return cls.BUY
        elif value == -1:
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    @classmethod
    def from_sign(cls, value: int) -> "OrderDir":
        if value > 0:
            return cls.BUY
        elif value < 0:
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")


def graphql_serialize_order_dir(value: OrderDir) -> str:
    return value.lower()

def graphql_parse_order_dir(value: str) -> OrderDir:
    if value == "buy":
        return OrderDir.BUY
    else:
        return OrderDir.SELL



def convert_datetime_to_utc_str(dt: "Optional[datetime] | UnsetType") -> Optional[str]:
    if not isinstance(dt, datetime):
        return None

    if dt.tzinfo is None:
        raise ValueError(
            "in a datetime sent to the backend, the good_til_date must be timezone-aware. Try \n"
            "import pytz\n"
            "datetime(..., tzinfo={your_local_timezone}) or "
            "datetime.now(tz=pytz.timezone('UTC'))\n"
            "# examples of local timezones:\n"
            "pytz.timezone('US/Eastern'), "
            "pytz.timezone('US/Pacific'), pytz.timezone('US/Central')"
        )
    utc_str = dt.astimezone(timezone.utc).isoformat()[:-6]
    # [:-6] removes the utc offset

    return f"{utc_str}Z"
