# generated by datamodel-codegen:
#   filename:  ModifyAlgoOrderRequest_for_TwapAlgo.json

from __future__ import annotations
import grpc
import msgspec
from architect_py.grpc_client.Algo.AlgoOrder_for_TwapAlgo import AlgoOrderForTwapAlgo
from architect_py.grpc_client.request import RequestUnary

from decimal import Decimal


from enum import Enum
from typing import Annotated, Optional

from msgspec import Meta, Struct



class Dir(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


HumanDuration = str


class OrderId(Struct):
    seqid: str
    seqno: Annotated[int, Meta(ge=0)]


class TwapParams(Struct):
    dir: Dir
    end_time: str
    execution_venue: str
    interval: HumanDuration
    quantity: Decimal
    reject_lockout: HumanDuration
    symbol: str
    take_through_frac: Optional[Decimal] = None


class ModifyAlgoOrderRequestForTwapAlgo(Struct):
    algo_order_id: OrderId
    params: TwapParams

    @staticmethod
    def create_stub(channel: grpc.aio.Channel, encoder: msgspec.json.Encoder) -> grpc.aio.UnaryUnaryMultiCallable["ModifyAlgoOrderRequestForTwapAlgo", AlgoOrderForTwapAlgo]:
        return channel.unary_unary(
            "/json.architect.Algo/ModifyTwapAlgoOrder",
            request_serializer=encoder.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=AlgoOrderForTwapAlgo
            ),
        )

ModifyAlgoOrderRequestForTwapAlgoRequestHelper = RequestUnary(ModifyAlgoOrderRequestForTwapAlgo, AlgoOrderForTwapAlgo, "/json.architect.Algo/ModifyTwapAlgoOrder")
