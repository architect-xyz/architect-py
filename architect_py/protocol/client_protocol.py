# fmt: off

# mypy: ignore-errors

# Autogenerated from generate_protocol.py

# If you are here for function definitions, please refer to architect_py/async_cline.py
# This file is so that the sync client has good type hinting
# It is not used for anything else
# For maintainers: ensure that the types in this file are correct for correct type hinting


import architect_py.graphql_client
from typing import Union
from architect_py.graphql_client import *
from architect_py.async_client import *
from httpx import Response


class AsyncClientProtocol:
    def cancel_all_orders(self: Any, **kwargs: Any) -> CancelAllOrdersOms: ...
    def cancel_order(self: Any, order_id: str, **kwargs: Any) -> CancelOrderOms: ...
    def configure_marketdata(self: Any, *, cpty: str, url: str) -> Any: ...
    def create_jwt(self: Any, **kwargs: Any) -> CreateJwtUser: ...
    def execute(self: Any, query: str, operation_name: Optional[str] = None, variables: Optional[dict[str, Any]] = None, **kwargs: Any) -> Response: ...
    def execute_ws(self: Any, query: str, operation_name: Optional[str] = None, variables: Optional[dict[str, Any]] = None, **kwargs: Any) -> AsyncIterator: ...
    def get_account_summaries(self: Any, account: list[str], venue: Optional[str] = None, trader: Optional[str] = None) -> Sequence: ...
    def get_account_summaries_query(self: Any, venue: Union[str, None, UnsetType] = UNSET, trader: Union[str, None, UnsetType] = UNSET, accounts: Union[list[str], None, UnsetType] = UNSET, **kwargs: Any) -> GetAccountSummariesQueryFolio: ...
    def get_account_summary(self: Any, account: str, venue: Optional[str] = None) -> AccountSummaryFields: ...
    def get_account_summary_query(self: Any, account: str, venue: Union[str, None, UnsetType] = UNSET, **kwargs: Any) -> GetAccountSummaryQueryFolio: ...
    def get_all_open_orders(self: Any) -> Sequence: ...
    def get_all_open_orders_query(self: Any, **kwargs: Any) -> GetAllOpenOrdersQueryOms: ...
    def get_cme_first_notice_date(self: Any, symbol: str) -> Optional[date]: ...
    def get_cme_future_from_root_month_year(self: Any, root: str, month: int, year: int) -> str: ...
    def get_cme_futures_series(self: Any, series: str) -> list[tuple[date, str]]: ...
    def get_data(self: Any, response: Response) -> dict[str, Any]: ...
    def get_execution_info(self: Any, symbol: str, execution_venue: Optional[str] = None) -> ExecutionInfoFields: ...
    def get_execution_info_query(self: Any, symbol: str, execution_venue: Union[str, None, UnsetType] = UNSET, **kwargs: Any) -> GetExecutionInfoQuerySymbology: ...
    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date: ...
    def get_external_l2_book_snapshot(self: Any, market: str) -> ExternalL2BookSnapshot: ...
    def get_fills(self: Any, venue: Optional[str], account: Optional[str], order_id: Optional[str], from_inclusive: Optional[datetime], to_exclusive: Optional[datetime]) -> GetFillsQueryFolioHistoricalFills: ...
    def get_fills_query(self: Any, venue: Union[str, None, UnsetType] = UNSET, account: Union[str, None, UnsetType] = UNSET, order_id: Union[str, None, UnsetType] = UNSET, from_inclusive: Union[datetime, None, UnsetType] = UNSET, to_exclusive: Union[datetime, None, UnsetType] = UNSET, **kwargs: Any) -> GetFillsQueryFolio: ...
    def get_first_notice_date_query(self: Any, symbol: str, **kwargs: Any) -> GetFirstNoticeDateQuerySymbology: ...
    def get_future_series(self: Any, series_symbol: str) -> list[str]: ...
    def get_future_series_query(self: Any, series_symbol: str, **kwargs: Any) -> GetFutureSeriesQuerySymbology: ...
    def get_historical_orders(self: Any, from_inclusive: datetime, to_exclusive: datetime, venue: Optional[str] = None, account: Optional[str] = None, parent_order_id: Optional[str] = None) -> Sequence: ...
    def get_historical_orders_query(self: Any, from_inclusive: datetime, to_exclusive: datetime, venue: Union[str, None, UnsetType] = UNSET, account: Union[str, None, UnsetType] = UNSET, parent_order_id: Union[str, None, UnsetType] = UNSET, **kwargs: Any) -> GetHistoricalOrdersQueryFolio: ...
    def get_l3_book_snapshot(self: Any, market: str) -> L3BookSnapshot: ...
    def get_l_2_book_snapshot_query(self: Any, venue: str, symbol: str, **kwargs: Any) -> GetL2BookSnapshotQueryMarketdata: ...
    def get_market_snapshot_query(self: Any, venue: str, symbol: str, **kwargs: Any) -> GetMarketSnapshotQueryMarketdata: ...
    def get_market_snapshots(self: Any, venue: str, symbols: list[str]) -> Sequence: ...
    def get_market_snapshots_query(self: Any, venue: str, symbols: Union[list[str], None, UnsetType] = UNSET, **kwargs: Any) -> GetMarketSnapshotsQueryMarketdata: ...
    def get_open_orders(self: Any, venue: Optional[str], account: Optional[str], trader: Optional[str], symbol: Optional[str], parent_order_id: Optional[str], order_ids: list[str]) -> Sequence: ...
    def get_open_orders_query(self: Any, venue: Union[str, None, UnsetType] = UNSET, account: Union[str, None, UnsetType] = UNSET, trader: Union[str, None, UnsetType] = UNSET, symbol: Union[str, None, UnsetType] = UNSET, parent_order_id: Union[str, None, UnsetType] = UNSET, order_ids: Union[list[str], None, UnsetType] = UNSET, **kwargs: Any) -> GetOpenOrdersQueryOms: ...
    def get_primary_execution_venue(self: Any, symbol: str) -> str: ...
    def get_primary_execution_venue_query(self: Any, symbol: str, **kwargs: Any) -> GetPrimaryExecutionVenueQuerySymbology: ...
    def get_product_info(self: Any, symbol: str) -> Optional[ProductInfoFields]: ...
    def get_product_info_query(self: Any, symbol: str, **kwargs: Any) -> GetProductInfoQuerySymbology: ...
    def get_product_infos(self: Any, symbols: list[str]) -> Sequence: ...
    def get_product_infos_query(self: Any, symbols: list[str], **kwargs: Any) -> GetProductInfosQuerySymbology: ...
    def grpc_channel(self: Any, endpoint: str) -> Any: ...
    def l1_book_snapshot(self: Any, venue: str, symbol: str) -> MarketTickerFields: ...
    def l2_book_snapshot(self: Any, venue: str, symbol: str) -> L2BookFields: ...
    def market_snapshot(self: Any, venue: str, symbol: str) -> MarketTickerFields: ...
    def place_order(self: Any, symbol: str, dir: OrderDir, quantity: Decimal, order_type: OrderType, time_in_force: TimeInForce, id: Union[str, None, UnsetType] = UNSET, trader: Union[str, None, UnsetType] = UNSET, account: Union[str, None, UnsetType] = UNSET, limit_price: Union[Decimal, None, UnsetType] = UNSET, post_only: Union[bool, None, UnsetType] = UNSET, trigger_price: Union[Decimal, None, UnsetType] = UNSET, good_til_date: Union[datetime, None, UnsetType] = UNSET, execution_venue: Union[str, None, UnsetType] = UNSET, **kwargs: Any) -> PlaceOrderOms: ...
    def refresh_grpc_credentials(self: Any, force: bool = False) -> Optional[str]: ...
    def search_symbols(self: Any, *, search_string: Optional[str] = None, glob: Optional[str] = None, regex: Optional[str] = None, underlying: Optional[str] = None, execution_venue: Optional[str] = None, sort_by_volume_desc_given_execution_venue: bool = False, max_results: Optional[int] = None) -> list[str]: ...
    def search_symbols_query(self: Any, sort_by_volume_desc_given_execution_venue: bool, search_string: Union[str, None, UnsetType] = UNSET, underlying: Union[str, None, UnsetType] = UNSET, execution_venue: Union[str, None, UnsetType] = UNSET, max_results: Union[int, None, UnsetType] = UNSET, **kwargs: Any) -> SearchSymbolsQuerySymbology: ...
    def send_limit_order(self: Any, *, symbol: str, odir: OrderDir, quantity: Decimal, limit_price: Decimal, order_type: OrderType = OrderType.LIMIT, execution_venue: Optional[str] = None, time_in_force: TimeInForce = TimeInForce.DAY, good_til_date: Optional[datetime] = None, price_round_method: Optional[TickRoundMethod] = None, account: Optional[str] = None, trader: Optional[str] = None, post_only: bool = False, trigger_price: Optional[Decimal] = None) -> OrderFields: ...
    def send_market_pro_order(self: Any, *, symbol: str, execution_venue: Optional[str] = None, odir: OrderDir, quantity: Decimal, time_in_force: TimeInForce = TimeInForce.DAY, account: Optional[str] = None, fraction_through_market: Decimal = Decimal('0.001')) -> OrderFields: ...
    def watch_l2_book(self: Any, endpoint: str, venue: Optional[str], symbol: str) -> AsyncIterator: ...
