import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, Literal, Optional, TypeVar


@dataclass(kw_only=True)
class QueryL2BookSnapshot:
    market_id: uuid.UUID


@dataclass(kw_only=True)
class L2BookSnapshot:
    timestamp: datetime
    epoch: datetime
    seqno: int
    bids: list[tuple[Decimal, Decimal]]
    asks: list[tuple[Decimal, Decimal]]


@dataclass(kw_only=True)
class QueryL3BookSnapshot:
    market_id: uuid.UUID


@dataclass(kw_only=True)
class L3Order:
    price: Decimal
    size: Decimal

    def __init__(self, *, price: Decimal, size: Decimal, **kwargs):
        self.price = price
        self.size = size
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass(kw_only=True)
class L3BookSnapshot:
    timestamp: datetime
    epoch: datetime
    seqno: int
    bids: list[L3Order]
    asks: list[L3Order]


@dataclass(kw_only=True)
class CandleV1:
    time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    buy_volume: Decimal
    sell_volume: Decimal


@dataclass(kw_only=True)
class TradeV1:
    time: Optional[datetime]
    direction: Optional[Literal["Buy", "Sell"]]
    price: Decimal
    size: Decimal

    def __init__(
        self,
        *,
        time: Optional[datetime],
        direction: Optional[Literal["Buy", "Sell"]],
        price: Decimal,
        size: Decimal,
        **kwargs
    ):
        self.time = time
        self.direction = direction
        self.price = price
        self.size = size
        for k, v in kwargs.items():
            setattr(self, k, v)
