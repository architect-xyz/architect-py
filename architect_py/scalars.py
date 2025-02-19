from enum import Enum
from typing import Literal, Optional, TypeVar

from datetime import datetime, timezone

from architect_py.graphql_client.base_model import UnsetType


"""
Custom Serialize / Deserializing functions for the scalars
"""


def serialize(value) -> str:
    return value.serialize()


class TradableProduct(str):
    def __new__(cls, value: str) -> "TradableProduct":
        assert (
            "/" in value
        ), f"TradableProduct must be in the form of 'base/quote'. Got: {value}"
        return super().__new__(cls, value)

    def serialize(self) -> str:
        return self

    @classmethod
    def parse(cls, value: str) -> "TradableProduct":
        return cls(value)

    @property
    def base_quote(self) -> list[str]:
        return self.split("/")

    @property
    def base(self) -> str:
        return self.split("/")[0]

    @property
    def quote(self) -> str:
        return self.split("/")[1]


def parse_tradable_product(value: str) -> TradableProduct:
    return TradableProduct(value)


class OrderDir(Enum):
    BUY = "buy"
    SELL = "sell"

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

    @classmethod
    def parse(cls, value: str) -> "OrderDir":
        if value == "buy":
            return cls.BUY
        elif value == "sell":
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    def serialize(self) -> str:
        return self.value

    def __str__(self) -> str:
        return f"Dir.{self.name}"

    def __repr__(self) -> str:
        return f"Dir.{self.name}"

    def __eq__(self, other) -> bool:
        return self.value == other.value

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


def convert_datetime_to_utc_str(dt: Optional[datetime] | UnsetType):
    if dt is None or isinstance(dt, UnsetType):
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
