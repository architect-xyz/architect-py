# generated by datamodel-codegen:
#   filename:  Algo/ModifyAlgoOrderRequestForTwapAlgo.json

from __future__ import annotations
from architect_py.grpc_client.Algo.AlgoOrderForTwapAlgo import AlgoOrderForTwapAlgo

from msgspec import Struct

from .. import definitions


class ModifyAlgoOrderRequestForTwapAlgo(Struct, omit_defaults=True):
    algo_order_id: definitions.OrderId
    params: definitions.TwapParams

    @staticmethod
    def get_response_type():
        return AlgoOrderForTwapAlgo

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Algo/ModifyTwapAlgoOrder"

    @staticmethod
    def get_unary_type():
        return "unary"
