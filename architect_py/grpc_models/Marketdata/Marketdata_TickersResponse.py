# generated by datamodel-codegen:
#   filename:  Marketdata_TickersResponse.json
#   timestamp: 2025-02-25T21:20:49+00:00

from __future__ import annotations

from typing import Annotated, List

from msgspec import Meta, Struct, field


class Ticker(Struct):
    s: Annotated[str, Meta(title='symbol')]
    tn: Annotated[int, Meta(ge=0, title='timestamp_ns')]
    ts: Annotated[int, Meta(title='timestamp')]
    ve: Annotated[str, Meta(title='venue')]
    ap: Annotated[str | None, Meta(title='ask_price')] | None = None
    as_: Annotated[str | None, Meta(title='ask_size')] | None = field(
        name='as', default=None
    )
    bp: Annotated[str | None, Meta(title='bid_price')] | None = None
    bs: Annotated[str | None, Meta(title='bid_size')] | None = None
    dividend: str | None = None
    dividend_yield: str | None = None
    eps_adj: str | None = None
    fr: Annotated[str | None, Meta(title='funding_rate')] | None = None
    ft: Annotated[str | None, Meta(title='next_funding_time')] | None = None
    h: Annotated[str | None, Meta(title='high_24h')] | None = None
    ip: Annotated[str | None, Meta(title='index_price')] | None = None
    l: Annotated[str | None, Meta(title='low_24h')] | None = None
    market_cap: str | None = None
    mp: Annotated[str | None, Meta(title='mark_price')] | None = None
    o: Annotated[str | None, Meta(title='open_24h')] | None = None
    oi: Annotated[str | None, Meta(title='open_interest')] | None = None
    p: Annotated[str | None, Meta(title='last_price')] | None = None
    price_to_earnings: str | None = None
    q: Annotated[str | None, Meta(title='last_size')] | None = None
    shares_outstanding_weighted_adj: str | None = None
    sp: Annotated[str | None, Meta(title='last_settlement_price')] | None = None
    v: Annotated[str | None, Meta(title='volume_24h')] | None = None
    vm: Annotated[str | None, Meta(title='volume_30d')] | None = None
    xh: Annotated[str | None, Meta(title='session_high')] | None = None
    xl: Annotated[str | None, Meta(title='session_low')] | None = None
    xo: Annotated[str | None, Meta(title='session_open')] | None = None
    xv: Annotated[str | None, Meta(title='session_volume')] | None = None


class TickersResponse(Struct):
    tickers: List[Ticker]
