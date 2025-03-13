# generated by datamodel-codegen:
#   filename:  Cpty/CptyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Cpty.CptyResponse import CptyResponse
from architect_py.grpc_client.Cpty.CptyResponse import CptyResponse

from typing import Annotated, Optional, Union

from msgspec import Meta, Struct

from .. import definitions
from ..Oms.Cancel import Cancel
from ..Oms.Order import Order


class CancelOrder(Struct, omit_defaults=True, tag_field="t", tag="cancel_order"):
    cancel: Cancel
    original_order: Optional[Order] = None


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


unary = "duplex_stream"
response_type = CptyResponse
route = "/json.architect.Cpty/Cpty"
