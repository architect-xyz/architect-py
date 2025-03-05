# generated by datamodel-codegen:
#   filename:  CreateAlgoOrderRequest_for_TwapAlgo.json

from __future__ import annotations
from architect_py.grpc_client.Algo.AlgoOrder_for_TwapAlgo import AlgoOrderForTwapAlgo
from architect_py.grpc_client.request import RequestUnary


from decimal import Decimal
from enum import Enum
from typing import Annotated, Optional

from msgspec import Meta, Struct

DecimalModel = Decimal


class Dir(str, Enum):
    """
    An order side/direction or a trade execution side/direction. In GraphQL these are serialized as "buy" or "sell".
    """

    BUY = 'BUY'
    SELL = 'SELL'


HumanDuration = str


class OrderId(Struct):
    """
    System-unique, persistent order identifiers
    """

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


UserId = str


class CreateAlgoOrderRequestForTwapAlgo(Struct):
    algo_name: str
    params: TwapParams
    account: Optional[str] = None
    algo_order_id: Optional[OrderId] = None
    parent_order_id: Optional[OrderId] = None
    trader: Optional[UserId] = None

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(CreateAlgoOrderRequestForTwapAlgo, AlgoOrderForTwapAlgo, "/json.architect.Algo/CreateTwapAlgoOrder")

