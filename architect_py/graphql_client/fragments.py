# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BeforeValidator, Field

from architect_py.scalars import OrderDir, TradableProduct, parse_tradable_product

from .base_model import BaseModel
from .enums import (
    CancelStatus,
    CandleWidth,
    MinOrderQuantityUnit,
    OrderSource,
    OrderStatus,
    OrderType,
    TimeInForce,
)


class AccountSummaryFields(BaseModel):
    account: UUID
    timestamp: datetime
    balances: List["AccountSummaryFieldsBalances"]
    positions: List["AccountSummaryFieldsPositions"]
    unrealized_pnl: Optional[Decimal] = Field(alias="unrealizedPnl")
    realized_pnl: Optional[Decimal] = Field(alias="realizedPnl")
    equity: Optional[Decimal]
    yesterday_equity: Optional[Decimal] = Field(alias="yesterdayEquity")
    cash_excess: Optional[Decimal] = Field(alias="cashExcess")
    purchasing_power: Optional[Decimal] = Field(alias="purchasingPower")
    total_margin: Optional[Decimal] = Field(alias="totalMargin")
    position_margin: Optional[Decimal] = Field(alias="positionMargin")


class AccountSummaryFieldsBalances(BaseModel):
    product: str
    balance: Decimal


class AccountSummaryFieldsPositions(BaseModel):
    symbol: Annotated[TradableProduct, BeforeValidator(parse_tradable_product)]
    quantity: Decimal
    trade_time: Optional[datetime] = Field(alias="tradeTime")
    cost_basis: Optional[Decimal] = Field(alias="costBasis")
    break_even_price: Optional[Decimal] = Field(alias="breakEvenPrice")
    liquidation_price: Optional[Decimal] = Field(alias="liquidationPrice")


class AccountWithPermissionsFields(BaseModel):
    account: "AccountWithPermissionsFieldsAccount"
    trader: str
    permissions: "AccountWithPermissionsFieldsPermissions"


class AccountWithPermissionsFieldsAccount(BaseModel):
    id: UUID
    name: str


class AccountWithPermissionsFieldsPermissions(BaseModel):
    list: bool
    view: bool
    trade: bool
    reduce_or_close: bool = Field(alias="reduceOrClose")
    set_limits: bool = Field(alias="setLimits")


class CancelFields(BaseModel):
    cancel_id: UUID = Field(alias="cancelId")
    order_id: str = Field(alias="orderId")
    recv_time: Optional[datetime] = Field(alias="recvTime")
    status: CancelStatus
    reject_reason: Optional[str] = Field(alias="rejectReason")


class CandleFields(BaseModel):
    timestamp: Optional[datetime]
    width: CandleWidth
    open: Optional[Decimal]
    high: Optional[Decimal]
    low: Optional[Decimal]
    close: Optional[Decimal]
    volume: Decimal


class ExecutionInfoFields(BaseModel):
    symbol: str
    execution_venue: str = Field(alias="executionVenue")
    tick_size: Optional[Decimal] = Field(alias="tickSize")
    step_size: Decimal = Field(alias="stepSize")
    min_order_quantity: Decimal = Field(alias="minOrderQuantity")
    min_order_quantity_unit: MinOrderQuantityUnit = Field(alias="minOrderQuantityUnit")
    is_delisted: bool = Field(alias="isDelisted")
    initial_margin: Optional[Decimal] = Field(alias="initialMargin")
    maintenance_margin: Optional[Decimal] = Field(alias="maintenanceMargin")


class L2BookLevelFields(BaseModel):
    price: Decimal
    size: Decimal


class L2BookFields(BaseModel):
    timestamp: Optional[datetime]
    bids: List["L2BookFieldsBids"]
    asks: List["L2BookFieldsAsks"]


class L2BookFieldsBids(L2BookLevelFields):
    pass


class L2BookFieldsAsks(L2BookLevelFields):
    pass


class MarketStatusFields(BaseModel):
    symbol: str
    is_trading: Optional[bool] = Field(alias="isTrading")
    is_quoting: Optional[bool] = Field(alias="isQuoting")


class MarketTickerFields(BaseModel):
    symbol: str
    timestamp: Optional[datetime]
    bid_price: Optional[Decimal] = Field(alias="bidPrice")
    bid_size: Optional[Decimal] = Field(alias="bidSize")
    ask_price: Optional[Decimal] = Field(alias="askPrice")
    ask_size: Optional[Decimal] = Field(alias="askSize")
    last_price: Optional[Decimal] = Field(alias="lastPrice")
    last_size: Optional[Decimal] = Field(alias="lastSize")


class OrderFields(BaseModel):
    id: str
    parent_id: Optional[str] = Field(alias="parentId")
    recv_time: Optional[datetime] = Field(alias="recvTime")
    status: OrderStatus
    reject_reason: Optional[str] = Field(alias="rejectReason")
    reject_message: Optional[str] = Field(alias="rejectMessage")
    symbol: str
    trader: str
    account: UUID
    dir: OrderDir
    quantity: Decimal
    filled_quantity: Decimal = Field(alias="filledQuantity")
    average_fill_price: Optional[Decimal] = Field(alias="averageFillPrice")
    order_type: OrderType = Field(alias="orderType")
    limit_price: Optional[Decimal] = Field(alias="limitPrice")
    post_only: Optional[bool] = Field(alias="postOnly")
    trigger_price: Optional[Decimal] = Field(alias="triggerPrice")
    time_in_force: TimeInForce = Field(alias="timeInForce")
    good_til_date: Optional[datetime] = Field(alias="goodTilDate")
    source: OrderSource
    execution_venue: str = Field(alias="executionVenue")


class SpreadLegFields(BaseModel):
    product: str
    quantity: Decimal


class ProductInfoFields(BaseModel):
    typename__: str = Field(alias="__typename")
    symbol: str
    product_type: str = Field(alias="productType")
    underlying: Optional[str]
    multiplier: Optional[Decimal]
    derivative_kind: Optional[str] = Field(alias="derivativeKind")
    first_notice_date: Optional[date] = Field(alias="firstNoticeDate")
    primary_venue: Optional[str] = Field(alias="primaryVenue")
    price_display_format: Optional[str] = Field(alias="priceDisplayFormat")
    spread_legs: Optional[List["ProductInfoFieldsSpreadLegs"]] = Field(
        alias="spreadLegs"
    )


class ProductInfoFieldsSpreadLegs(SpreadLegFields):
    pass


AccountSummaryFields.model_rebuild()
AccountWithPermissionsFields.model_rebuild()
CancelFields.model_rebuild()
CandleFields.model_rebuild()
ExecutionInfoFields.model_rebuild()
L2BookLevelFields.model_rebuild()
L2BookFields.model_rebuild()
MarketStatusFields.model_rebuild()
MarketTickerFields.model_rebuild()
OrderFields.model_rebuild()
SpreadLegFields.model_rebuild()
ProductInfoFields.model_rebuild()
