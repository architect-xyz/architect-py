# generated by datamodel-codegen:
#   filename:  Oms_PendingCancelsRequest.json

from __future__ import annotations

from typing import List, Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class PendingCancelsRequest(Struct):
    account: Optional[AccountIdOrName] = None
    cancel_ids: Optional[List[str]] = None
    symbol: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None
    venue: Optional[str] = None
