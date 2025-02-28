from decimal import Decimal

# generated by datamodel-codegen:
#   filename:  Algo_AlgoOrder_for_TwapAlgo.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Optional

from msgspec import Meta, Struct


class AlgoState(str, Enum):
    Pending = 'Pending'
    Running = 'Running'
    Stopped = 'Stopped'




class Dir(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


HumanDuration = str


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class TwapParams(Struct):
    dir: Dir
    end_time: str
    execution_venue: str
    interval: HumanDuration
    quantity: Decimal
    reject_lockout: HumanDuration
    symbol: str
    take_through_frac: Optional[Decimal] = None


class TwapStatus(Struct):
    quantity_filled: Decimal
    realized_twap: Optional[Decimal] = None


UserId = str


class AlgoOrderForTwapAlgo(Struct):
    account: str
    algo_name: str
    algo_order_id: OrderId
    create_time: str
    params: TwapParams
    state: AlgoState
    status: TwapStatus
    trader: UserId
    display_symbols: Optional[List[str]] = None
    last_error: Optional[str] = None
    last_error_time: Optional[str] = None
    parent_order_id: Optional[OrderId] = None
