from decimal import Decimal

# generated by datamodel-codegen:
#   filename:  Marketdata_TickersResponse.json

from __future__ import annotations

from typing import Annotated, List, Optional

from msgspec import Meta, Struct, field



class Ticker(Struct):
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    ve: Annotated[str, Meta(title='venue')]
    ap: Optional[Annotated[Optional[Decimal], Meta(title='ask_price')]] = None
    as_: Optional[Annotated[Optional[Decimal], Meta(title='ask_size')]] = field(
        name='as', default=None
    )
    bp: Optional[Annotated[Optional[Decimal], Meta(title='bid_price')]] = None
    bs: Optional[Annotated[Optional[Decimal], Meta(title='bid_size')]] = None
    dividend: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None
    eps_adj: Optional[Decimal] = None
    fr: Optional[Annotated[Optional[Decimal], Meta(title='funding_rate')]] = None
    ft: Optional[Annotated[Optional[str], Meta(title='next_funding_time')]] = None
    h: Optional[Annotated[Optional[Decimal], Meta(title='high_24h')]] = None
    ip: Optional[Annotated[Optional[Decimal], Meta(title='index_price')]] = None
    l: Optional[Annotated[Optional[Decimal], Meta(title='low_24h')]] = None
    market_cap: Optional[Decimal] = None
    mp: Optional[Annotated[Optional[Decimal], Meta(title='mark_price')]] = None
    o: Optional[Annotated[Optional[Decimal], Meta(title='open_24h')]] = None
    oi: Optional[Annotated[Optional[Decimal], Meta(title='open_interest')]] = None
    p: Optional[Annotated[Optional[Decimal], Meta(title='last_price')]] = None
    price_to_earnings: Optional[Decimal] = None
    q: Optional[Annotated[Optional[Decimal], Meta(title='last_size')]] = None
    shares_outstanding_weighted_adj: Optional[Decimal] = None
    sp: Optional[Annotated[Optional[Decimal], Meta(title='last_settlement_price')]] = (
        None
    )
    v: Optional[Annotated[Optional[Decimal], Meta(title='volume_24h')]] = None
    vm: Optional[Annotated[Optional[Decimal], Meta(title='volume_30d')]] = None
    xh: Optional[Annotated[Optional[Decimal], Meta(title='session_high')]] = None
    xl: Optional[Annotated[Optional[Decimal], Meta(title='session_low')]] = None
    xo: Optional[Annotated[Optional[Decimal], Meta(title='session_open')]] = None
    xv: Optional[Annotated[Optional[Decimal], Meta(title='session_volume')]] = None

    @property
    def symbol(self) -> str:
        return self.s

    @symbol.setter
    def symbol(self, value: str) -> None:
        self.s = value

    @property
    def timestamp_ns(self) -> int:
        return self.tn

    @timestamp_ns.setter
    def timestamp_ns(self, value: int) -> None:
        self.tn = value

    @property
    def timestamp(self) -> int:
        return self.ts

    @timestamp.setter
    def timestamp(self, value: int) -> None:
        self.ts = value

    @property
    def venue(self) -> str:
        return self.ve

    @venue.setter
    def venue(self, value: str) -> None:
        self.ve = value

    @property
    def ask_price(self) -> Optional[Decimal]:
        return self.ap

    @ask_price.setter
    def ask_price(self, value: Optional[Decimal]) -> None:
        self.ap = value

    @property
    def ask_size(self) -> Optional[Decimal]:
        return self.as_

    @ask_size.setter
    def ask_size(self, value: Optional[Decimal]) -> None:
        self.as_ = value

    @property
    def bid_price(self) -> Optional[Decimal]:
        return self.bp

    @bid_price.setter
    def bid_price(self, value: Optional[Decimal]) -> None:
        self.bp = value

    @property
    def bid_size(self) -> Optional[Decimal]:
        return self.bs

    @bid_size.setter
    def bid_size(self, value: Optional[Decimal]) -> None:
        self.bs = value

    @property
    def funding_rate(self) -> Optional[Decimal]:
        return self.fr

    @funding_rate.setter
    def funding_rate(self, value: Optional[Decimal]) -> None:
        self.fr = value

    @property
    def next_funding_time(self) -> Optional[str]:
        return self.ft

    @next_funding_time.setter
    def next_funding_time(self, value: Optional[str]) -> None:
        self.ft = value

    @property
    def high_24h(self) -> Optional[Decimal]:
        return self.h

    @high_24h.setter
    def high_24h(self, value: Optional[Decimal]) -> None:
        self.h = value

    @property
    def index_price(self) -> Optional[Decimal]:
        return self.ip

    @index_price.setter
    def index_price(self, value: Optional[Decimal]) -> None:
        self.ip = value

    @property
    def low_24h(self) -> Optional[Decimal]:
        return self.l

    @low_24h.setter
    def low_24h(self, value: Optional[Decimal]) -> None:
        self.l = value

    @property
    def mark_price(self) -> Optional[Decimal]:
        return self.mp

    @mark_price.setter
    def mark_price(self, value: Optional[Decimal]) -> None:
        self.mp = value

    @property
    def open_24h(self) -> Optional[Decimal]:
        return self.o

    @open_24h.setter
    def open_24h(self, value: Optional[Decimal]) -> None:
        self.o = value

    @property
    def open_interest(self) -> Optional[Decimal]:
        return self.oi

    @open_interest.setter
    def open_interest(self, value: Optional[Decimal]) -> None:
        self.oi = value

    @property
    def last_price(self) -> Optional[Decimal]:
        return self.p

    @last_price.setter
    def last_price(self, value: Optional[Decimal]) -> None:
        self.p = value

    @property
    def last_size(self) -> Optional[Decimal]:
        return self.q

    @last_size.setter
    def last_size(self, value: Optional[Decimal]) -> None:
        self.q = value

    @property
    def last_settlement_price(self) -> Optional[Decimal]:
        return self.sp

    @last_settlement_price.setter
    def last_settlement_price(self, value: Optional[Decimal]) -> None:
        self.sp = value

    @property
    def volume_24h(self) -> Optional[Decimal]:
        return self.v

    @volume_24h.setter
    def volume_24h(self, value: Optional[Decimal]) -> None:
        self.v = value

    @property
    def volume_30d(self) -> Optional[Decimal]:
        return self.vm

    @volume_30d.setter
    def volume_30d(self, value: Optional[Decimal]) -> None:
        self.vm = value

    @property
    def session_high(self) -> Optional[Decimal]:
        return self.xh

    @session_high.setter
    def session_high(self, value: Optional[Decimal]) -> None:
        self.xh = value

    @property
    def session_low(self) -> Optional[Decimal]:
        return self.xl

    @session_low.setter
    def session_low(self, value: Optional[Decimal]) -> None:
        self.xl = value

    @property
    def session_open(self) -> Optional[Decimal]:
        return self.xo

    @session_open.setter
    def session_open(self, value: Optional[Decimal]) -> None:
        self.xo = value

    @property
    def session_volume(self) -> Optional[Decimal]:
        return self.xv

    @session_volume.setter
    def session_volume(self, value: Optional[Decimal]) -> None:
        self.xv = value


class TickersResponse(Struct):
    tickers: List[Ticker]
