# generated by datamodel-codegen:
#   filename:  Orderflow_DropcopyRequest.json

from __future__ import annotations

from typing import Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class DropcopyRequest(Struct):
    aberrant_fills: Optional[bool] = False
    account: Optional[AccountIdOrName] = None
    execution_venue: Optional[str] = None
    fills: Optional[bool] = True
    orders: Optional[bool] = False
    trader: Optional[TraderIdOrEmail] = None
