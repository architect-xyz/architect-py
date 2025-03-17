# generated by datamodel-codegen:
#   filename:  Oms/PendingCancelsResponse.json

from __future__ import annotations

from typing import List

from msgspec import Struct

from .Cancel import Cancel


class PendingCancelsResponse(Struct, omit_defaults=True):
    pending_cancels: List[Cancel]

    # below is a constructor that takes all field titles as arguments for convenience
    @staticmethod
    def new(
        pending_cancels: List[Cancel],
    ) -> "PendingCancelsResponse":
        return PendingCancelsResponse(
            pending_cancels,
        )

    def __str__(self) -> str:
        return f"PendingCancelsResponse(pending_cancels={self.pending_cancels})"
