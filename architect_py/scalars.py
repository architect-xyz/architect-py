from enum import Enum
from typing import Literal


"""
Custom Serialize / Deserializing functions for the scalars
"""


def serialize(value):
    return value.serialize()


def deserialize(value):
    return value.deserialize(value)


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
    def deserialize(cls, value: str) -> "OrderDir":
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
