from enum import Enum
from typing import Literal


class OrderDir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

    def flip(self) -> "OrderDir":
        """
        Returns the opposite direction.
        """
        if self == OrderDir.BUY:
            return OrderDir.SELL
        elif self == OrderDir.SELL:
            return OrderDir.BUY
        else:
            raise ValueError(f"Unknown Dir: {self}")

    def get_opposite(self) -> "OrderDir":
        """
        @deprecated(reason="Use flip instead")
        """
        return self.flip()

    def __int__(self):
        if self == OrderDir.BUY:
            return 1
        elif self == OrderDir.SELL:
            return -1
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
    """
    For ariadne-codegen
    """
    return value.lower()


def graphql_parse_order_dir(value: str) -> OrderDir:
    """
    For ariadne-codegen
    """
    if value == "buy":
        return OrderDir.BUY
    else:
        return OrderDir.SELL
