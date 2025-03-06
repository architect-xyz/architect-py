# generated by datamodel-codegen:
#   filename:  Folio/AccountSummary.json

from __future__ import annotations

from decimal import Decimal
from typing import Annotated, Dict, List, Optional

from msgspec import Meta, Struct

from .. import definitions


class AccountSummary(Struct):
    account: str
    balances: Dict[str, Decimal]
    positions: Dict[str, List[definitions.AccountPosition]]
    timestamp: str
    cash_excess: Optional[
        Annotated[Optional[Decimal], Meta(description='Cash available to withdraw.')]
    ] = None
    """
    Cash available to withdraw.
    """
    equity: Optional[Decimal] = None
    position_margin: Optional[
        Annotated[
            Optional[Decimal],
            Meta(description='Margin requirement based on current positions only.'),
        ]
    ] = None
    """
    Margin requirement based on current positions only.
    """
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
    """
    Margin requirement calculated for worst-case based on open positions and working orders.
    """
    unrealized_pnl: Optional[Decimal] = None
    yesterday_equity: Optional[Decimal] = None
