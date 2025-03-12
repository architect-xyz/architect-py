# generated by datamodel-codegen:
#   filename:  Cpty/CptyResponse.json

from __future__ import annotations

from typing import Annotated, Any, Dict, List, Optional, Union

from msgspec import Meta, Struct

from .. import definitions
from ..Oms.Order import Order


class UpdateAccountSummary(Struct, omit_defaults=True, tag="t", tag_field="as"):
    account: definitions.AccountIdOrName
    is_snapshot: bool
    timestamp: int
    timestamp_ns: Annotated[int, Meta(ge=0)]
    balances: Optional[Dict[str, Any]] = None
    positions: Optional[Dict[str, Any]] = None
    statistics: Optional[definitions.AccountStatistics] = None


class ReconcileOpenOrder(Struct, omit_defaults=True, tag="t", tag_field="oo"):
    orders: List[Order]
    snapshot_for_account: Optional[definitions.AccountIdOrName] = None


class ReconcileOrder(Order, tag="t", tag_field="ro"):
    pass


CptyResponse = Annotated[
    Union[Dict[str, Any], ReconcileOrder, ReconcileOpenOrder, UpdateAccountSummary],
    Meta(title="CptyResponse"),
]
