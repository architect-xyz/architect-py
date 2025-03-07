# generated by datamodel-codegen:
#   filename:  Orderflow/Dropcopy.json

from __future__ import annotations

from decimal import Decimal
from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct

from .. import definitions


class Dropcopy1(Struct):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    t: Literal["o"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
    k: Literal["LIMIT"]
    p: Annotated[Decimal, Meta(title="limit_price")]
    po: Annotated[bool, Meta(title="post_only")]
    eid: Optional[Annotated[Optional[str], Meta(title="exchange_order_id")]] = None
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    r: Optional[
        Annotated[Optional[definitions.OrderRejectReason], Meta(title="reject_reason")]
    ] = None
    rm: Optional[Annotated[Optional[str], Meta(title="reject_message")]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title="average_fill_price")]] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> OrderDir:
        return self.d

    @dir.setter
    def dir(self, value: OrderDir) -> None:
        self.d = value

    @property
    def status(self) -> definitions.OrderStatus:
        return self.o

    @status.setter
    def status(self, value: definitions.OrderStatus) -> None:
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
    def source(self) -> definitions.OrderSource:
        return self.src

    @source.setter
    def source(self, value: definitions.OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
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
    def trader(self) -> definitions.UserId:
        return self.u

    @trader.setter
    def trader(self, value: definitions.UserId) -> None:
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
    def exchange_order_id(self) -> Optional[str]:
        return self.eid

    @exchange_order_id.setter
    def exchange_order_id(self, value: Optional[str]) -> None:
        self.eid = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[definitions.OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[definitions.OrderRejectReason]) -> None:
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


class Dropcopy2(Struct):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    t: Literal["o"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
    k: Literal["STOP_LOSS_LIMIT"]
    p: Annotated[Decimal, Meta(title="limit_price")]
    tp: Annotated[Decimal, Meta(title="trigger_price")]
    eid: Optional[Annotated[Optional[str], Meta(title="exchange_order_id")]] = None
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    r: Optional[
        Annotated[Optional[definitions.OrderRejectReason], Meta(title="reject_reason")]
    ] = None
    rm: Optional[Annotated[Optional[str], Meta(title="reject_message")]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title="average_fill_price")]] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> OrderDir:
        return self.d

    @dir.setter
    def dir(self, value: OrderDir) -> None:
        self.d = value

    @property
    def status(self) -> definitions.OrderStatus:
        return self.o

    @status.setter
    def status(self, value: definitions.OrderStatus) -> None:
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
    def source(self) -> definitions.OrderSource:
        return self.src

    @source.setter
    def source(self, value: definitions.OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
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
    def trader(self) -> definitions.UserId:
        return self.u

    @trader.setter
    def trader(self, value: definitions.UserId) -> None:
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
    def exchange_order_id(self) -> Optional[str]:
        return self.eid

    @exchange_order_id.setter
    def exchange_order_id(self, value: Optional[str]) -> None:
        self.eid = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[definitions.OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[definitions.OrderRejectReason]) -> None:
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


class Dropcopy3(Struct):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    t: Literal["o"]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
    k: Literal["TAKE_PROFIT_LIMIT"]
    p: Annotated[Decimal, Meta(title="limit_price")]
    tp: Annotated[Decimal, Meta(title="trigger_price")]
    eid: Optional[Annotated[Optional[str], Meta(title="exchange_order_id")]] = None
    pid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="parent_id")]] = (
        None
    )
    r: Optional[
        Annotated[Optional[definitions.OrderRejectReason], Meta(title="reject_reason")]
    ] = None
    rm: Optional[Annotated[Optional[str], Meta(title="reject_message")]] = None
    xp: Optional[Annotated[Optional[Decimal], Meta(title="average_fill_price")]] = None

    @property
    def account(self) -> str:
        return self.a

    @account.setter
    def account(self, value: str) -> None:
        self.a = value

    @property
    def dir(self) -> OrderDir:
        return self.d

    @dir.setter
    def dir(self, value: OrderDir) -> None:
        self.d = value

    @property
    def status(self) -> definitions.OrderStatus:
        return self.o

    @status.setter
    def status(self, value: definitions.OrderStatus) -> None:
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
    def source(self) -> definitions.OrderSource:
        return self.src

    @source.setter
    def source(self, value: definitions.OrderSource) -> None:
        self.src = value

    @property
    def time_in_force(self) -> definitions.TimeInForce:
        return self.tif

    @time_in_force.setter
    def time_in_force(self, value: definitions.TimeInForce) -> None:
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
    def trader(self) -> definitions.UserId:
        return self.u

    @trader.setter
    def trader(self, value: definitions.UserId) -> None:
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
    def exchange_order_id(self) -> Optional[str]:
        return self.eid

    @exchange_order_id.setter
    def exchange_order_id(self, value: Optional[str]) -> None:
        self.eid = value

    @property
    def parent_id(self) -> Optional[definitions.OrderId]:
        return self.pid

    @parent_id.setter
    def parent_id(self, value: Optional[definitions.OrderId]) -> None:
        self.pid = value

    @property
    def reject_reason(self) -> Optional[definitions.OrderRejectReason]:
        return self.r

    @reject_reason.setter
    def reject_reason(self, value: Optional[definitions.OrderRejectReason]) -> None:
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


class Dropcopy4(Struct):
    d: Annotated[OrderDir, Meta(title="direction")]
    id: Annotated[str, Meta(title="fill_id")]
    k: Annotated[definitions.FillKind, Meta(title="fill_kind")]
    p: Annotated[Decimal, Meta(title="price")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    t: Annotated[int, Meta(title="is_taker")]
    tn: Annotated[int, Meta(ge=0, title="trade_time_ns")]
    ts: Annotated[
        int,
        Meta(description="When the cpty claims the trade happened", title="trade_time"),
    ]
    """
    When the cpty claims the trade happened
    """
    x: Annotated[str, Meta(title="execution_venue")]
    a: Optional[Annotated[Optional[str], Meta(title="account")]] = None
    atn: Optional[Annotated[Optional[int], Meta(ge=0, title="recv_time_ns")]] = None
    ats: Optional[
        Annotated[
            Optional[int],
            Meta(
                description="When Architect received the fill, if realtime",
                title="recv_time",
            ),
        ]
    ] = None
    """
    When Architect received the fill, if realtime
    """
    f: Optional[Annotated[Optional[Decimal], Meta(title="fee")]] = None
    fu: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="Fee currency, if different from the price currency",
                title="fee_currency",
            ),
        ]
    ] = None
    """
    Fee currency, if different from the price currency
    """
    oid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="order_id")]] = (
        None
    )
    u: Optional[Annotated[Optional[definitions.UserId], Meta(title="trader")]] = None
    xid: Optional[Annotated[Optional[str], Meta(title="exchange_fill_id")]] = None

    @property
    def direction(self) -> OrderDir:
        return self.d

    @direction.setter
    def direction(self, value: OrderDir) -> None:
        self.d = value

    @property
    def fill_id(self) -> str:
        return self.id

    @fill_id.setter
    def fill_id(self, value: str) -> None:
        self.id = value

    @property
    def fill_kind(self) -> definitions.FillKind:
        return self.k

    @fill_kind.setter
    def fill_kind(self, value: definitions.FillKind) -> None:
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
    def order_id(self) -> Optional[definitions.OrderId]:
        return self.oid

    @order_id.setter
    def order_id(self, value: Optional[definitions.OrderId]) -> None:
        self.oid = value

    @property
    def trader(self) -> Optional[definitions.UserId]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[definitions.UserId]) -> None:
        self.u = value

    @property
    def exchange_fill_id(self) -> Optional[str]:
        return self.xid

    @exchange_fill_id.setter
    def exchange_fill_id(self, value: Optional[str]) -> None:
        self.xid = value


class Dropcopy5(Struct, tag_field="t", tag="af"):
    """
    Fills which we received but couldn't parse fully, return details best effort
    """

    id: Annotated[str, Meta(title="fill_id")]
    x: Annotated[str, Meta(title="execution_venue")]
    a: Optional[Annotated[Optional[str], Meta(title="account")]] = None
    atn: Optional[Annotated[Optional[int], Meta(ge=0, title="recv_time_ns")]] = None
    ats: Optional[Annotated[Optional[int], Meta(title="recv_time")]] = None
    d: Optional[Annotated[Optional[OrderDir], Meta(title="direction")]] = None
    f: Optional[Annotated[Optional[Decimal], Meta(title="fee")]] = None
    fu: Optional[Annotated[Optional[str], Meta(title="fee_currency")]] = None
    k: Optional[Annotated[Optional[definitions.FillKind], Meta(title="fill_kind")]] = (
        None
    )
    oid: Optional[Annotated[Optional[definitions.OrderId], Meta(title="order_id")]] = (
        None
    )
    p: Optional[Annotated[Optional[Decimal], Meta(title="price")]] = None
    q: Optional[Annotated[Optional[Decimal], Meta(title="quantity")]] = None
    s: Optional[Annotated[Optional[str], Meta(title="symbol")]] = None
    tn: Optional[Annotated[Optional[int], Meta(ge=0, title="trade_time_ns")]] = None
    ts: Optional[Annotated[Optional[int], Meta(title="trade_time")]] = None
    u: Optional[Annotated[Optional[definitions.UserId], Meta(title="trader")]] = None
    xid: Optional[Annotated[Optional[str], Meta(title="exchange_fill_id")]] = None

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
    def direction(self) -> Optional[OrderDir]:
        return self.d

    @direction.setter
    def direction(self, value: Optional[OrderDir]) -> None:
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
    def fill_kind(self) -> Optional[definitions.FillKind]:
        return self.k

    @fill_kind.setter
    def fill_kind(self, value: Optional[definitions.FillKind]) -> None:
        self.k = value

    @property
    def order_id(self) -> Optional[definitions.OrderId]:
        return self.oid

    @order_id.setter
    def order_id(self, value: Optional[definitions.OrderId]) -> None:
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
    def trader(self) -> Optional[definitions.UserId]:
        return self.u

    @trader.setter
    def trader(self, value: Optional[definitions.UserId]) -> None:
        self.u = value

    @property
    def exchange_fill_id(self) -> Optional[str]:
        return self.xid

    @exchange_fill_id.setter
    def exchange_fill_id(self, value: Optional[str]) -> None:
        self.xid = value


Dropcopy = Annotated[
    Union[Union[Dropcopy1, Dropcopy2, Dropcopy3], Dropcopy4, Dropcopy5],
    Meta(title="Dropcopy"),
]
