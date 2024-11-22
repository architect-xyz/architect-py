# Autogenerated from generate_protocol.py

# This file is so that the sync client has good type hinting
# It is not used for anything else
# Ensure that the types in this file are correct for correct type hinting

from types import NoneType
import architect_py.graphql_client
from architect_py.graphql_client import *
from architect_py.async_client import *
from httpx import Response
from dns.name import Name


class AsyncClientProtocol:
    def cancel_all_orders(self: Any, venue: Union[str, NoneType, UnsetType] = UNSET, **kwargs: Any) -> Optional[str]: ...
    def cancel_order(self: Any, order_id: str, **kwargs: Any) -> str: ...
    def cancel_orders(self: Any, order_ids: list[str], **kwargs: Any) -> list[str]: ...
    def configure_marketdata(self: Any, *, cpty: str, url: str) -> Any: ...
    def execute(self: Any, query: str, operation_name: Optional[str] = None, variables: Optional[dict[str, Any]] = None, **kwargs: Any) -> Response: ...
    def execute_ws(self: Any, query: str, operation_name: Optional[str] = None, variables: Optional[dict[str, Any]] = None, **kwargs: Any) -> AsyncIterator: ...
    def fills_subscription(self: Any, **kwargs: Any) -> AsyncIterator: ...
    def find_markets(self: Any, base: str, venue: str, route: str = 'DIRECT') -> list[str]: ...
    def get_account_summaries(self: Any, **kwargs: Any) -> list[GetAccountSummariesAccountSummaries]: ...
    def get_account_summaries_for_cpty(self: Any, venue: str, route: str, **kwargs: Any) -> GetAccountSummariesForCptyAccountSummariesForCpty: ...
    def get_accounts(self: Any, **kwargs: Any) -> list[GetAccountsAccounts]: ...
    def get_algo_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetAlgoOrderAlgoOrder]: ...
    def get_algo_status(self: Any, order_id: str, **kwargs: Any) -> list[GetAlgoStatusAlgoStatus]: ...
    def get_all_market_snapshots(self: Any, **kwargs: Any) -> list[GetAllMarketSnapshotsMarketsSnapshots]: ...
    def get_all_open_orders(self: Any, **kwargs: Any) -> list[GetAllOpenOrdersOpenOrders]: ...
    def get_balances_and_positions(self: Any) -> list[BalancesAndPositions]: ...
    def get_balances_for_cpty(self: Any, venue: str, route: str, **kwargs: Any) -> GetBalancesForCptyAccountSummariesForCpty: ...
    def get_book_snapshot(self: Any, market: str, num_levels: int, precision: Union[Decimal, NoneType, UnsetType] = UNSET, retain_seconds: Union[int, NoneType, UnsetType] = UNSET, **kwargs: Any) -> GetBookSnapshotBookSnapshot: ...
    def get_cme_first_notice_date(self: Any, market: str) -> Optional[date]: ...
    def get_cme_future_from_root_month_year(self: Any, root: str, month: int, year: int) -> SearchMarketsFilterMarkets: ...
    def get_cme_futures_series(self: Any, series: str) -> list[tuple[date, SearchMarketsFilterMarkets]]: ...
    def get_data(self: Any, response: Response) -> dict[str, Any]: ...
    def get_fills(self: Any, venue: Union[str, NoneType, UnsetType] = UNSET, route: Union[str, NoneType, UnsetType] = UNSET, base: Union[str, NoneType, UnsetType] = UNSET, quote: Union[str, NoneType, UnsetType] = UNSET, **kwargs: Any) -> GetFillsFills: ...
    def get_filtered_markets(self: Any, venue: Union[str, NoneType, UnsetType] = UNSET, base: Union[str, NoneType, UnsetType] = UNSET, quote: Union[str, NoneType, UnsetType] = UNSET, underlying: Union[str, NoneType, UnsetType] = UNSET, max_results: Union[int, NoneType, UnsetType] = UNSET, results_offset: Union[int, NoneType, UnsetType] = UNSET, search_string: Union[str, NoneType, UnsetType] = UNSET, only_favorites: Union[bool, NoneType, UnsetType] = UNSET, sort_by_volume_desc: Union[bool, NoneType, UnsetType] = UNSET, **kwargs: Any) -> list[GetFilteredMarketsFilterMarkets]: ...
    def get_first_notice_date(self: Any, id: str, **kwargs: Any) -> Optional[GetFirstNoticeDateMarket]: ...
    def get_l2_book_snapshot(self: Any, market: str) -> L2BookSnapshot: ...
    def get_l3_book_snapshot(self: Any, market: str) -> L3BookSnapshot: ...
    def get_market(self: Any, id: str, **kwargs: Any) -> Optional[GetMarketMarket]: ...
    def get_market_snapshot(self: Any, id: str, **kwargs: Any) -> Optional[GetMarketSnapshotMarketSnapshot]: ...
    def get_markets(self: Any, ids: list[str], **kwargs: Any) -> list[Optional[GetMarketsMarkets]]: ...
    def get_mm_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetMmOrderMmAlgoOrder]: ...
    def get_mm_status(self: Any, order_id: str, **kwargs: Any) -> list[GetMmStatusMmAlgoStatus]: ...
    def get_open_orders(self: Any, venue: Optional[str] = None, route: Optional[str] = None, cpty: Optional[str] = None) -> Any: ...
    def get_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetOrderOrder]: ...
    def get_out_orders(self: Any, from_inclusive: datetime, to_exclusive: datetime, **kwargs: Any) -> list[GetOutOrdersOutedOrders]: ...
    def get_pov_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetPovOrderPovOrder]: ...
    def get_pov_status(self: Any, order_id: str, **kwargs: Any) -> list[GetPovStatusPovStatus]: ...
    def get_smart_order_router_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetSmartOrderRouterOrderSmartOrderRouterOrder]: ...
    def get_smart_order_router_status(self: Any, order_id: str, **kwargs: Any) -> list[GetSmartOrderRouterStatusSmartOrderRouterStatus]: ...
    def get_spread_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetSpreadOrderSpreadAlgoOrder]: ...
    def get_spread_status(self: Any, order_id: str, **kwargs: Any) -> list[GetSpreadStatusSpreadAlgoStatus]: ...
    def get_twap_order(self: Any, order_id: str, **kwargs: Any) -> Optional[GetTwapOrderTwapOrder]: ...
    def get_twap_status(self: Any, order_id: str, **kwargs: Any) -> list[GetTwapStatusTwapStatus]: ...
    def grpc_channel(self: Any, endpoint: Union[Name, str]) -> Any: ...
    def load_and_index_symbology(self: Any, cpty: Optional[str] = None) -> Any: ...
    def preview_smart_order_router(self: Any, *, markets: list[str], base: str, quote: str, odir: OrderDir, limit_price: Decimal, target_size: Decimal, execution_time_limit_ms: int) -> Optional[Sequence]: ...
    def preview_smart_order_router_algo_request(self: Any, algo: CreateSmartOrderRouterAlgo, **kwargs: Any) -> Optional[PreviewSmartOrderRouterAlgoRequestPreviewSmartOrderRouterAlgo]: ...
    def remove_telegram_api_keys(self: Any, **kwargs: Any) -> bool: ...
    def search_markets(self: Any, venue: str | None | architect_py.graphql_client.base_model.UnsetType = UNSET, base: str | None | architect_py.graphql_client.base_model.UnsetType = UNSET, quote: str | None | architect_py.graphql_client.base_model.UnsetType = UNSET, underlying: str | None | architect_py.graphql_client.base_model.UnsetType = UNSET, max_results: int | None | architect_py.graphql_client.base_model.UnsetType = UNSET, results_offset: int | None | architect_py.graphql_client.base_model.UnsetType = UNSET, search_string: str | None | architect_py.graphql_client.base_model.UnsetType = UNSET, only_favorites: bool | None | architect_py.graphql_client.base_model.UnsetType = UNSET, sort_by_volume_desc: bool | None | architect_py.graphql_client.base_model.UnsetType = UNSET, glob: str | None = None, regex: str | None = None, **kwargs: Any) -> list[SearchMarketsFilterMarkets]: ...
    def send_limit_order(self: Any, *, market: str, odir: OrderDir, quantity: Decimal, limit_price: Decimal, order_type: CreateOrderType = CreateOrderType.LIMIT, post_only: bool = False, trigger_price: Optional[Decimal] = None, time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC, good_til_date: Optional[datetime] = None, price_round_method: Optional[TickRoundMethod] = None, account: Optional[str] = None, quote_id: Optional[str] = None, source: OrderSource = OrderSource.API, wait_for_confirm: bool = False) -> Optional[GetOrderOrder]: ...
    def send_market_pro_order(self: Any, *, market: str, odir: OrderDir, quantity: Decimal, time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.DAY, account: Optional[str] = None, source: OrderSource = OrderSource.API, percent_through_market: Decimal = Decimal(0.0200000000000000004163336342344337026588618755340576171875)) -> Optional[GetOrderOrder]: ...
    def send_mm_algo(self: Any, *, name: str, market: str, account: Optional[str] = None, buy_quantity: Decimal, sell_quantity: Decimal, min_position: Decimal, max_position: Decimal, max_improve_bbo: Decimal, position_tilt: Decimal, reference_price: ReferencePrice, ref_dist_frac: Decimal, tolerance_frac: Decimal, fill_lockout_ms: int, order_lockout_ms: int, reject_lockout_ms: int) -> Any: ...
    def send_mm_algo_request(self: Any, algo: CreateMMAlgo, **kwargs: Any) -> str: ...
    def send_order(self: Any, order: CreateOrder, **kwargs: Any) -> str: ...
    def send_orders(self: Any, orders: list[CreateOrder], **kwargs: Any) -> list[str]: ...
    def send_pov_algo(self: Any, *, name: str, market: str, odir: OrderDir, target_volume_frac: Decimal, min_order_quantity: Decimal, max_quantity: Decimal, order_lockout_ms: int, end_time: datetime, account: Optional[str] = None, take_through_frac: Optional[Decimal] = None) -> str: ...
    def send_pov_algo_request(self: Any, algo: CreatePovAlgo, **kwargs: Any) -> str: ...
    def send_smart_order_router_algo(self: Any, *, markets: list[str], base: str, quote: str, odir: OrderDir, limit_price: Decimal, target_size: Decimal, execution_time_limit_ms: int) -> str: ...
    def send_smart_order_router_algo_request(self: Any, algo: CreateSmartOrderRouterAlgo, **kwargs: Any) -> str: ...
    def send_spread_algo(self: Any, *, name: str, market: str, buy_quantity: Decimal, sell_quantity: Decimal, min_position: Decimal, max_position: Decimal, max_improve_bbo: Decimal, position_tilt: Decimal, reference_price: ReferencePrice, ref_dist_frac: Decimal, tolerance_frac: Decimal, hedge_market: CreateSpreadAlgoHedgeMarket, fill_lockout_ms: int, order_lockout_ms: int, reject_lockout_ms: int, account: Optional[str] = None) -> str: ...
    def send_spread_algo_request(self: Any, algo: CreateSpreadAlgo, **kwargs: Any) -> str: ...
    def send_twap_algo(self: Any, *, name: str, market: str, odir: OrderDir, quantity: Decimal, interval_ms: int, reject_lockout_ms: int, end_time: datetime, account: Optional[str] = None, take_through_frac: Optional[Decimal] = None) -> str: ...
    def send_twap_algo_request(self: Any, algo: CreateTwapAlgo, **kwargs: Any) -> str: ...
    def start_session(self: Any) -> Any: ...
