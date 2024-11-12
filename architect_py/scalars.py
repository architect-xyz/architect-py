from enum import Enum


"""
Custom Serialize / Deserializing functions for the scalars

Decimal does not need one

"""


def serialize(value):
    return value.serialize()


def deserialize(value):
    return AccountId.deserialize(value)


class AccountId:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("AccountId must be a string.")
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"AccountId({self.value})"

    def __eq__(self, other):
        return self.value == other.value

    def to_string(self):
        return str(self.value)

    @classmethod
    def from_string(cls, value):
        return cls(value)

    @classmethod
    def deserialize(cls, value):
        return cls(value)

    def serialize(self):
        return self.value


class OrderId:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("OrderId must be a string.")
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"OrderId({self.value})"

    def __eq__(self, other):
        return self.value == other.value

    def to_string(self):
        return str(self.value)

    @classmethod
    def from_string(cls, value):
        return cls(value)


class Dir(Enum):
    BUY = "buy"
    SELL = "sell"

    def __int__(self):
        if self == Dir.BUY:
            return 1
        elif self == Dir.SELL:
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
        if value == "buy":
            return cls.BUY
        elif value == "sell":
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
