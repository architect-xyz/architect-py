# Generated by ariadne-codegen
# Source: schema.graphql

from enum import Enum


class AccountMode(str, Enum):
    LIVE = "LIVE"
    PAPER = "PAPER"


class AlgoControlCommand(str, Enum):
    START = "START"
    PAUSE = "PAUSE"
    STOP = "STOP"


class AlgoKind(str, Enum):
    MARKET_MAKER = "MARKET_MAKER"
    POV = "POV"
    SMART_ORDER_ROUTER = "SMART_ORDER_ROUTER"
    TWAP = "TWAP"
    SPREADER = "SPREADER"
    CHASER = "CHASER"
    SPREAD = "SPREAD"


class AlgoRunningStatus(str, Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    DONE = "DONE"


class CandleWidth(str, Enum):
    ONE_SECOND = "ONE_SECOND"
    FIVE_SECOND = "FIVE_SECOND"
    ONE_MINUTE = "ONE_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    ONE_HOUR = "ONE_HOUR"
    ONE_DAY = "ONE_DAY"


class CmeSecurityType(str, Enum):
    CASH = "CASH"
    COMBO = "COMBO"
    FRA = "FRA"
    FUT = "FUT"
    FWD = "FWD"
    IDX = "IDX"
    INDEX = "INDEX"
    IRS = "IRS"
    OOC = "OOC"
    OOF = "OOF"


class CreateOrderType(str, Enum):
    LIMIT = "LIMIT"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"


class CreateTimeInForceInstruction(str, Enum):
    GTC = "GTC"
    GTD = "GTD"
    IOC = "IOC"
    DAY = "DAY"
    FOK = "FOK"


class EnvironmentKind(str, Enum):
    PLATFORM = "PLATFORM"
    BROKERAGE = "BROKERAGE"


class EventContractsType(str, Enum):
    SINGLE = "SINGLE"
    DUAL = "DUAL"


class FillKind(str, Enum):
    NORMAL = "NORMAL"
    REVERSAL = "REVERSAL"
    CORRECTION = "CORRECTION"


class LicenseTier(str, Enum):
    BASIC = "BASIC"
    PROFESSIONAL = "PROFESSIONAL"


class MMAlgoKind(str, Enum):
    MM = "MM"
    SPREAD = "SPREAD"


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


class OrderStateFlags(str, Enum):
    OPEN = "OPEN"
    REJECTED = "REJECTED"
    ACKED = "ACKED"
    FILLED = "FILLED"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"
    OUT = "OUT"
    STALE = "STALE"


class ParentOrderKind(str, Enum):
    ALGO = "ALGO"
    ORDER = "ORDER"


class Reason(str, Enum):
    ALGO_PAUSED = "ALGO_PAUSED"
    ALGO_STOPPED = "ALGO_STOPPED"
    MIN_POSITION = "MIN_POSITION"
    MAX_POSITION = "MAX_POSITION"
    WITHIN_FILL_LOCKOUT = "WITHIN_FILL_LOCKOUT"
    WITHIN_REJECT_LOCKOUT = "WITHIN_REJECT_LOCKOUT"
    WITHIN_ORDER_LOCKOUT = "WITHIN_ORDER_LOCKOUT"
    NO_REFERENCE_PRICE = "NO_REFERENCE_PRICE"
    NO_REFERENCE_SIZE = "NO_REFERENCE_SIZE"
    NO_BID = "NO_BID"
    NO_ASK = "NO_ASK"
    OPEN_ORDER_WITHIN_TOLERANCE = "OPEN_ORDER_WITHIN_TOLERANCE"
    OPEN_ORDER_OUTSIDE_TOLERANCE = "OPEN_ORDER_OUTSIDE_TOLERANCE"
    CANCEL_PENDING = "CANCEL_PENDING"


class ReferencePrice(str, Enum):
    MID = "MID"
    BID_ASK = "BID_ASK"
    HEDGE_MARKET_BID_ASK = "HEDGE_MARKET_BID_ASK"


class UserTier(str, Enum):
    PLATFORM = "PLATFORM"
    BROKERAGE_UNSUBSCRIBED = "BROKERAGE_UNSUBSCRIBED"
    BROKERAGE_BASIC = "BROKERAGE_BASIC"
    BROKERAGE_PROFESSIONAL = "BROKERAGE_PROFESSIONAL"
    STAFF = "STAFF"
