# Generated by ariadne-codegen
# Source: ../../queries.async.graphql

from typing import Any, List, Optional

from pydantic import Field

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
    order_id: Any = Field(alias="orderId")
    order: Optional["GetSmartOrderRouterStatusSmartOrderRouterStatusStatusOrder"]
    creation_time: Any = Field(alias="creationTime")
    status: AlgoRunningStatus
    last_status_change: Any = Field(alias="lastStatusChange")
    fraction_complete: Optional[float] = Field(alias="fractionComplete")


class GetSmartOrderRouterStatusSmartOrderRouterStatusStatusOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    trader: Any
    account: Optional[Any]
    algo: AlgoKind
    parent_order_id: Optional[Any] = Field(alias="parentOrderId")
    markets: List[Any]


class GetSmartOrderRouterStatusSmartOrderRouterStatusOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    markets: List["GetSmartOrderRouterStatusSmartOrderRouterStatusOrderMarkets"]
    dir: Any
    limit_price: Any = Field(alias="limitPrice")
    target_size: Any = Field(alias="targetSize")
    execution_time_limit_ms: int = Field(alias="executionTimeLimitMs")
    parent_order_id: Optional[Any] = Field(alias="parentOrderId")


class GetSmartOrderRouterStatusSmartOrderRouterStatusOrderMarkets(BaseModel):
    id: Any


GetSmartOrderRouterStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatusStatus.model_rebuild()
GetSmartOrderRouterStatusSmartOrderRouterStatusOrder.model_rebuild()
