# Generated by ariadne-codegen
# Source: queries.async.graphql

from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from architect_py.scalars import OrderDir

from .base_model import BaseModel


class GetSmartOrderRouterOrder(BaseModel):
    smart_order_router_order: Optional[
        "GetSmartOrderRouterOrderSmartOrderRouterOrder"
    ] = Field(alias="smartOrderRouterOrder")


class GetSmartOrderRouterOrderSmartOrderRouterOrder(BaseModel):
    order_id: str = Field(alias="orderId")
    markets: List["GetSmartOrderRouterOrderSmartOrderRouterOrderMarkets"]
    dir: OrderDir
    limit_price: Decimal = Field(alias="limitPrice")
    target_size: Decimal = Field(alias="targetSize")
    execution_time_limit_ms: int = Field(alias="executionTimeLimitMs")
    parent_order_id: Optional[str] = Field(alias="parentOrderId")


class GetSmartOrderRouterOrderSmartOrderRouterOrderMarkets(BaseModel):
    id: str


GetSmartOrderRouterOrder.model_rebuild()
GetSmartOrderRouterOrderSmartOrderRouterOrder.model_rebuild()
