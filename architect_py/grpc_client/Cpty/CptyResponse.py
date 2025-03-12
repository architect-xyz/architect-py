# generated by datamodel-codegen:
#   filename:  Cpty/CptyResponse.json

from __future__ import annotations

from typing import Annotated, Any, Dict, List, Optional, Union

from msgspec import Meta, Struct

from .. import definitions
from ..Oms import Order


class UpdateAccountSummary(Struct):
    account: definitions.AccountIdOrName
    is_snapshot: bool
    timestamp: int
    timestamp_ns: Annotated[int, Meta(ge=0)]
    balances: Optional[Dict[str, Any]] = None
    positions: Optional[Dict[str, Any]] = None
    statistics: Optional[definitions.AccountStatistics] = None


class ReconcileOpenOrder(Struct):
    orders: List[Order]
    snapshot_for_account: Optional[definitions.AccountIdOrName] = None


CptyResponse = Annotated[
    Union[Dict[str, Any], Order, ReconcileOpenOrder, UpdateAccountSummary],
    Meta(title='CptyResponse'),
]
