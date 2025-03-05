# generated by datamodel-codegen:
#   filename:  HistoricalFillsResponse.json

from __future__ import annotations
from decimal import Decimal


from enum import Enum
from typing import Annotated, List, Optional

from msgspec import Meta, Struct



class Dir(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class FillKind(int, Enum):
    integer_0 = 0
    integer_1 = 1
    integer_2 = 2


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


UserId = str


class AberrantFill(Struct):
    id: Annotated[str, Meta(title='fill_id')]
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


class Fill(Struct):
    d: Annotated[Dir, Meta(title='direction')]
    id: Annotated[str, Meta(title='fill_id')]
    k: Annotated[FillKind, Meta(title='fill_kind')]
    p: Annotated[Decimal, Meta(title='price')]
    q: Annotated[Decimal, Meta(title='quantity')]
    s: Annotated[str, Meta(title='symbol')]
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
    t: Optional[Annotated[int, Meta(title='is_taker')]] = None
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
    def is_taker(self) -> Optional[int]:
        return self.t

    @is_taker.setter
    def is_taker(self, value: Optional[int]) -> None:
        self.t = value

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


class HistoricalFillsResponse(Struct):
    aberrant_fills: List[AberrantFill]
    fills: List[Fill]
