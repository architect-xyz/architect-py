from dataclasses import dataclass
from decimal import Decimal

from typing import Optional


@dataclass
class SimplePosition:
    quantity: Optional[Decimal]
    average_price: Optional[Decimal]
    mark: Optional[Decimal]

    @property
    def pnl(self) -> Optional[Decimal]:
        if self.mark is None or self.average_price is None or self.quantity is None:
            return None
        return self.quantity * (self.mark - self.average_price)

    @property
    def notional(self) -> Optional[Decimal]:
        if self.mark is None or self.quantity is None:
            return None
        return self.quantity * self.mark


@dataclass
class Balance:
    amount: Optional[Decimal]
    total_margin: Optional[Decimal]
    position_margin: Optional[Decimal]
    purchasing_power: Optional[Decimal]
    cash_excess: Optional[Decimal]
    yesterday_balance: Optional[Decimal]

    @staticmethod
    def new_empty() -> "Balance":
        return Balance(None, None, None, None, None, None)

    @property
    def change_in_balance(self) -> Optional[Decimal]:
        if self.amount and self.yesterday_balance:
            return self.amount - self.yesterday_balance
        else:
            return None

    @property
    def order_margin(self) -> Optional[Decimal]:
        if self.total_margin and self.position_margin:
            return self.total_margin - self.position_margin
        else:
            return None


@dataclass
class BalancesAndPositions:
    account_name: str
    usd_balance: Balance
    positions: dict[str, SimplePosition]

    @property
    def total_pnl_of_positions(self) -> tuple[Decimal, bool]:
        # this ignores positions with no mark

        total_pnl = Decimal(0)
        exists_none_pnl = False

        for position in self.positions.values():
            if position.pnl is None:
                exists_none_pnl = True
            else:
                total_pnl += position.pnl

        return total_pnl, exists_none_pnl
