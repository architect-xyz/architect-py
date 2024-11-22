# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from architect_py.scalars import OrderDir

from .base_model import BaseModel
from .enums import AlgoRunningStatus


class GetPovStatus(BaseModel):
    pov_status: List["GetPovStatusPovStatus"] = Field(alias="povStatus")


class GetPovStatusPovStatus(BaseModel):
    order_id: str = Field(alias="orderId")
    order: Optional["GetPovStatusPovStatusOrder"]
    creation_time: datetime = Field(alias="creationTime")
    status: AlgoRunningStatus
    fraction_complete: Optional[float] = Field(alias="fractionComplete")
    realized_volume_frac: Optional[Decimal] = Field(alias="realizedVolumeFrac")
    market_volume: Decimal = Field(alias="marketVolume")
    quantity_filled: Decimal = Field(alias="quantityFilled")


class GetPovStatusPovStatusOrder(BaseModel):
    name: str
    order_id: str = Field(alias="orderId")
    market_id: str = Field(alias="marketId")
    dir: OrderDir
    target_volume_frac: Decimal = Field(alias="targetVolumeFrac")
    min_order_quantity: Decimal = Field(alias="minOrderQuantity")
    max_quantity: Decimal = Field(alias="maxQuantity")
    end_time: datetime = Field(alias="endTime")
    account_id: Optional[str] = Field(alias="accountId")
    take_through_frac: Optional[Decimal] = Field(alias="takeThroughFrac")


GetPovStatus.model_rebuild()
GetPovStatusPovStatus.model_rebuild()
