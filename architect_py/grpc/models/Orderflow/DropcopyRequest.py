# generated by datamodel-codegen:
#   filename:  Orderflow/DropcopyRequest.json

from __future__ import annotations
from architect_py.grpc.models.Orderflow.Dropcopy import (
    Dropcopy,
    TaggedOrder,
    TaggedFill,
    TaggedAberrantFill,
)

from typing import Optional

from msgspec import Struct

from .. import definitions


class DropcopyRequest(Struct, omit_defaults=True):
    aberrant_fills: Optional[bool] = False
    account: Optional[definitions.AccountIdOrName] = None
    execution_venue: Optional[str] = None
    fills: Optional[bool] = True
    orders: Optional[bool] = False
    trader: Optional[definitions.TraderIdOrEmail] = None

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        aberrant_fills: Optional[bool] = False,
        account: Optional[definitions.AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        fills: Optional[bool] = True,
        orders: Optional[bool] = False,
        trader: Optional[definitions.TraderIdOrEmail] = None,
    ):
        return cls(
            aberrant_fills,
            account,
            execution_venue,
            fills,
            orders,
            trader,
        )

    def __str__(self) -> str:
        return f"DropcopyRequest(aberrant_fills={self.aberrant_fills},account={self.account},execution_venue={self.execution_venue},fills={self.fills},orders={self.orders},trader={self.trader})"

    @staticmethod
    def get_response_type():
        return Dropcopy

    @staticmethod
    def get_unannotated_response_type():
        return TaggedOrder | TaggedFill | TaggedAberrantFill

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Orderflow/Dropcopy"

    @staticmethod
    def get_rpc_method():
        return "stream"
