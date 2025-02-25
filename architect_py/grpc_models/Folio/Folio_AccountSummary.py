# generated by datamodel-codegen:
#   filename:  Folio_AccountSummary.json
#   timestamp: 2025-02-25T21:20:58+00:00

from __future__ import annotations

from typing import Annotated, Dict, List

from msgspec import Meta, Struct


class AccountPosition(Struct):
    quantity: str
    break_even_price: str | None = None
    cost_basis: str | None = None
    liquidation_price: str | None = None
    trade_time: (
        Annotated[
            str | None,
            Meta(description='The meaning of this field varies by reporting venue.'),
        ]
        | None
    ) = None


class AccountSummary(Struct):
    account: str
    balances: Dict[str, str]
    positions: Dict[str, List[AccountPosition]]
    timestamp: str
    cash_excess: (
        Annotated[str | None, Meta(description='Cash available to withdraw.')] | None
    ) = None
    equity: str | None = None
    position_margin: (
        Annotated[
            str | None,
            Meta(description='Margin requirement based on current positions only.'),
        ]
        | None
    ) = None
    purchasing_power: str | None = None
    realized_pnl: str | None = None
    total_margin: (
        Annotated[
            str | None,
            Meta(
                description='Margin requirement calculated for worst-case based on open positions and working orders.'
            ),
        ]
        | None
    ) = None
    unrealized_pnl: str | None = None
    yesterday_equity: str | None = None
