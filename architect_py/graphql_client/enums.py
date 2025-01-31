# Generated by ariadne-codegen
# Source: schema.graphql

from enum import Enum


class CancelStatus(str, Enum):
    PENDING = "PENDING"
    ACKED = "ACKED"
    REJECTED = "REJECTED"


class CandleWidth(str, Enum):
    ONE_SECOND = "ONE_SECOND"
    FIVE_SECOND = "FIVE_SECOND"
    ONE_MINUTE = "ONE_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    ONE_HOUR = "ONE_HOUR"
    ONE_DAY = "ONE_DAY"


class FillKind(str, Enum):
    NORMAL = "NORMAL"
    REVERSAL = "REVERSAL"
    CORRECTION = "CORRECTION"


class MinOrderQuantityUnit(str, Enum):
    BASE = "BASE"
    QUOTE = "QUOTE"


class OrderSource(str, Enum):
    API = "API"
    GUI = "GUI"
    ALGO = "ALGO"
    EXTERNAL = "EXTERNAL"
    CLI = "CLI"
    TELEGRAM = "TELEGRAM"
    OTHER = "OTHER"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    ACKED = "ACKED"
    REJECTED = "REJECTED"
    OPEN = "OPEN"
    OUT = "OUT"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"
    STALE = "STALE"


class OrderType(str, Enum):
    LIMIT = "LIMIT"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"


class TimeInForce(str, Enum):
    GTC = "GTC"
    GTD = "GTD"
    DAY = "DAY"
    IOC = "IOC"
    FOK = "FOK"
