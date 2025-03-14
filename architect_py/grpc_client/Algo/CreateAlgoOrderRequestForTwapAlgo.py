# generated by datamodel-codegen:
#   filename:  Algo/CreateAlgoOrderRequestForTwapAlgo.json

from __future__ import annotations
from architect_py.grpc_client.Algo.AlgoOrderForTwapAlgo import AlgoOrderForTwapAlgo

from typing import Optional

from msgspec import Struct

from .. import definitions


class CreateAlgoOrderRequestForTwapAlgo(Struct, omit_defaults=True):
    algo_name: str
    params: definitions.TwapParams
    account: Optional[str] = None
    algo_order_id: Optional[definitions.OrderId] = None
    parent_order_id: Optional[definitions.OrderId] = None
    trader: Optional[definitions.UserId] = None

    @staticmethod
    def get_response_type():
        return AlgoOrderForTwapAlgo

    @staticmethod
    def get_unannotated_response_type():
        return AlgoOrderForTwapAlgo

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Algo/CreateTwapAlgoOrder"

    @staticmethod
    def get_rpc_method():
        return "unary"
