# generated by datamodel-codegen:
#   filename:  Orderflow/DropcopyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Orderflow.Dropcopy import (
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
