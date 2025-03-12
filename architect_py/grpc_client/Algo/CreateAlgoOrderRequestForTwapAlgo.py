# generated by datamodel-codegen:
#   filename:  Algo/CreateAlgoOrderRequestForTwapAlgo.json

from __future__ import annotations

from typing import Optional

from msgspec import Struct

from .. import definitions


class CreateAlgoOrderRequestForTwapAlgo(Struct):
    algo_name: str
    params: definitions.TwapParams
    account: Optional[str] = None
    algo_order_id: Optional[definitions.OrderId] = None
    parent_order_id: Optional[definitions.OrderId] = None
    trader: Optional[definitions.UserId] = None

    @staticmethod
    def get_response_type():
        return "&RESPONSE_TYPE:CreateAlgoOrderRequestForTwapAlgo"

    @staticmethod
    def get_route() -> str:
        return "&ROUTE:CreateAlgoOrderRequestForTwapAlgo"

    @staticmethod
    def get_unary_type():
        return "&UNARY_TYPE:CreateAlgoOrderRequestForTwapAlgo"
