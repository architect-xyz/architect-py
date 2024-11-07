# Generated by ariadne-codegen
# Source: queries.graphql

from decimal import Decimal
from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AlgoRunningStatus, MMAlgoKind, ReferencePrice


class GetSpreadStatus(BaseModel):
    spread_algo_status: List["GetSpreadStatusSpreadAlgoStatus"] = Field(
        alias="spreadAlgoStatus"
    )


class GetSpreadStatusSpreadAlgoStatus(BaseModel):
    order_id: Any = Field(alias="orderId")
    order: Optional["GetSpreadStatusSpreadAlgoStatusOrder"]
    creation_time: Any = Field(alias="creationTime")
    status: AlgoRunningStatus
    position: Decimal
    hedge_position: Decimal = Field(alias="hedgePosition")
    miss_ratio: Decimal = Field(alias="missRatio")
    effective_spread: Optional[Decimal] = Field(alias="effectiveSpread")
    buy_status: "GetSpreadStatusSpreadAlgoStatusBuyStatus" = Field(alias="buyStatus")
    sell_status: "GetSpreadStatusSpreadAlgoStatusSellStatus" = Field(alias="sellStatus")
    kind: MMAlgoKind


class GetSpreadStatusSpreadAlgoStatusOrder(BaseModel):
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
    account: Optional[Any]


class GetSpreadStatusSpreadAlgoStatusBuyStatus(BaseModel):
    last_order_time: Any = Field(alias="lastOrderTime")
    last_fill_time: Any = Field(alias="lastFillTime")
    last_reject_time: Any = Field(alias="lastRejectTime")
    open_order: Optional["GetSpreadStatusSpreadAlgoStatusBuyStatusOpenOrder"] = Field(
        alias="openOrder"
    )
    reference_price: Optional[Decimal] = Field(alias="referencePrice")


class GetSpreadStatusSpreadAlgoStatusBuyStatusOpenOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    price: Decimal
    quantity: Decimal
    cancel_pending: bool = Field(alias="cancelPending")


class GetSpreadStatusSpreadAlgoStatusSellStatus(BaseModel):
    last_order_time: Any = Field(alias="lastOrderTime")
    last_fill_time: Any = Field(alias="lastFillTime")
    last_reject_time: Any = Field(alias="lastRejectTime")
    open_order: Optional["GetSpreadStatusSpreadAlgoStatusSellStatusOpenOrder"] = Field(
        alias="openOrder"
    )
    reference_price: Optional[Decimal] = Field(alias="referencePrice")


class GetSpreadStatusSpreadAlgoStatusSellStatusOpenOrder(BaseModel):
    order_id: Any = Field(alias="orderId")
    price: Decimal
    quantity: Decimal
    cancel_pending: bool = Field(alias="cancelPending")


GetSpreadStatus.model_rebuild()
GetSpreadStatusSpreadAlgoStatus.model_rebuild()
GetSpreadStatusSpreadAlgoStatusBuyStatus.model_rebuild()
GetSpreadStatusSpreadAlgoStatusSellStatus.model_rebuild()
