# generated by datamodel-codegen:
#   filename:  Folio_HistoricalOrdersResponse.json
#   timestamp: 2025-02-26T07:59:56+00:00

from __future__ import annotations

from enum import Enum
from typing import Annotated, List

from msgspec import Meta, Struct


class Dir(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class K(Enum):
    LIMIT = 'LIMIT'


class K1(Enum):
    STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'


class K2(Enum):
    TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class OrderRejectReason(Enum):
    DuplicateOrderId = 'DuplicateOrderId'
    NotAuthorized = 'NotAuthorized'
    NoExecutionVenue = 'NoExecutionVenue'
    NoAccount = 'NoAccount'
    NoCpty = 'NoCpty'
    UnsupportedOrderType = 'UnsupportedOrderType'
    UnsupportedExecutionVenue = 'UnsupportedExecutionVenue'
    Unknown = 'Unknown'


class OrderSource(Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3
    integer_4 = 4
    integer_5 = 5
    integer_255 = 255


class OrderStatus(Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_127 = 127
    integer_128 = 128
    integer_129 = 129
    integer_254 = 254


class TimeInForce1(Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'


class TimeInForce2(Struct):
    GTD: str


class TimeInForce3(Enum):
    DAY = 'DAY'


class Order1(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[str, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[
        TimeInForce1 | TimeInForce2 | TimeInForce3, Meta(title='time_in_force')
    ]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[str, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[str, Meta(title='filled_quantity')]
    k: K
    p: Annotated[str, Meta(title='limit_price')]
    po: Annotated[bool, Meta(title='post_only')]
    pid: Annotated[OrderId | None, Meta(title='parent_id')] | None = None
    r: Annotated[OrderRejectReason | None, Meta(title='reject_reason')] | None = None
    rm: Annotated[str | None, Meta(title='reject_message')] | None = None
    xp: Annotated[str | None, Meta(title='average_fill_price')] | None = None


class Order2(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[str, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[
        TimeInForce1 | TimeInForce2 | TimeInForce3, Meta(title='time_in_force')
    ]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[str, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[str, Meta(title='filled_quantity')]
    k: K1
    p: Annotated[str, Meta(title='limit_price')]
    tp: Annotated[str, Meta(title='trigger_price')]
    pid: Annotated[OrderId | None, Meta(title='parent_id')] | None = None
    r: Annotated[OrderRejectReason | None, Meta(title='reject_reason')] | None = None
    rm: Annotated[str | None, Meta(title='reject_message')] | None = None
    xp: Annotated[str | None, Meta(title='average_fill_price')] | None = None


class Order3(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[str, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[
        TimeInForce1 | TimeInForce2 | TimeInForce3, Meta(title='time_in_force')
    ]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[str, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[str, Meta(title='filled_quantity')]
    k: K2
    p: Annotated[str, Meta(title='limit_price')]
    tp: Annotated[str, Meta(title='trigger_price')]
    pid: Annotated[OrderId | None, Meta(title='parent_id')] | None = None
    r: Annotated[OrderRejectReason | None, Meta(title='reject_reason')] | None = None
    rm: Annotated[str | None, Meta(title='reject_message')] | None = None
    xp: Annotated[str | None, Meta(title='average_fill_price')] | None = None


class HistoricalOrdersResponse(Struct):
    orders: List[Order1 | Order2 | Order3]
