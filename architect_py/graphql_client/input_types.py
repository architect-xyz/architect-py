# Generated by ariadne-codegen
# Source: schema.graphql

from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional

from pydantic import Field, PlainSerializer

from architect_py.scalars import Dir, serialize
from architect_py.utils.dt import convert_datetime_to_utc_str

from .base_model import BaseModel
from .enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
    OrderSource,
    ReferencePrice,
)


class CreateMMAlgo(BaseModel):
    name: str
    market: str
    account: Optional[str] = None
    buy_quantity: Decimal = Field(alias="buyQuantity")
    sell_quantity: Decimal = Field(alias="sellQuantity")
    min_position: Decimal = Field(alias="minPosition")
    max_position: Decimal = Field(alias="maxPosition")
    max_improve_bbo: Decimal = Field(alias="maxImproveBbo")
    position_tilt: Decimal = Field(alias="positionTilt")
    reference_price: ReferencePrice = Field(alias="referencePrice")
    ref_dist_frac: Decimal = Field(alias="refDistFrac")
    tolerance_frac: Decimal = Field(alias="toleranceFrac")
    fill_lockout_ms: int = Field(alias="fillLockoutMs")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")


class CreateOrder(BaseModel):
    market: str
    dir: Annotated[Dir, PlainSerializer(serialize)]
    quantity: Decimal
    account: Optional[str] = None
    order_type: CreateOrderType = Field(alias="orderType")
    limit_price: Optional[Decimal] = Field(alias="limitPrice", default=None)
    post_only: Optional[bool] = Field(alias="postOnly", default=None)
    trigger_price: Optional[Decimal] = Field(alias="triggerPrice", default=None)
    time_in_force: "CreateTimeInForce" = Field(alias="timeInForce")
    quote_id: Optional[str] = Field(alias="quoteId", default=None)
    source: Optional[OrderSource] = None


class CreatePovAlgo(BaseModel):
    name: str
    market: str
    dir: Annotated[Dir, PlainSerializer(serialize)]
    target_volume_frac: Decimal = Field(alias="targetVolumeFrac")
    min_order_quantity: Decimal = Field(alias="minOrderQuantity")
    max_quantity: Decimal = Field(alias="maxQuantity")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    end_time: Annotated[datetime, PlainSerializer(convert_datetime_to_utc_str)] = Field(
        alias="endTime"
    )
    account: Optional[str] = None
    take_through_frac: Optional[Decimal] = Field(alias="takeThroughFrac", default=None)


class CreateSmartOrderRouterAlgo(BaseModel):
    markets: List[str]
    base: str
    quote: str
    dir: Annotated[Dir, PlainSerializer(serialize)]
    limit_price: Decimal = Field(alias="limitPrice")
    target_size: Decimal = Field(alias="targetSize")
    execution_time_limit_ms: int = Field(alias="executionTimeLimitMs")


class CreateSpreadAlgo(BaseModel):
    name: str
    market: str
    account: Optional[str] = None
    buy_quantity: Decimal = Field(alias="buyQuantity")
    sell_quantity: Decimal = Field(alias="sellQuantity")
    min_position: Decimal = Field(alias="minPosition")
    max_position: Decimal = Field(alias="maxPosition")
    max_improve_bbo: Decimal = Field(alias="maxImproveBbo")
    position_tilt: Decimal = Field(alias="positionTilt")
    reference_price: ReferencePrice = Field(alias="referencePrice")
    ref_dist_frac: Decimal = Field(alias="refDistFrac")
    tolerance_frac: Decimal = Field(alias="toleranceFrac")
    hedge_market: "CreateSpreadAlgoHedgeMarket" = Field(alias="hedgeMarket")
    fill_lockout_ms: int = Field(alias="fillLockoutMs")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")


class CreateSpreadAlgoHedgeMarket(BaseModel):
    market: str
    conversion_ratio: Decimal = Field(alias="conversionRatio")
    premium: Decimal
    hedge_frac: Decimal = Field(alias="hedgeFrac")


class CreateTimeInForce(BaseModel):
    instruction: CreateTimeInForceInstruction
    good_til_date: Optional[
        Annotated[datetime, PlainSerializer(convert_datetime_to_utc_str)]
    ] = Field(alias="goodTilDate", default=None)


class CreateTwapAlgo(BaseModel):
    name: str
    market: str
    dir: Annotated[Dir, PlainSerializer(serialize)]
    quantity: Decimal
    interval_ms: int = Field(alias="intervalMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")
    end_time: Annotated[datetime, PlainSerializer(convert_datetime_to_utc_str)] = Field(
        alias="endTime"
    )
    account: Optional[str] = None
    take_through_frac: Optional[Decimal] = Field(alias="takeThroughFrac", default=None)


class MarketFilter(BaseModel):
    search_string: Optional[str] = Field(alias="searchString", default=None)
    base: Optional[str] = None
    quote: Optional[str] = None
    venue: Optional[str] = None
    route: Optional[str] = None
    underlying: Optional[str] = None
    max_results: Optional[int] = Field(alias="maxResults", default=None)
    results_offset: Optional[int] = Field(alias="resultsOffset", default=None)
    only_favorites: Optional[bool] = Field(alias="onlyFavorites", default=None)
    sort_by_volume_desc: Optional[bool] = Field(alias="sortByVolumeDesc", default=None)
    include_delisted: Optional[bool] = Field(alias="includeDelisted", default=None)


class UpdateMarket(BaseModel):
    market_id: str = Field(alias="marketId")
    is_favorite: bool = Field(alias="isFavorite")


CreateOrder.model_rebuild()
CreateSpreadAlgo.model_rebuild()
