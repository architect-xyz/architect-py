# generated by datamodel-codegen:
#   filename:  AccountSummariesResponse.json

from __future__ import annotations
from decimal import Decimal


from typing import Annotated, Mapping, Optional, Sequence

from msgspec import Meta, Struct



class AccountPosition(Struct):
    quantity: Decimal
    break_even_price: Optional[Decimal] = None
    cost_basis: Optional[Decimal] = None
    liquidation_price: Optional[Decimal] = None
    trade_time: Optional[
        Annotated[
            Optional[str],
            Meta(description='The meaning of this field varies by reporting venue.'),
        ]
    ] = None


class AccountSummary(Struct):
    account: str
    balances: Mapping[str, Decimal]
    positions: Mapping[str, Sequence[AccountPosition]]
    timestamp: str
    cash_excess: Optional[
        Annotated[Optional[Decimal], Meta(description='Cash available to withdraw.')]
    ] = None
    equity: Optional[Decimal] = None
    position_margin: Optional[
        Annotated[
            Optional[Decimal],
            Meta(description='Margin requirement based on current positions only.'),
        ]
    ] = None
    purchasing_power: Optional[Decimal] = None
    realized_pnl: Optional[Decimal] = None
    total_margin: Optional[
        Annotated[
            Optional[Decimal],
            Meta(
                description='Margin requirement calculated for worst-case based on open positions and working orders.'
            ),
        ]
    ] = None
    unrealized_pnl: Optional[Decimal] = None
    yesterday_equity: Optional[Decimal] = None


class AccountSummariesResponse(Struct):
    account_summaries: Sequence[AccountSummary]
