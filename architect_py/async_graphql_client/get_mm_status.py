# Generated by ariadne-codegen
# Source: queries.async.graphql

from decimal import Decimal
from typing import Any, List, Optional

from pydantic import Field

from architect_py.scalars import AccountId

from .base_model import BaseModel
from .enums import AlgoRunningStatus, MMAlgoKind, ReferencePrice


class GetMmStatus(BaseModel):
    mm_algo_status: List["GetMmStatusMmAlgoStatus"] = Field(alias="mmAlgoStatus")


class GetMmStatusMmAlgoStatus(BaseModel):
    order_id: Any = Field(alias="orderId")
    order: Optional["GetMmStatusMmAlgoStatusOrder"]
    creation_time: Any = Field(alias="creationTime")
    status: AlgoRunningStatus
    position: Decimal
    hedge_position: Decimal = Field(alias="hedgePosition")
    miss_ratio: Decimal = Field(alias="missRatio")
    effective_spread: Optional[Decimal] = Field(alias="effectiveSpread")
    buy_status: "GetMmStatusMmAlgoStatusBuyStatus" = Field(alias="buyStatus")
    sell_status: "GetMmStatusMmAlgoStatusSellStatus" = Field(alias="sellStatus")
    kind: MMAlgoKind


class GetMmStatusMmAlgoStatusOrder(BaseModel):
    name: str
    order_id: Any = Field(alias="orderId")
    market_id: Any = Field(alias="marketId")
    quantity_buy: Decimal = Field(alias="quantityBuy")
    quantity_sell: Decimal = Field(alias="quantitySell")
    min_position: Decimal = Field(alias="minPosition")
    max_position: Decimal = Field(alias="maxPosition")
    max_improve_bbo: Decimal = Field(alias="maxImproveBbo")
    position_tilt: Decimal = Field(alias="positionTilt")
    reference_price: ReferencePrice = Field(alias="referencePrice")
    ref_dist_frac: Decimal = Field(alias="refDistFrac")
    tolerance_frac: Decimal = Field(alias="toleranceFrac")
    account: Optional[AccountId]


class GetMmStatusMmAlgoStatusBuyStatus(BaseModel):
    last_order_time: Any = Field(alias="lastOrderTime")
    last_fill_time: Any = Field(alias="lastFillTime")
    last_reject_time: Any = Field(alias="lastRejectTime")
    open_order: Optional["GetMmStatusMmAlgoStatusBuyStatusOpenOrder"] = Field(
        alias="openOrder"
    )
    reference_price: Optional[Decimal] = Field(alias="referencePrice")


class GetMmStatusMmAlgoStatusBuyStatusOpenOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    price: Decimal
    quantity: Decimal
    cancel_pending: bool = Field(alias="cancelPending")


class GetMmStatusMmAlgoStatusSellStatus(BaseModel):
    last_order_time: Any = Field(alias="lastOrderTime")
    last_fill_time: Any = Field(alias="lastFillTime")
    last_reject_time: Any = Field(alias="lastRejectTime")
    open_order: Optional["GetMmStatusMmAlgoStatusSellStatusOpenOrder"] = Field(
        alias="openOrder"
    )
    reference_price: Optional[Decimal] = Field(alias="referencePrice")


class GetMmStatusMmAlgoStatusSellStatusOpenOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    price: Decimal
    quantity: Decimal
    cancel_pending: bool = Field(alias="cancelPending")


GetMmStatus.model_rebuild()
GetMmStatusMmAlgoStatus.model_rebuild()
GetMmStatusMmAlgoStatusBuyStatus.model_rebuild()
GetMmStatusMmAlgoStatusSellStatus.model_rebuild()
