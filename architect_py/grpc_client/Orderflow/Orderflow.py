# generated by datamodel-codegen:
#   filename:  Orderflow.json

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct


class CancelStatus(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_127 = 127




class Dir(str, Enum):
    """
    An order side/direction or a trade execution side/direction. In GraphQL these are serialized as "buy" or "sell".
    """

    BUY = 'BUY'
    SELL = 'SELL'


class FillKind(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2


class OrderId(Struct):
    """
    System-unique, persistent order identifiers
    """

    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class OrderRejectReason(str, Enum):
    DuplicateOrderId = 'DuplicateOrderId'
    NotAuthorized = 'NotAuthorized'
    NoExecutionVenue = 'NoExecutionVenue'
    NoAccount = 'NoAccount'
    NoCpty = 'NoCpty'
    UnsupportedOrderType = 'UnsupportedOrderType'
    UnsupportedExecutionVenue = 'UnsupportedExecutionVenue'
    Unknown = 'Unknown'


class OrderSource(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_3 = 3
    integer_4 = 4
    integer_5 = 5
    integer_255 = 255


class OrderStatus(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2
    integer_127 = 127
    integer_128 = 128
    integer_129 = 129
    integer_254 = 254


class TimeInForce1(str, Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'


class TimeInForce2(Struct):
    GTD: str


TimeInForce = Union[TimeInForce1, TimeInForce2, Literal['DAY']]


UserId = str


class Orderflow1(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: Literal['w']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: Literal['LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    po: Annotated[bool, Meta(title='post_only')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[
        Annotated[Optional[Decimal], Meta(title='average_fill_price')]
    ] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def status(self) -> OrderStatus:
        return self.o

    @status.setter
    def status(self, value: OrderStatus) -> None:
        self.o = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def source(self) -> OrderSource:
        return self.src

    @source.setter
    def source(self, value: OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def recv_time_ns(self) -> int:
        return self.tn

    @recv_time_ns.setter
    def recv_time_ns(self, value: int) -> None:
        self.tn = value

    @property
    def recv_time(self) -> int:
        return self.ts

    @recv_time.setter
    def recv_time(self, value: int) -> None:
        self.ts = value

    @property
    def trader(self) -> UserId:
        return self.u

    @trader.setter
    def trader(self, value: UserId) -> None:
        self.u = value

    @property
    def execution_venue(self) -> str:
        return self.ve

    @execution_venue.setter
    def execution_venue(self, value: str) -> None:
        self.ve = value

    @property
    def filled_quantity(self) -> Decimal:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: Decimal) -> None:
        self.xq = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def post_only(self) -> bool:
        return self.po

    @post_only.setter
    def post_only(self, value: bool) -> None:
        self.po = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[OrderRejectReason]) -> None:
        self.r = value

    @property
    def reject_message(self) -> Optional[str]:
        return self.rm

    @reject_message.setter
    def reject_message(self, value: Optional[str]) -> None:
        self.rm = value

    @property
    def average_fill_price(self) -> Optional[Decimal]:
        return self.xp

    @average_fill_price.setter
    def average_fill_price(self, value: Optional[Decimal]) -> None:
        self.xp = value


class Orderflow2(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: Literal['w']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: Literal['STOP_LOSS_LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[
        Annotated[Optional[Decimal], Meta(title='average_fill_price')]
    ] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def status(self) -> OrderStatus:
        return self.o

    @status.setter
    def status(self, value: OrderStatus) -> None:
        self.o = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def source(self) -> OrderSource:
        return self.src

    @source.setter
    def source(self, value: OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def recv_time_ns(self) -> int:
        return self.tn

    @recv_time_ns.setter
    def recv_time_ns(self, value: int) -> None:
        self.tn = value

    @property
    def recv_time(self) -> int:
        return self.ts

    @recv_time.setter
    def recv_time(self, value: int) -> None:
        self.ts = value

    @property
    def trader(self) -> UserId:
        return self.u

    @trader.setter
    def trader(self, value: UserId) -> None:
        self.u = value

    @property
    def execution_venue(self) -> str:
        return self.ve

    @execution_venue.setter
    def execution_venue(self, value: str) -> None:
        self.ve = value

    @property
    def filled_quantity(self) -> Decimal:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: Decimal) -> None:
        self.xq = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def trigger_price(self) -> Decimal:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: Decimal) -> None:
        self.tp = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[OrderRejectReason]) -> None:
        self.r = value

    @property
    def reject_message(self) -> Optional[str]:
        return self.rm

    @reject_message.setter
    def reject_message(self, value: Optional[str]) -> None:
        self.rm = value

    @property
    def average_fill_price(self) -> Optional[Decimal]:
        return self.xp

    @average_fill_price.setter
    def average_fill_price(self, value: Optional[Decimal]) -> None:
        self.xp = value


class Orderflow3(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    t: Literal['w']
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[Decimal, Meta(title='filled_quantity')]
    k: Literal['TAKE_PROFIT_LIMIT']
    p: Annotated[Decimal, Meta(title='limit_price')]
    tp: Annotated[Decimal, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[
        Annotated[Optional[Decimal], Meta(title='average_fill_price')]
    ] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> Dir:
        return self.d

    @dir.setter
    def dir(self, value: Dir) -> None:
        self.d = value

    @property
    def status(self) -> OrderStatus:
        return self.o

    @status.setter
    def status(self, value: OrderStatus) -> None:
        self.o = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def source(self) -> OrderSource:
        return self.src

    @source.setter
    def source(self, value: OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: TimeInForce) -> None:
        self.tif = value

    @property
    def recv_time_ns(self) -> int:
        return self.tn

    @recv_time_ns.setter
    def recv_time_ns(self, value: int) -> None:
        self.tn = value

    @property
    def recv_time(self) -> int:
        return self.ts

    @recv_time.setter
    def recv_time(self, value: int) -> None:
        self.ts = value

    @property
    def trader(self) -> UserId:
        return self.u

    @trader.setter
    def trader(self, value: UserId) -> None:
        self.u = value

    @property
    def execution_venue(self) -> str:
        return self.ve

    @execution_venue.setter
    def execution_venue(self, value: str) -> None:
        self.ve = value

    @property
    def filled_quantity(self) -> Decimal:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: Decimal) -> None:
        self.xq = value

    @property
    def limit_price(self) -> Decimal:
        return self.p

    @limit_price.setter
    def limit_price(self, value: Decimal) -> None:
        self.p = value

    @property
    def trigger_price(self) -> Decimal:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: Decimal) -> None:
        self.tp = value

    @property
    def parent_id(self) -> Optional[OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[OrderRejectReason]) -> None:
        self.r = value

    @property
    def reject_message(self) -> Optional[str]:
        return self.rm

    @reject_message.setter
    def reject_message(self, value: Optional[str]) -> None:
        self.rm = value

    @property
    def average_fill_price(self) -> Optional[Decimal]:
        return self.xp

    @average_fill_price.setter
    def average_fill_price(self, value: Optional[Decimal]) -> None:
        self.xp = value


class Orderflow4(Struct):
    id: OrderId
    t: Literal['a']


class Orderflow5(Struct):
    id: OrderId
    r: OrderRejectReason
    t: Literal['r']
    rm: Optional[str] = None


class Orderflow6(Struct):
    id: OrderId
    t: Literal['o']


class Orderflow7(Struct):
    id: OrderId
    t: Literal['z']


class Orderflow8(Struct):
    id: OrderId
    o: CancelStatus
    t: Literal['xc']
    tn: Annotated[int, Meta(ge=0)]
    ts: int
    xid: str
    r: Optional[str] = None


class Orderflow9(Struct):
    id: OrderId
    t: Literal['xr']
    xid: str
    rm: Optional[str] = None


class Orderflow10(Struct):
    id: OrderId
    t: Literal['xa']
    xid: Optional[str] = None


class Orderflow11(Struct):
    id: OrderId
    t: Literal['xx']
    xid: Optional[str] = None


class Orderflow12(Struct):
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

    @property
    def direction(self) -> Dir:
        return self.d

    @direction.setter
    def direction(self, value: Dir) -> None:
        self.d = value

    @property
    def fill_id(self) -> str:
        return self.id

    @fill_id.setter
    def fill_id(self, value: str) -> None:
        self.id = value

    @property
    def fill_kind(self) -> FillKind:
        return self.k

    @fill_kind.setter
    def fill_kind(self, value: FillKind) -> None:
        self.k = value

    @property
    def price(self) -> Decimal:
        return self.p

    @price.setter
    def price(self, value: Decimal) -> None:
        self.p = value

    @property
    def quantity(self) -> Decimal:
        return self.q

    @quantity.setter
    def quantity(self, value: Decimal) -> None:
        self.q = value

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def is_taker(self) -> int:
        return self.t

    @is_taker.setter
    def is_taker(self, value: int) -> None:
        self.t = value

    @property
    def trade_time_ns(self) -> int:
        return self.tn

    @trade_time_ns.setter
    def trade_time_ns(self, value: int) -> None:
        self.tn = value

    @property
    def trade_time(self) -> int:
        return self.ts

    @trade_time.setter
    def trade_time(self, value: int) -> None:
        self.ts = value

    @property
    def execution_venue(self) -> str:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: str) -> None:
        self.x = value

    @property
    def account(self) -> Optional[str]:
        return self.a

    @account.setter
    def account(self, value: Optional[str]) -> None:
        self.a = value

    @property
    def recv_time_ns(self) -> Optional[int]:
        return self.atn

    @recv_time_ns.setter
    def recv_time_ns(self, value: Optional[int]) -> None:
        self.atn = value

    @property
    def recv_time(self) -> Optional[int]:
        return self.ats

    @recv_time.setter
    def recv_time(self, value: Optional[int]) -> None:
        self.ats = value

    @property
    def fee(self) -> Optional[Decimal]:
        return self.f

    @fee.setter
    def fee(self, value: Optional[Decimal]) -> None:
        self.f = value

    @property
    def fee_currency(self) -> Optional[str]:
        return self.fu

    @fee_currency.setter
    def fee_currency(self, value: Optional[str]) -> None:
        self.fu = value

    @property
    def order_id(self) -> Optional[OrderId]:
        return self.oid

    @order_id.setter
    def order_id(self, value: Optional[OrderId]) -> None:
        self.oid = value

    @property
    def trader(self) -> Optional[UserId]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[UserId]) -> None:
        self.u = value

    @property
    def exchange_fill_id(self) -> Optional[str]:
        return self.xid

    @exchange_fill_id.setter
    def exchange_fill_id(self, value: Optional[str]) -> None:
        self.xid = value


class Orderflow13(Struct):
    """
    Fills which we received but couldn't parse fully, return details best effort
    """

    id: Annotated[str, Meta(title='fill_id')]
    t: Literal['af']
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

    @property
    def fill_id(self) -> str:
        return self.id

    @fill_id.setter
    def fill_id(self, value: str) -> None:
        self.id = value

    @property
    def execution_venue(self) -> str:
        return self.x

    @execution_venue.setter
    def execution_venue(self, value: str) -> None:
        self.x = value

    @property
    def account(self) -> Optional[str]:
        return self.a

    @account.setter
    def account(self, value: Optional[str]) -> None:
        self.a = value

    @property
    def recv_time_ns(self) -> Optional[int]:
        return self.atn

    @recv_time_ns.setter
    def recv_time_ns(self, value: Optional[int]) -> None:
        self.atn = value

    @property
    def recv_time(self) -> Optional[int]:
        return self.ats

    @recv_time.setter
    def recv_time(self, value: Optional[int]) -> None:
        self.ats = value

    @property
    def direction(self) -> Optional[Dir]:
        return self.d

    @direction.setter
    def direction(self, value: Optional[Dir]) -> None:
        self.d = value

    @property
    def fee(self) -> Optional[Decimal]:
        return self.f

    @fee.setter
    def fee(self, value: Optional[Decimal]) -> None:
        self.f = value

    @property
    def fee_currency(self) -> Optional[str]:
        return self.fu

    @fee_currency.setter
    def fee_currency(self, value: Optional[str]) -> None:
        self.fu = value

    @property
    def fill_kind(self) -> Optional[FillKind]:
        return self.k

    @fill_kind.setter
    def fill_kind(self, value: Optional[FillKind]) -> None:
        self.k = value

    @property
    def order_id(self) -> Optional[OrderId]:
        return self.oid

    @order_id.setter
    def order_id(self, value: Optional[OrderId]) -> None:
        self.oid = value

    @property
    def price(self) -> Optional[Decimal]:
        return self.p

    @price.setter
    def price(self, value: Optional[Decimal]) -> None:
        self.p = value

    @property
    def quantity(self) -> Optional[Decimal]:
        return self.q

    @quantity.setter
    def quantity(self, value: Optional[Decimal]) -> None:
        self.q = value

    @property
    def symbol(self) -> Optional[str]:
        return self.s

    @symbol.setter
    def symbol(self, value: Optional[str]) -> None:
        self.s = value

    @property
    def trade_time_ns(self) -> Optional[int]:
        return self.tn

    @trade_time_ns.setter
    def trade_time_ns(self, value: Optional[int]) -> None:
        self.tn = value

    @property
    def trade_time(self) -> Optional[int]:
        return self.ts

    @trade_time.setter
    def trade_time(self, value: Optional[int]) -> None:
        self.ts = value

    @property
    def trader(self) -> Optional[UserId]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[UserId]) -> None:
        self.u = value

    @property
    def exchange_fill_id(self) -> Optional[str]:
        return self.xid

    @exchange_fill_id.setter
    def exchange_fill_id(self, value: Optional[str]) -> None:
        self.xid = value


Orderflow = Annotated[
    Union[
        Union[Orderflow1, Orderflow2, Orderflow3],
        Orderflow4,
        Orderflow5,
        Orderflow6,
        Orderflow7,
        Orderflow8,
        Orderflow9,
        Orderflow10,
        Orderflow11,
        Orderflow12,
        Orderflow13,
    ],
    Meta(title='Orderflow'),
]
