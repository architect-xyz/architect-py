# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from architect_py.scalars import OrderDir

from .base_model import BaseModel
from .enums import AlgoKind, AlgoRunningStatus


class GetSmartOrderRouterStatus(BaseModel):
    smart_order_router_status: List[
        "GetSmartOrderRouterStatusSmartOrderRouterStatus"
    ] = Field(alias="smartOrderRouterStatus")


class GetSmartOrderRouterStatusSmartOrderRouterStatus(BaseModel):
    status: "GetSmartOrderRouterStatusSmartOrderRouterStatusStatus"
    order: Optional["GetSmartOrderRouterStatusSmartOrderRouterStatusOrder"]


class GetSmartOrderRouterStatusSmartOrderRouterStatusStatus(BaseModel):
    order_id: str = Field(alias="orderId")
    order: Optional["GetSmartOrderRouterStatusSmartOrderRouterStatusStatusOrder"]
    creation_time: datetime = Field(alias="creationTime")
    status: AlgoRunningStatus
    last_status_change: datetime = Field(alias="lastStatusChange")
    fraction_complete: Optional[float] = Field(alias="fractionComplete")


class GetSmartOrderRouterStatusSmartOrderRouterStatusStatusOrder(BaseModel):
    order_id: str = Field(alias="orderId")
    trader: str
    account: Optional[str]
    algo: AlgoKind
    parent_order_id: Optional[str] = Field(alias="parentOrderId")
    markets: List[str]


class GetSmartOrderRouterStatusSmartOrderRouterStatusOrder(BaseModel):
    order_id: str = Field(alias="orderId")
    markets: List["GetSmartOrderRouterStatusSmartOrderRouterStatusOrderMarkets"]
    dir: OrderDir
    limit_price: Decimal = Field(alias="limitPrice")
    target_size: Decimal = Field(alias="targetSize")
    execution_time_limit_ms: int = Field(alias="executionTimeLimitMs")
    parent_order_id: Optional[str] = Field(alias="parentOrderId")


class GetSmartOrderRouterStatusSmartOrderRouterStatusOrderMarkets(BaseModel):
    id: str


GetSmartOrderRouterStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatusStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatusOrder.model_rebuild()
