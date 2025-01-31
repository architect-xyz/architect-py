# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import CancelStatus


class CancelOrder(BaseModel):
    oms: "CancelOrderOms"


class CancelOrderOms(BaseModel):
    cancel_order: "CancelOrderOmsCancelOrder" = Field(alias="cancelOrder")


class CancelOrderOmsCancelOrder(BaseModel):
    id: Any
    order_id: str = Field(alias="orderId")
    status: CancelStatus
    reject_reason: Optional[str] = Field(alias="rejectReason")


CancelOrder.model_rebuild()
CancelOrderOms.model_rebuild()
