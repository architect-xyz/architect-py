# generated by datamodel-codegen:
#   filename:  Oms/CancelOrderRequest.json

from __future__ import annotations
from architect_py.grpc_client.Oms.Cancel import Cancel

from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class CancelOrderRequest(Struct):
    id: Annotated[definitions.OrderId, Meta(title="order_id")]
    xid: Optional[
        Annotated[
            Optional[str],
            Meta(
                description="If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.",
                title="cancel_id",
            ),
        ]
    ] = None
    """
    If not specified, one will be generated for you; note, in that case, you won't know for sure if the specific request went through.
    """

    @property
    def order_id(self) -> definitions.OrderId:
        return self.id

    @order_id.setter
    def order_id(self, value: definitions.OrderId) -> None:
        self.id = value

    @property
    def cancel_id(self) -> Optional[str]:
        return self.xid

    @cancel_id.setter
    def cancel_id(self, value: Optional[str]) -> None:
        self.xid = value

    @staticmethod
    def get_response_type():
        return Cancel

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Oms/CancelOrder"

    @staticmethod
    def get_unary_type():
        return "unary"
