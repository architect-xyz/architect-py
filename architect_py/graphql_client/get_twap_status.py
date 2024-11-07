# Generated by ariadne-codegen
# Source: queries.graphql

from decimal import Decimal
from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AlgoRunningStatus


class GetTwapStatus(BaseModel):
    twap_status: List["GetTwapStatusTwapStatus"] = Field(alias="twapStatus")


class GetTwapStatusTwapStatus(BaseModel):
    order_id: Any = Field(alias="orderId")
    order: Optional["GetTwapStatusTwapStatusOrder"]
    creation_time: Any = Field(alias="creationTime")
    status: AlgoRunningStatus
    fraction_complete: Optional[float] = Field(alias="fractionComplete")
    realized_twap: Optional[Decimal] = Field(alias="realizedTwap")
    quantity_filled: Decimal = Field(alias="quantityFilled")


class GetTwapStatusTwapStatusOrder(BaseModel):
    name: str
    order_id: Any = Field(alias="orderId")
    market_id: Any = Field(alias="marketId")
    dir: Any
    quantity: Decimal
    end_time: Any = Field(alias="endTime")
    account_id: Optional[Any] = Field(alias="accountId")
    interval_ms: int = Field(alias="intervalMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")
    take_through_frac: Optional[Decimal] = Field(alias="takeThroughFrac")


GetTwapStatus.model_rebuild()
GetTwapStatusTwapStatus.model_rebuild()
