from dataclasses import dataclass
from decimal import Decimal

from typing import Optional


@dataclass
class SimplePosition:
    quantity: Decimal
    average_price: Decimal
    mark: Optional[Decimal]

    @property
    def pnl(self) -> Optional[Decimal]:
        if self.mark is None:
            return None
        return self.quantity * (self.mark - self.average_price)

    @property
    def notional(self) -> Optional[Decimal]:
        if self.mark is None:
            return None
        return self.quantity * self.mark


@dataclass
class Balance:
    amount: Decimal
    total_margin: Decimal
    position_margin: Decimal
    purchasing_power: Decimal
    cash_excess: Decimal
    yesterday_balance: Decimal

    @property
    def change_in_balance(self) -> Decimal:
        return self.amount - self.yesterday_balance

    @property
    def order_margin(self) -> Decimal:
        return self.total_margin - self.position_margin


@dataclass
class BalancesAndPositions:
    account_name: str
    usd_balance: Balance
    positions: dict[str, SimplePosition]

    @property
    def total_pnl_of_positions(self) -> Decimal:
        # this ignores positions with no mark
        pnls = [
            position.pnl
            for position in self.positions.values()
            if position.pnl is not None
        ]
        if len(pnls) == 0:
            return Decimal(0)
        else:
            return sum(pnls)  # type: ignore
