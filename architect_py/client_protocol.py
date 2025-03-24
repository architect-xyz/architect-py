# fmt: off

# mypy: ignore-errors

# Autogenerated from generate_protocol.py

# If you are here for function definitions, please refer to architect_py/async_cline.py
# This file is so that the sync client has good type hinting
# It is not used for anything else
# For maintainers: ensure that the types in this file are correct for correct type hinting


from typing import Union
from architect_py.grpc_client.definitions import *
from architect_py.graphql_client import *
from architect_py.async_client import *


class AsyncClientProtocol:
    def cancel_all_orders(self) -> bool: ...
    def cancel_order(self, order_id: OrderId) -> Cancel: ...
    @staticmethod
    def connect(*, api_key: str, api_secret: str, paper_trading: bool, host: str = 'app.architect.co', grpc_endpoint: str = 'cme.marketdata.architect.co', _port: Optional[int] = None, **kwargs: Any) -> AsyncClient: ...
    def get_account_history(self, account: str, from_inclusive: Optional[datetime] = None, to_exclusive: Optional[datetime] = None) -> list[AccountSummary]: ...
    def get_account_summaries(self, accounts: Optional[list[str]] = None, trader: Optional[str] = None) -> list[AccountSummary]: ...
    def get_account_summary(self, account: str) -> AccountSummary: ...
    def get_all_open_orders(self) -> list[Order]: ...
    def get_cme_first_notice_date(self, symbol: str) -> Optional[date]: ...
    def get_cme_future_from_root_month_year(self, root: str, month: int, year: int) -> str: ...
    def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]: ...
    def get_execution_info(self, symbol: TradableProduct, execution_venue: str) -> Optional[ExecutionInfoFields]: ...
    def get_execution_infos(self, symbols: Optional[list[TradableProduct]], execution_venue: Optional[str] = None) -> Sequence[ExecutionInfoFields]: ...
    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date: ...
    def get_fills(self, from_inclusive: Optional[datetime], to_exclusive: Optional[datetime], venue: Optional[str] = None, account: Optional[str] = None, order_id: Optional[OrderId] = None, limit: Optional[int] = None) -> HistoricalFillsResponse: ...
    def get_future_series(self, series_symbol: str) -> list[str]: ...
    def get_historical_candles(self, symbol: str, candle_width: CandleWidth, start: datetime, end: datetime) -> HistoricalCandlesResponse: ...
    def get_historical_orders(self, order_ids: Optional[list[OrderId]] = None, from_inclusive: Optional[datetime] = None, to_exclusive: Optional[datetime] = None, venue: Optional[str] = None, account: Optional[str] = None, parent_order_id: Optional[OrderId] = None) -> Sequence[Order]: ...
    def get_l1_book_snapshot(self, symbol: str, venue: str) -> MarketTickerFields: ...
    def get_l1_book_snapshots(self, symbols: list[str], venue: str) -> Sequence[MarketTickerFields]: ...
    def get_l2_book_snapshot(self, symbol: str, venue: str) -> L2BookFields: ...
    def get_market_snapshot(self, symbol: TradableProduct, venue: str) -> MarketTickerFields: ...
    def get_market_snapshots(self, symbols: list[TradableProduct], venue: str) -> Sequence[MarketTickerFields]: ...
    def get_market_status(self, symbol: TradableProduct, venue: str) -> MarketStatusFields: ...
    def get_open_orders(self, order_ids: Optional[list[OrderId]] = None, venue: Optional[str] = None, account: Optional[str] = None, trader: Optional[str] = None, symbol: Optional[str] = None, parent_order_id: Optional[OrderId] = None) -> list[Order]: ...
    def get_order(self, order_id: OrderId) -> Optional[Order]: ...
    def get_orders(self, order_ids: list[OrderId]) -> list[Optional[Order]]: ...
    def get_product_info(self, symbol: str) -> Optional[ProductInfoFields]: ...
    def get_product_infos(self, symbols: Optional[list[str]]) -> Sequence[ProductInfoFields]: ...
    def list_accounts(self) -> list[AccountWithPermissions]: ...
    def search_symbols(self, search_string: Optional[str] = None, execution_venue: Optional[str] = None, offset: int = 0, limit: int = 20) -> list[TradableProduct]: ...
    def send_limit_order(self, *, symbol: TradableProduct, execution_venue: Optional[str], odir: OrderDir, quantity: Decimal, limit_price: Decimal, order_type: PlaceOrderRequestType = PlaceOrderRequestType.LIMIT, time_in_force: Union[GoodTilDate, TimeInForceEnum] = TimeInForceEnum.DAY, price_round_method: Optional[TickRoundMethod] = None, account: Optional[str] = None, trader: Optional[str] = None, post_only: bool = False, trigger_price: Optional[Decimal] = None) -> Order: ...
    def send_market_pro_order(self, *, symbol: TradableProduct, execution_venue: str, odir: OrderDir, quantity: Decimal, time_in_force: Union[GoodTilDate, TimeInForceEnum] = TimeInForceEnum.DAY, account: Optional[str] = None, fraction_through_market: Decimal = Decimal('0.001')) -> Order: ...
    def who_am_i(self) -> tuple[str, str]: ...
