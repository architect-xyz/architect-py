# generated by datamodel-codegen:
#   filename:  Cpty/CptyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Cpty.CptyResponse import (
    CptyResponse,
    Any,
    ReconcileOrder,
    ReconcileOpenOrder,
    UpdateAccountSummary,
)

from typing import Annotated, Optional, Union

from msgspec import Meta, Struct

from .. import definitions
from ..Oms.Cancel import Cancel
from ..Oms.Order import Order


class CancelOrder(Struct, omit_defaults=True, tag_field="t", tag="cancel_order"):
    cancel: Cancel
    original_order: Optional[Order] = None

    # below is a constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        cancel: Cancel,
        original_order: Optional[Order] = None,
    ):
        return cls(
            cancel,
            original_order,
        )

    def __str__(self) -> str:
        return f"CancelOrder(cancel={self.cancel},original_order={self.original_order})"


class Login(
    definitions.CptyLoginRequest, omit_defaults=True, tag_field="t", tag="login"
):
    pass


class Logout(
    definitions.CptyLogoutRequest, omit_defaults=True, tag_field="t", tag="logout"
):
    pass


class PlaceOrder(Order, omit_defaults=True, tag_field="t", tag="place_order"):
    pass


CptyRequest = Annotated[
    Union[Login, Logout, PlaceOrder, CancelOrder], Meta(title="CptyRequest")
]

CptyRequest_rpc_method = "duplex_stream"
CptyRequestResponseType = CptyResponse
CptyRequestUnannotatedResponseType = (
    dict[str, Any] | ReconcileOrder | ReconcileOpenOrder | UpdateAccountSummary
)
CptyRequest_route = "/json.architect.Cpty/Cpty"
