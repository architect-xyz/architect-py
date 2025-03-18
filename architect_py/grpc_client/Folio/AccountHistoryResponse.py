# generated by datamodel-codegen:
#   filename:  Folio/AccountHistoryResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .AccountSummary import AccountSummary


class AccountHistoryResponse(Struct, omit_defaults=True):
    history: List[AccountSummary]

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        history: List[AccountSummary],
    ):
        return cls(
            history,
        )

    def __str__(self) -> str:
        return f"AccountHistoryResponse(history={self.history})"
