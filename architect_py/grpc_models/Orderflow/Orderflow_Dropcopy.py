# generated by datamodel-codegen:
#   filename:  Orderflow_Dropcopy.json

from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional, Union

from msgspec import Meta, Struct


class T(Enum):
    o = 'o'


class K(Enum):
    LIMIT = 'LIMIT'


class K1(Enum):
    STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'


class K2(Enum):
    TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'


class T3(Enum):
    af = 'af'


Decimal = str


class Dir(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class FillKind(Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2


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


TimeInForce = Union[TimeInForce1, TimeInForce2, TimeInForce3]


UserId = str


class Dropcopy1(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: T
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: K
    p: Annotated[Decimal, Meta(title='limit_price')]
    po: Annotated[bool, Meta(title='post_only')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None


class Dropcopy2(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: T
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: K1
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None


class Dropcopy3(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: T
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: K2
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None


class Dropcopy4(Struct):
    d: Annotated[Dir, Meta(title='direction')]
    id: Annotated[str, Meta(title='fill_id')]
    k: Annotated[FillKind, Meta(title='fill_kind')]
    p: Annotated[Decimal, Meta(title='price')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    t: Annotated[int, Meta(title='is_taker')]
    tn: Annotated[int, Meta(ge=0, title='trade_time_ns')]
    ts: Annotated[
        int,
        Meta(description='When the cpty claims the trade happened', title='trade_time'),
    ]
    """
    When the cpty claims the trade happened
    """
    x: Annotated[str, Meta(title='execution_venue')]
    a: Optional[Annotated[Optional[str], Meta(title='account')]] = None
    atn: Optional[Annotated[Optional[int], Meta(ge=0, title='recv_time_ns')]] = None
    ats: Optional[
        Annotated[
            Optional[int],
            Meta(
                description='When Architect received the fill, if realtime',
                title='recv_time',
            ),
        ]
    ] = None
    """
    When Architect received the fill, if realtime
    """
    f: Optional[Annotated[Optional[Decimal], Meta(title='fee')]] = None
    fu: Optional[
        Annotated[
            Optional[str],
            Meta(
                description='Fee currency, if different from the price currency',
                title='fee_currency',
            ),
        ]
    ] = None
    """
    Fee currency, if different from the price currency
    """
    oid: Optional[Annotated[Optional[OrderId], Meta(title='order_id')]] = None
    u: Optional[Annotated[Optional[UserId], Meta(title='trader')]] = None
    xid: Optional[Annotated[Optional[str], Meta(title='exchange_fill_id')]] = None


class Dropcopy5(Struct):
    id: Annotated[str, Meta(title='fill_id')]
    t: T3
    x: Annotated[str, Meta(title='execution_venue')]
    a: Optional[Annotated[Optional[str], Meta(title='account')]] = None
    atn: Optional[Annotated[Optional[int], Meta(ge=0, title='recv_time_ns')]] = None
    ats: Optional[Annotated[Optional[int], Meta(title='recv_time')]] = None
    d: Optional[Annotated[Optional[Dir], Meta(title='direction')]] = None
    f: Optional[Annotated[Optional[Decimal], Meta(title='fee')]] = None
    fu: Optional[Annotated[Optional[str], Meta(title='fee_currency')]] = None
    k: Optional[Annotated[Optional[FillKind], Meta(title='fill_kind')]] = None
    oid: Optional[Annotated[Optional[OrderId], Meta(title='order_id')]] = None
    p: Optional[Annotated[Optional[Decimal], Meta(title='price')]] = None
    q: Optional[Annotated[Optional[Decimal], Meta(title='quantity')]] = None
    s: Optional[Annotated[Optional[str], Meta(title='symbol')]] = None
    tn: Optional[Annotated[Optional[int], Meta(ge=0, title='trade_time_ns')]] = None
    ts: Optional[Annotated[Optional[int], Meta(title='trade_time')]] = None
    u: Optional[Annotated[Optional[UserId], Meta(title='trader')]] = None
    xid: Optional[Annotated[Optional[str], Meta(title='exchange_fill_id')]] = None


Dropcopy = Annotated[
    Union[Union[Dropcopy1, Dropcopy2, Dropcopy3], Dropcopy4, Dropcopy5],
    Meta(title='Dropcopy'),
]
