import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, Literal, Optional, TypeVar


@dataclass(kw_only=True)
class L2BookSnapshot:
    timestamp: datetime
    epoch: datetime
    seqno: int
    bids: list[tuple[Decimal, Decimal]]
    asks: list[tuple[Decimal, Decimal]]


@dataclass(kw_only=True)
class QueryL2BookSnapshot:
    market_id: uuid.UUID


@dataclass(kw_only=True)
class TradeV1:
    time: Optional[datetime]
    direction: Optional[Literal["Buy", "Sell"]]
    price: Decimal
    size: Decimal
