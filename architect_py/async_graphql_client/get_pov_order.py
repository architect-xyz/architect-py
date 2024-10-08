# Generated by ariadne-codegen
# Source: queries.async.graphql

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetPovOrder(BaseModel):
    pov_order: Optional["GetPovOrderPovOrder"] = Field(alias="povOrder")


class GetPovOrderPovOrder(BaseModel):
    name: str
    order_id: Any = Field(alias="orderId")
    market_id: Any = Field(alias="marketId")
    dir: Any
    target_volume_frac: Any = Field(alias="targetVolumeFrac")
    min_order_quantity: Any = Field(alias="minOrderQuantity")
    max_quantity: Any = Field(alias="maxQuantity")
    end_time: Any = Field(alias="endTime")
    account_id: Optional[Any] = Field(alias="accountId")
    take_through_frac: Optional[Any] = Field(alias="takeThroughFrac")


GetPovOrder.model_rebuild()
