# generated by datamodel-codegen:
#   filename:  Oms/Order.json

from __future__ import annotations
from architect_py.scalars import OrderDir

from decimal import Decimal
from typing import Annotated, Literal, Optional, Union

from msgspec import Meta, Struct

from .. import definitions


class Order1(Struct, tag_field="k", tag="LIMIT"):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
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


class Order2(Struct, tag_field="k", tag="STOP_LOSS_LIMIT"):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
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


class Order3(Struct, tag_field="k", tag="TAKE_PROFIT_LIMIT"):
    a: Annotated[str, Meta(title="account")]
    d: Annotated[OrderDir, Meta(title="dir")]
    id: definitions.OrderId
    o: Annotated[definitions.OrderStatus, Meta(title="status")]
    q: Annotated[Decimal, Meta(title="quantity")]
    s: Annotated[str, Meta(title="symbol")]
    src: Annotated[definitions.OrderSource, Meta(title="source")]
    tif: Annotated[definitions.TimeInForce, Meta(title="time_in_force")]
    tn: Annotated[int, Meta(ge=0, title="recv_time_ns")]
    ts: Annotated[int, Meta(title="recv_time")]
    u: Annotated[definitions.UserId, Meta(title="trader")]
    ve: Annotated[str, Meta(title="execution_venue")]
    xq: Annotated[Decimal, Meta(title="filled_quantity")]
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


Order = Annotated[Union[Order1, Order2, Order3], Meta(title="Order")]
