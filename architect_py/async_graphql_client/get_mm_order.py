# Generated by ariadne-codegen
# Source: queries.async.graphql

from decimal import Decimal
from typing import Any, Optional

from pydantic import Field

from architect_py.scalars import AccountId

from .base_model import BaseModel
from .enums import ReferencePrice


class GetMmOrder(BaseModel):
    mm_algo_order: Optional["GetMmOrderMmAlgoOrder"] = Field(alias="mmAlgoOrder")


class GetMmOrderMmAlgoOrder(BaseModel):
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


GetMmOrder.model_rebuild()
