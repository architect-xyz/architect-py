# Generated by ariadne-codegen
# Source: ../../queries.async.graphql

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AlgoKind


class GetAlgoOrder(BaseModel):
    algo_order: Optional["GetAlgoOrderAlgoOrder"] = Field(alias="algoOrder")


class GetAlgoOrderAlgoOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    trader: Any
    account: Optional[Any]
    algo: AlgoKind
    parent_order_id: Optional[Any] = Field(alias="parentOrderId")
    markets: List[Any]


GetAlgoOrder.model_rebuild()
