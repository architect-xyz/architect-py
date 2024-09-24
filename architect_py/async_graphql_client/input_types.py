# Generated by ariadne-codegen
# Source: schema.graphql

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    CreateOrderType,
    CreateTimeInForceInstruction,
    OrderSource,
    ReferencePrice,
)


class CreateMMAlgo(BaseModel):
    name: Any
    market: Any
    account: Optional[Any] = None
    buy_quantity: Any = Field(alias="buyQuantity")
    sell_quantity: Any = Field(alias="sellQuantity")
    min_position: Any = Field(alias="minPosition")
    max_position: Any = Field(alias="maxPosition")
    max_improve_bbo: Any = Field(alias="maxImproveBbo")
    position_tilt: Any = Field(alias="positionTilt")
    reference_price: ReferencePrice = Field(alias="referencePrice")
    ref_dist_frac: Any = Field(alias="refDistFrac")
    tolerance_frac: Any = Field(alias="toleranceFrac")
    fill_lockout_ms: int = Field(alias="fillLockoutMs")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")


class CreateOrder(BaseModel):
    market: Any
    dir: Any
    quantity: Any
    account: Optional[Any] = None
    order_type: CreateOrderType = Field(alias="orderType")
    limit_price: Optional[Any] = Field(alias="limitPrice", default=None)
    post_only: Optional[bool] = Field(alias="postOnly", default=None)
    trigger_price: Optional[Any] = Field(alias="triggerPrice", default=None)
    time_in_force: "CreateTimeInForce" = Field(alias="timeInForce")
    quote_id: Optional[Any] = Field(alias="quoteId", default=None)
    source: Optional[OrderSource] = None


class CreatePovAlgo(BaseModel):
    name: Any
    market: Any
    dir: Any
    target_volume_frac: Any = Field(alias="targetVolumeFrac")
    min_order_quantity: Any = Field(alias="minOrderQuantity")
    max_quantity: Any = Field(alias="maxQuantity")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    end_time: Any = Field(alias="endTime")
    account: Optional[Any] = None
    take_through_frac: Optional[Any] = Field(alias="takeThroughFrac", default=None)


class CreateSmartOrderRouterAlgo(BaseModel):
    markets: List[Any]
    base: Any
    quote: Any
    dir: Any
    limit_price: Any = Field(alias="limitPrice")
    target_size: Any = Field(alias="targetSize")
    execution_time_limit_ms: int = Field(alias="executionTimeLimitMs")


class CreateSpreadAlgo(BaseModel):
    name: Any
    market: Any
    account: Optional[Any] = None
    buy_quantity: Any = Field(alias="buyQuantity")
    sell_quantity: Any = Field(alias="sellQuantity")
    min_position: Any = Field(alias="minPosition")
    max_position: Any = Field(alias="maxPosition")
    max_improve_bbo: Any = Field(alias="maxImproveBbo")
    position_tilt: Any = Field(alias="positionTilt")
    reference_price: ReferencePrice = Field(alias="referencePrice")
    ref_dist_frac: Any = Field(alias="refDistFrac")
    tolerance_frac: Any = Field(alias="toleranceFrac")
    hedge_market: "CreateSpreadAlgoHedgeMarket" = Field(alias="hedgeMarket")
    fill_lockout_ms: int = Field(alias="fillLockoutMs")
    order_lockout_ms: int = Field(alias="orderLockoutMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")


class CreateSpreadAlgoHedgeMarket(BaseModel):
    market: Any
    conversion_ratio: Any = Field(alias="conversionRatio")
    premium: Any
    hedge_frac: Any = Field(alias="hedgeFrac")


class CreateTimeInForce(BaseModel):
    instruction: CreateTimeInForceInstruction
    good_til_date: Optional[Any] = Field(alias="goodTilDate", default=None)


class CreateTwapAlgo(BaseModel):
    name: Any
    market: Any
    dir: Any
    quantity: Any
    interval_ms: int = Field(alias="intervalMs")
    reject_lockout_ms: int = Field(alias="rejectLockoutMs")
    end_time: Any = Field(alias="endTime")
    account: Optional[Any] = None
    take_through_frac: Optional[Any] = Field(alias="takeThroughFrac", default=None)


class MarketFilter(BaseModel):
    search_string: Optional[Any] = Field(alias="searchString", default=None)
    base: Optional[Any] = None
    quote: Optional[Any] = None
    venue: Optional[Any] = None
    route: Optional[Any] = None
    underlying: Optional[Any] = None
    max_results: Optional[int] = Field(alias="maxResults", default=None)
    results_offset: Optional[int] = Field(alias="resultsOffset", default=None)
    only_favorites: Optional[bool] = Field(alias="onlyFavorites", default=None)
    sort_by_volume_desc: Optional[bool] = Field(alias="sortByVolumeDesc", default=None)
    include_delisted: Optional[bool] = Field(alias="includeDelisted", default=None)


class UpdateMarket(BaseModel):
    market_id: Any = Field(alias="marketId")
    is_favorite: bool = Field(alias="isFavorite")
