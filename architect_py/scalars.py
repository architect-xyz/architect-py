from enum import Enum


"""
Custom Serialize / Deserializing functions for the scalars

Decimal does not need one

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

    def __str__(self) -> str:
        return f"Dir.{self.name}"

    def __repr__(self) -> str:
        return f"Dir.{self.name}"

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @classmethod
    def from_string(cls, value):
        if value.lower() == "buy":
            return cls.BUY
        elif value.lower() == "sell":
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    @classmethod
    def from_unit(cls, value):
        if value == 1:
            return cls.BUY
        elif value == -1:
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    @classmethod
    def from_sign(cls, value):
        if value > 0:
            return cls.BUY
        elif value < 0:
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    @classmethod
    def deserialize(cls, value):
        if value == "buy":
            return cls.BUY
        elif value == "sell":
            return cls.SELL
        else:
            raise ValueError(f"Unknown Dir: {value}")

    def serialize(self):
        return self.value
