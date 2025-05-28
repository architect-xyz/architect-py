# fmt: off
# mypy: ignore-errors
# ruff: noqa
from architect_py.grpc.models import *
import asyncio
import pandas as pd
from architect_py.common_types import OrderDir as OrderDir, TimeInForce as TimeInForce, TradableProduct as TradableProduct, Venue as Venue
from architect_py.graphql_client import GraphQLClient as GraphQLClient
from architect_py.graphql_client.exceptions import GraphQLClientGraphQLMultiError as GraphQLClientGraphQLMultiError
from architect_py.graphql_client.fragments import ExecutionInfoFields as ExecutionInfoFields, ProductInfoFields as ProductInfoFields
from architect_py.grpc.client import GrpcClient as GrpcClient
from architect_py.grpc.models.Orderflow.OrderflowRequest import OrderflowRequestUnannotatedResponseType as OrderflowRequestUnannotatedResponseType, OrderflowRequest_route as OrderflowRequest_route
from architect_py.grpc.models.definitions import AccountIdOrName as AccountIdOrName, AccountWithPermissions as AccountWithPermissions, CandleWidth as CandleWidth, L2BookDiff as L2BookDiff, OrderId as OrderId, OrderSource as OrderSource, OrderType as OrderType, SortTickersBy as SortTickersBy, TraderIdOrEmail as TraderIdOrEmail
from architect_py.grpc.resolve_endpoint import resolve_endpoint as resolve_endpoint
from architect_py.utils.nearest_tick import TickRoundMethod as TickRoundMethod
from architect_py.utils.orderbook import update_orderbook_side as update_orderbook_side
from architect_py.utils.pandas import candles_to_dataframe as candles_to_dataframe
from architect_py.utils.price_bands import price_band_pairs as price_band_pairs
from architect_py.utils.symbol_parsing import nominative_expiration as nominative_expiration
from datetime import date, datetime
from decimal import Decimal
from typing import Any, AsyncGenerator, AsyncIterator, Literal, Sequence, overload

class Client:
    """
    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    This Client takes control of the event loop, which you can pass in.

    One can find the function definition in the AsyncClient class.

    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.

    Avoid adding functions or other attributes to this class unless you know what you are doing, because
    the __getattribute__ method changes the behavior of the class in a way that is not intuitive.

    Instead, add them to the AsyncClient class.
    """
    api_key: str | None
    api_secret: str | None
    paper_trading: bool
    graphql_client: GraphQLClient
    grpc_core: GrpcClient | None
    grpc_marketdata: dict[Venue, GrpcClient]
    grpc_hmart: GrpcClient | None
    jwt: str | None
    jwt_expiration: datetime | None
    l1_books: dict[Venue, dict[TradableProduct, tuple[L1BookSnapshot, asyncio.Task]]]
    def __init__(self, *, api_key: str, api_secret: str, paper_trading: bool, endpoint: str = 'https://app.architect.co', graphql_port: int | None = None, event_loop: asyncio.events.AbstractEventLoop | None = None) -> None:
        """
        Create a new Client instance.

        An `api_key` and `api_secret` can be created at https://app.architect.co/api-keys

        Pass in an `event_loop` if you want to use your own; otherwise, this class
        will use the default asyncio event loop.
        """
    l2_books: dict[Venue, dict[TradableProduct, tuple[L2BookSnapshot, asyncio.Task]]]
    def refresh_jwt(self, force: bool = False):
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force=True, refresh the JWT unconditionally.

        Query methods on Client that require auth will call this method internally.
        """
    def set_jwt(self, jwt: str | None, jwt_expiration: datetime | None = None):
        """
        Manually set the JWT for gRPC authentication.

        Args:
            jwt: the JWT to set;
                None to clear the JWT
            jwt_expiration: when to expire the JWT
        """
    def discover_marketdata(self) -> None:
        """
        Load marketdata endpoints from the server config.

        The Architect core is responsible for telling you where to find marketdata as per
        its configuration.  You can also manually set marketdata endpoints by calling
        set_marketdata directly.

        This method is called on Client.connect.
        """
    def set_marketdata(self, venue: Venue, endpoint: str):
        """
        Manually set the marketdata endpoint for a venue.
        """
    def marketdata(self, venue: Venue) -> GrpcClient:
        """
        Get the marketdata client for a venue.
        """
    def set_hmart(self, endpoint: str):
        """
        Manually set the hmart (historical marketdata service) endpoint.
        """
    def hmart(self) -> GrpcClient:
        """
        Get the hmart (historical marketdata service) client.
        """
    def core(self) -> GrpcClient:
        """
        Get the core client.
        """
    def who_am_i(self) -> tuple[str, str]:
        """
        Gets the user_id and user_email for the user that the API key belongs to.

        Returns:
            (user_id, user_email)
        """
    def list_symbols(self, *, marketdata: Venue | None = None) -> list[str]:
        """
        List all symbols.

        Args:
            marketdata: query marketdata endpoint for the specified venue directly;
                If provided, query the venue's marketdata endpoint directly,
                instead of the Architect core.  This is sometimes useful for
                cross-referencing symbols or checking availability.
        """
    def search_symbols(self, search_string: str | None = None, execution_venue: str | None = None, offset: int = 0, limit: int = 20) -> list[TradableProduct]:
        '''
        Search for tradable products on Architect.

        Args:
            search_string: a string to search for in the symbol
                Can be "*" for wild card search.
                Examples: "ES", "NQ", "GC"
            execution_venue: the execution venue to search in
                Examples: "CME"
        '''
    def get_product_info(self, symbol: str) -> ProductInfoFields | None:
        '''
        Get information about a product, e.g. product_type, underlying, multiplier.

        Args:
            symbol: the symbol to get information for
                the symbol should *not* have a quote,
                ie "ES 20250620 CME Future" instead of "ES 20250620 CME Future/USD"

                If you used TradableProduct, you can use the base() method to get the symbol

        Returns:
            None if the symbol does not exist
        '''
    def get_product_infos(self, symbols: list[str] | None) -> Sequence[ProductInfoFields]:
        """
        Get information about products, e.g. product_type, underlying, multiplier.

        Args:
            symbols: the symbols to get information for, or None for all symbols

        Returns:
            Product infos for each symbol.  Not guaranteed to contain all symbols
            that were asked for, or in the same order; any duplicates or invalid
            symbols will be ignored.
        """
    def get_execution_info(self, symbol: TradableProduct | str, execution_venue: str) -> ExecutionInfoFields | None:
        '''
        Get information about tradable product execution, e.g. tick_size,
        step_size, margins.

        Args:
            symbol: the symbol to get execution information for
            execution_venue: the execution venue e.g. "CME"

        Returns:
            None if the symbol doesn\'t exist
        '''
    def get_execution_infos(self, symbols: list[TradableProduct | str] | None, execution_venue: str | None = None) -> Sequence[ExecutionInfoFields]:
        '''
        Get information about tradable product execution, e.g. tick_size,
        step_size, margins, for many symbols.

        Args:
            symbols: the symbols to get execution information for, or None for all symbols
            execution_venue: the execution venue e.g. "CME"

        Returns:
            Execution infos for each symbol.  Not guaranteed to contain all symbols
            that were asked for, or in the same order; any duplicates or invalid
            symbols will be ignored.
        '''
    def get_cme_first_notice_date(self, symbol: str) -> date | None:
        '''
        @deprecated(reason="Use get_product_info instead; first_notice_date is now a field")

        Get the first notice date for a CME future.

        Args:
            symbol: the symbol to get the first notice date for a CME future

        Returns:
            The first notice date as a date object if it exists
        '''
    def get_future_series(self, series_symbol: str) -> list[str]:
        '''
        @deprecated(reason="Use get_futures_series instead")
        '''
    def get_futures_series(self, series_symbol: str) -> list[str]:
        '''
        List all futures in a given series.

        Args:
            series_symbol: the futures series
                e.g. "ES CME Futures" would yield a list of all the ES futures
        Returns:
            List of futures products
        '''
    def get_front_future(self, series_symbol: str, venue: str, by_volume: bool = True) -> str:
        '''
        Gets the future with the most volume in a series.

        Args:
            series_symbol: the futures series
                e.g. "ES CME Futures" would yield the lead future for the ES series
            venue: the venue to get the lead future for, e.g. "CME"
            by_volume: if True, sort by volume; otherwise sort by expiration date

        Returns:
            The lead future symbol
        '''
    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date | None:
        '''
        @deprecated(reason="Use utils.symbol_parsing.nominative_expiration instead")

        Get the expiration date from a CME future name.

        Args:
            name: the CME future name
                e.g. "ES 20211217 CME Future" -> date(2021, 12, 17)
        Returns:
            the expiration date as a date object
        '''
    def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]:
        '''
        @deprecated(reason="Use get_futures_series instead")

        List all futures in a given CME series.

        Args:
            series: the series to get the futures for
                e.g. "ES CME Futures"
        Returns:
            a list of tuples of the expiration date and
            the symbol for each future in the series

            e.g.
            ```
            [
                (datetime.date(2025, 3, 21), \'ES 20250321 CME Future\'),
                (datetime.date(2025, 6, 20), \'ES 20250620 CME Future\'),
                (datetime.date(2025, 9, 19), \'ES 20250919 CME Future\'),
                # ...
            ]
            ```
        '''
    def get_cme_future_from_root_month_year(self, root: str, month: int, year: int) -> str:
        '''
        Get the symbol for a CME future from the root, month, and year.
        This is a simple wrapper around search_symbols.

        Args:
            root: the root symbol for the future e.g. "ES"
            month: the month of the future
            year: the year of the future
        Returns:
            The future symbol if it exists and is unique.
        '''
    def get_market_status(self, symbol: TradableProduct | str, venue: Venue) -> MarketStatus:
        '''
        Returns market status for symbol (e.g. if it\'s currently quoting or trading).

        Args:
            symbol: the symbol to get the market status for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        '''
    def get_market_snapshot(self, symbol: TradableProduct | str, venue: Venue) -> L1BookSnapshot:
        '''
        @deprecated(reason="Use get_l1_snapshot instead")

        This is an alias for l1_book_snapshot.

        Args:
            symbol: the symbol to get the market snapshot for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        Returns:
            L1BookSnapshot for the symbol
        '''
    def get_market_snapshots(self, symbols: list[TradableProduct | str], venue: Venue) -> Sequence[L1BookSnapshot]:
        '''
        @deprecated(reason="Use get_l1_snapshots instead")

            This is an alias for l1_book_snapshots.

            Args:
                symbols: the symbols to get the market snapshots for
                venue: the venue that the symbols are traded at
        '''
    @overload
    def get_historical_candles(self, symbol: TradableProduct | str, venue: Venue, candle_width: CandleWidth, start: datetime, end: datetime, *, as_dataframe: Literal[True]) -> pd.DataFrame: ...
    @overload
    def get_historical_candles(self, symbol: TradableProduct | str, venue: Venue, candle_width: CandleWidth, start: datetime, end: datetime) -> list[Candle]: ...
    def get_l1_book_snapshot(self, symbol: TradableProduct | str, venue: Venue) -> L1BookSnapshot:
        """
        Gets the L1 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l1 book snapshot for
            venue: the venue that the symbol is traded at
        """
    def get_l1_book_snapshots(self, symbols: list[TradableProduct | str], venue: Venue) -> Sequence[L1BookSnapshot]:
        """
        Gets the L1 book snapshots for a list of symbols.

        Args:
            symbols: the symbols to get the l1 book snapshots for
            venue: the venue that the symbols are traded at
        """
    def get_l2_book_snapshot(self, symbol: TradableProduct | str, venue: Venue) -> L2BookSnapshot:
        """
        Gets the L2 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l2 book snapshot for
            venue: the venue that the symbol is traded at
        """
    def get_ticker(self, symbol: TradableProduct | str, venue: Venue) -> Ticker:
        """
        Gets the ticker for a symbol.
        """
    def list_accounts(self) -> list[AccountWithPermissions]:
        """
        List accounts for the user that the API key belongs to.

        Returns:
            a list of AccountWithPermissionsFields for the user that the API key belongs to
            a list of AccountWithPermissions for the user that the API key belongs to
            (use who_am_i to get the user_id / email)
        """
    def get_account_summary(self, account: str) -> AccountSummary:
        '''
        Get account summary, including balances, positions, pnls, etc.

        Args:
            account: account uuid or name
                Examples: "00000000-0000-0000-0000-000000000000", "STONEX:000000/JDoe"
        '''
    def get_account_summaries(self, accounts: list[str] | None = None, trader: str | None = None) -> list[AccountSummary]:
        """
        Get account summaries for accounts matching the filters.

        Args:
            accounts: list of account uuids or names
            trader: if specified, return summaries for all accounts for this trader

        If both arguments are given, the union of matching accounts are returned.
        """
    def get_account_history(self, account: str, from_inclusive: datetime | None = None, to_exclusive: datetime | None = None) -> list[AccountSummary]:
        """
        Get historical sequence of account summaries for the given account.
        """
    def get_open_orders(self, order_ids: list[OrderId] | None = None, venue: str | None = None, account: str | None = None, trader: str | None = None, symbol: str | None = None, parent_order_id: OrderId | None = None) -> list[Order]:
        """
        Returns a list of open orders for the user that match the filters.

        Args:
            order_ids: a list of order ids to get
            venue: the venue to get orders for
            account: the account to get orders for
            trader: the trader to get orders for
            symbol: the symbol to get orders for
            parent_order_id: the parent order id to get orders for

        Returns:
            Open orders that match the union of the filters
        """
    def get_all_open_orders(self) -> list[Order]:
        '''
        @deprecated(reason="Use get_open_orders with no parameters instead")

        Returns a list of all open orders for the authenticated user.
        '''
    def get_historical_orders(self, order_ids: list[OrderId] | None = None, from_inclusive: datetime | None = None, to_exclusive: datetime | None = None, venue: str | None = None, account: str | None = None, parent_order_id: OrderId | None = None) -> list[Order]:
        """
        Returns a list of all historical orders that match the filters.

        Historical orders are orders that are not open, having been filled,
        canceled, expired, or outed.

        Args:
            order_ids: a list of order ids to get
            from_inclusive: the start date to get orders for
            to_exclusive: the end date to get orders for
            venue: the venue to get orders for, e.g. CME
            account: account uuid or name
            parent_order_id: the parent order id to get orders for
        Returns:
            Historical orders that match the union of the filters.

        If order_ids is not specified, then from_inclusive and to_exclusive
        MUST be specified.
        """
    def get_order(self, order_id: OrderId) -> Order | None:
        """
        Returns the specified order.  Useful for looking at past sent orders.
        Queries open_orders first, then queries historical_orders.

        Args:
            order_id: the order id to get
        """
    def get_orders(self, order_ids: list[OrderId]) -> list[Order | None]:
        """
        Returns the specified orders.  Useful for looking at past sent orders.
        Plural form of get_order.

        Args:
            order_ids: a list of order ids to get
        """
    def get_fills(self, from_inclusive: datetime | None = None, to_exclusive: datetime | None = None, venue: str | None = None, account: str | None = None, order_id: OrderId | None = None, limit: int | None = None) -> HistoricalFillsResponse:
        '''
        Returns all fills matching the given filters.

        Args:
            from_inclusive: the start date to get fills for
            to_exclusive: the end date to get fills for
            venue: the venue to get fills for, e.g. "CME"
            account: account uuid or name
            order_id: the order id to get fills for
        '''
    def send_limit_order(self, *args, **kwargs) -> Order:
        '''
        @deprecated(reason="Use place_limit_order instead")
        '''
    def place_limit_order(self, *, id: OrderId | None = None, symbol: TradableProduct | str, execution_venue: str | None = None, dir: OrderDir | None = None, quantity: Decimal, limit_price: Decimal, order_type: OrderType = ..., time_in_force: TimeInForce = ..., price_round_method: TickRoundMethod | None = None, account: str | None = None, trader: str | None = None, post_only: bool = False, trigger_price: Decimal | None = None, **kwargs: Any) -> Order:
        '''
        Sends a regular limit order.

        Args:
            id: in case user wants to generate their own order id, otherwise it will be generated automatically
            symbol: the symbol to send the order for
            execution_venue: the execution venue to send the order to,
                if execution_venue is set to None, the OMS will send the order to the primary_exchange
                the primary_exchange can be deduced from `get_product_info`
            dir: the direction of the order, BUY or SELL
            quantity: the quantity of the order
            limit_price: the limit price of the order
                It is highly recommended to make this a Decimal object from the decimal module to avoid floating point errors
            order_type: the type of the order
            time_in_force: the time in force of the order
            price_round_method: the method to round the price to the nearest tick, will not round if None
            account: the account to send the order for
                While technically optional, for most order types, the account is required
            trader: the trader to send the order for, defaults to the user\'s trader
                for when sending order for another user, not relevant for vast majority of users
            post_only: whether the order should be post only, not supported by all exchanges
            trigger_price: the trigger price for the order, only relevant for stop / take_profit orders
        Returns:
            the Order object for the order
            The order.status should  be "PENDING" until the order is "OPEN" / "REJECTED" / "OUT" / "CANCELED" / "STALE"

            If the order is rejected, the order.reject_reason and order.reject_message will be set
        '''
    def send_market_pro_order(self, *, id: OrderId | None = None, symbol: TradableProduct | str, execution_venue: str, odir: OrderDir, quantity: Decimal, time_in_force: TimeInForce = ..., account: str | None = None, fraction_through_market: Decimal = ...) -> Order:
        '''
        Sends a market-order like limit price based on the BBO.
        Meant to behave as a market order but with more protections.

        Args:
            id: in case user wants to generate their own order id, otherwise it will be generated automatically
            symbol: the symbol to send the order for
            execution_venue: the execution venue to send the order to
            odir: the direction of the order
            quantity: the quantity of the order
            time_in_force: the time in force of the order
            account: the account to send the order for
            fraction_through_market: the fraction through the market to send the order at
                e.g. 0.001 would send the order 0.1% through the market
        Returns:
            the OrderFields object for the order
            The order.status should  be "PENDING" until the order is "OPEN" / "REJECTED" / "OUT" / "CANCELED" / "STALE"

            If the order is rejected, the order.reject_reason and order.reject_message will be set
        '''
    def cancel_order(self, order_id: OrderId) -> Cancel:
        """
        Cancels an order by order id.

        Args:
            order_id: the order id to cancel
        Returns:
            the CancelFields object
        """
    def cancel_all_orders(self, account: AccountIdOrName | None = None, execution_venue: str | None = None, trader: TraderIdOrEmail | None = None) -> bool:
        """
        Cancels all open orders.

        Returns:
            True if all orders were cancelled successfully
            False if there was an error
        """
