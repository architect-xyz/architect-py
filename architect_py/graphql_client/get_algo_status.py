# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AlgoKind, AlgoRunningStatus


class GetAlgoStatus(BaseModel):
    algo_status: List["GetAlgoStatusAlgoStatus"] = Field(alias="algoStatus")


class GetAlgoStatusAlgoStatus(BaseModel):
    order_id: str = Field(alias="orderId")
    order: Optional["GetAlgoStatusAlgoStatusOrder"]
    creation_time: datetime = Field(alias="creationTime")
    status: AlgoRunningStatus
    last_status_change: datetime = Field(alias="lastStatusChange")
    fraction_complete: Optional[float] = Field(alias="fractionComplete")


class GetAlgoStatusAlgoStatusOrder(BaseModel):
    order_id: str = Field(alias="orderId")
    trader: str
    account: Optional[str]
    algo: AlgoKind
    parent_order_id: Optional[str] = Field(alias="parentOrderId")
    markets: List[str]


GetAlgoStatus.model_rebuild()
GetAlgoStatusAlgoStatus.model_rebuild()
