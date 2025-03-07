# generated by datamodel-codegen:
#   filename:  Oms/OpenOrdersRequest.json

from __future__ import annotations
from architect_py.grpc_client.Oms.OpenOrdersResponse import OpenOrdersResponse

from typing import List, Optional

from msgspec import Struct

from .. import definitions


class OpenOrdersRequest(Struct):
    account: Optional[definitions.AccountIdOrName] = None
    order_ids: Optional[List[definitions.OrderId]] = None
    parent_order_id: Optional[definitions.OrderId] = None
    symbol: Optional[str] = None
    trader: Optional[definitions.TraderIdOrEmail] = None
    venue: Optional[str] = None

    @staticmethod
    def get_response_type():
        return ResponseType

    @staticmethod
    def get_route() -> str:
        return route

    @staticmethod
    def get_unary_type():
        return unary_type


ResponseType = OpenOrdersResponse
route = "/json.architect.Oms/OpenOrders"
unary_type = "unary"
