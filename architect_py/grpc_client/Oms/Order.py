# generated by datamodel-codegen:
#   filename:  Order.json

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct


class Quantity(Struct):
    pass


class FilledQuantity(Struct):
    pass


class LimitPrice(Struct):
    pass


class TriggerPrice(Struct):
    pass


Decimal1 = Decimal


class Dir(str, Enum):
    """
    An order side/direction or a trade execution side/direction. In GraphQL these are serialized as "buy" or "sell".
    """

    BUY = 'BUY'
    SELL = 'SELL'


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


class TimeInForce3(str, Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'


class TimeInForce4(Struct):
    GTD: str


TimeInForce = Union[TimeInForce3, TimeInForce4, Literal['DAY']]


UserId = str


class Order4(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Quantity, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[FilledQuantity, Meta(title='filled_quantity')]
    k: Literal['LIMIT']
    p: Annotated[LimitPrice, Meta(title='limit_price')]
    po: Annotated[bool, Meta(title='post_only')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None

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
    def quantity(self) -> Quantity:
        return self.q

    @quantity.setter
    def quantity(self, value: Quantity) -> None:
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
    def filled_quantity(self) -> FilledQuantity:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: FilledQuantity) -> None:
        self.xq = value

    @property
    def limit_price(self) -> LimitPrice:
        return self.p

    @limit_price.setter
    def limit_price(self, value: LimitPrice) -> None:
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


class Order5(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Quantity, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[FilledQuantity, Meta(title='filled_quantity')]
    k: Literal['STOP_LOSS_LIMIT']
    p: Annotated[LimitPrice, Meta(title='limit_price')]
    tp: Annotated[TriggerPrice, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None

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
    def quantity(self) -> Quantity:
        return self.q

    @quantity.setter
    def quantity(self, value: Quantity) -> None:
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
    def filled_quantity(self) -> FilledQuantity:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: FilledQuantity) -> None:
        self.xq = value

    @property
    def limit_price(self) -> LimitPrice:
        return self.p

    @limit_price.setter
    def limit_price(self, value: LimitPrice) -> None:
        self.p = value

    @property
    def trigger_price(self) -> TriggerPrice:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: TriggerPrice) -> None:
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


class Order6(Struct):
    a: Annotated[str, Meta(title='account')]
    d: Annotated[Dir, Meta(title='dir')]
    id: OrderId
    o: Annotated[OrderStatus, Meta(title='status')]
    q: Annotated[Quantity, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
    src: Annotated[OrderSource, Meta(title='source')]
    tif: Annotated[TimeInForce, Meta(title='time_in_force')]
    tn: Annotated[int, Meta(ge=0, title='recv_time_ns')]
    ts: Annotated[int, Meta(title='recv_time')]
    u: Annotated[UserId, Meta(title='trader')]
    ve: Annotated[str, Meta(title='execution_venue')]
    xq: Annotated[FilledQuantity, Meta(title='filled_quantity')]
    k: Literal['TAKE_PROFIT_LIMIT']
    p: Annotated[LimitPrice, Meta(title='limit_price')]
    tp: Annotated[TriggerPrice, Meta(title='trigger_price')]
    pid: Optional[Annotated[Optional[OrderId], Meta(title='parent_id')]] = None
    r: Optional[Annotated[Optional[OrderRejectReason], Meta(title='reject_reason')]] = (
        None
    )
    rm: Optional[Annotated[Optional[str], Meta(title='reject_message')]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title='average_fill_price')]] = None

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
    def quantity(self) -> Quantity:
        return self.q

    @quantity.setter
    def quantity(self, value: Quantity) -> None:
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
    def filled_quantity(self) -> FilledQuantity:
        return self.xq

    @filled_quantity.setter
    def filled_quantity(self, value: FilledQuantity) -> None:
        self.xq = value

    @property
    def limit_price(self) -> LimitPrice:
        return self.p

    @limit_price.setter
    def limit_price(self, value: LimitPrice) -> None:
        self.p = value

    @property
    def trigger_price(self) -> TriggerPrice:
        return self.tp

    @trigger_price.setter
    def trigger_price(self, value: TriggerPrice) -> None:
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


Order = Annotated[Union[Order4, Order5, Order6], Meta(title='Order')]
