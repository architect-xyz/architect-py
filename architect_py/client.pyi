# fmt: off
# mypy: ignore-errors
# ruff: noqa
from architect_py.grpc.models import *
import asyncio
import pandas as pd
from architect_py.batch_place_order import BatchPlaceOrder as BatchPlaceOrder
from architect_py.common_types import OrderDir as OrderDir, TimeInForce as TimeInForce, TradableProduct as TradableProduct, Venue as Venue
from architect_py.graphql_client import GraphQLClient as GraphQLClient
from architect_py.graphql_client.exceptions import GraphQLClientGraphQLMultiError as GraphQLClientGraphQLMultiError
from architect_py.graphql_client.fragments import ExecutionInfoFields as ExecutionInfoFields, ProductInfoFields as ProductInfoFields
from architect_py.grpc.client import GrpcClient as GrpcClient
from architect_py.grpc.models.definitions import AccountIdOrName as AccountIdOrName, AccountWithPermissions as AccountWithPermissions, CandleWidth as CandleWidth, L2BookDiff as L2BookDiff, OrderId as OrderId, OrderSource as OrderSource, OrderType as OrderType, SortTickersBy as SortTickersBy, SpreaderParams as SpreaderParams, TraderIdOrEmail as TraderIdOrEmail, TriggerLimitOrderType as TriggerLimitOrderType
from architect_py.grpc.orderflow import OrderflowChannel as OrderflowChannel
from architect_py.grpc.resolve_endpoint import PAPER_GRPC_PORT as PAPER_GRPC_PORT, resolve_endpoint as resolve_endpoint
from architect_py.utils.nearest_tick import TickRoundMethod as TickRoundMethod
from architect_py.utils.orderbook import update_orderbook_side as update_orderbook_side
from architect_py.utils.pandas import candles_to_dataframe as candles_to_dataframe, tickers_to_dataframe as tickers_to_dataframe
from architect_py.utils.price_bands import price_band_pairs as price_band_pairs
from architect_py.utils.symbol_parsing import nominative_expiration as nominative_expiration
from datetime import date, datetime
from decimal import Decimal
from typing import Any, AsyncGenerator, Literal, Sequence, overload

class Client:
    """
    One can find the function definition in the AsyncClient class and in the pyi file.

    This class is a wrapper around the AsyncClient class that allows you to call async methods synchronously.
    This does not work for subscription based methods.

    This Client takes control of the event loop, which you can pass in.


    The AsyncClient is more performant and powerful, so it is recommended to use that class if possible.
    Avoid adding functions or other attributes to this class unless you know what you are doing.
    """
    api_key: str | None
    api_secret: str | None
    paper_trading: bool
    as_user: str | None
    as_role: str | None
    graphql_client: GraphQLClient
    grpc_options: Sequence[tuple[str, Any]] | None
    grpc_core: GrpcClient | None
    grpc_marketdata: dict[Venue, GrpcClient]
    grpc_hmart: GrpcClient | None
    jwt: str | None
    jwt_expiration: datetime | None
    l1_books: dict[Venue, dict[TradableProduct, tuple[L1BookSnapshot, asyncio.Task]]]
    def __init__(self, *, api_key: str, api_secret: str, paper_trading: bool, as_user: str | None = None, as_role: str | None = None, endpoint: str = 'https://app.architect.co', graphql_port: int | None = None, grpc_options: Sequence[tuple[str, Any]] | None = None, event_loop: asyncio.events.AbstractEventLoop | None = None) -> None:
        """
        Create a new Client instance.

        An `api_key` and `api_secret` can be created at https://app.architect.co/api-keys

        Pass in an `event_loop` if you want to use your own; otherwise, this class
        will use the default asyncio event loop.
        """
    l2_books: dict[Venue, dict[TradableProduct, tuple[L2BookSnapshot, asyncio.Task]]]
    def close(self) -> None:
        """
        Close the gRPC channel and GraphQL client.

        This fixes the:
        Error in sys.excepthook:

        Original exception was:

        One might get when closing the client
        """
    def refresh_jwt(self, force: bool = False):
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force=True, refresh the JWT unconditionally.

        Query methods on Client that require auth will call this method internally.
        """
    def set_marketdata(self, venue: Venue, endpoint: str):
        """
        Manually set the marketdata endpoint for a venue.
        """
    def set_hmart(self, endpoint: str):
        """
        Manually set the hmart (historical marketdata service) endpoint.
        """
    def who_am_i(self) -> tuple[str, str]:
        """
        Gets the user_id and user_email for the user that the API key belongs to.

        Returns:
            (user_id, user_email)
        """
    def cpty_status(self, kind: str, instance: str | None = None) -> CptyStatus:
        """
        Get cpty status.
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
    def search_symbols(self, search_string: str | None = None, execution_venue: str | None = None, include_expired: bool = False, sort_alphabetically: bool = True, offset: int = 0, limit: int = 20) -> list[TradableProduct]:
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
    def get_front_future(self, series_symbol: str, venue: str | None = None) -> TradableProduct:
        '''
        Gets the front future.
        ** If the venue is provided, it will return the future with the most volume in that venue**
        Otherwise, will sort by expiration date and return the earliest future.

        ** Note that this function returns a TradableProduct (ie with a base and a quote)


        Args:
            series_symbol: the futures series
                e.g. "ES CME Futures" would yield the lead future for the ES series
            venue: the venue to get the lead future for, e.g. "CME"
                ** If the venue is provided, it will return the future with the most volume in that venue**

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
    def get_tickers(self, *, venue: Venue, symbols: Sequence[TradableProduct | str] | None = None, include_options: bool = False, sort_by: SortTickersBy | str | None = None, offset: int | None = None, limit: int | None = None, as_dataframe: bool = False) -> Sequence[Ticker] | pd.DataFrame:
        """
        Gets the tickers for a list of symbols.
        """
    def get_options_chain(self, *, expiration: date, underlying: str, wrap: str | None = None, venue: str) -> OptionsChain:
        '''
        Get the options chain for a symbol.

        Args:
            expiration: the expiration date of the options chain
            underlying: the underlying symbol for the options chain
            wrap: the disambiguation for underlyings with multiple chains, see method `get_options_wraps`
            venue: the venue to get the options chain from, e.g. "CME", "US-EQUITIES"

        Returns:
            A list of Option objects for the symbol.
        '''
    @staticmethod
    def get_option_symbol(options_contract: OptionsContract) -> TradableProduct:
        '''
        Get the tradable product symbol for an options contract.
        Users can get the OptionsContract from the method `get_options_chain`

        Args:
            options_contract: the options contract to get the symbol for

        Returns:
            The tradable product symbol for the options contract.
            e.g. "AAPL US 20250718 200.00 P Option/USD"
        '''
    def get_options_expirations(self, *, underlying: str, wrap: str | None = None, venue: str) -> OptionsExpirations:
        '''
        Get the available expirations for a symbol\'s options chain.

        Args:
            symbol: the underlying symbol for the options chain, e.g. "TSLA US Equity"
            wrap: the disambiguation for underlyings with multiple chains, see method `get_options_wraps`
            venue: the venue to get the options expirations from, e.g. "CME", "US-EQUITIES"
        '''
    def get_options_wraps(self, *, underlying: str, venue: str) -> OptionsWraps:
        '''
        Get the available wraps for a symbol\'s options chain.
        For disambiguation of underlyings with multiple chains.

        Args:
            underlying: the underlying symbol for the options chain
                e.g. "TSLA US Equity"
            venue: the venue to get the options wraps from, e.g. "CME", "US-EQUITIES"

        Returns:
            A list of wraps for the options chain.
            e.g. "TSLA US Equity" might yield wraps=["1TSLA", "2TSLA", "TSLA"]
        '''
    def get_options_contract_greeks(self, *, contract: str, venue: str) -> OptionsGreeks:
        '''
        Get the greeks for a specific options contract.

        Args:
            contract: the specific options contract to get the greeks for, e.g. "AAPL US 20250718 200.00 P Option/USD"
            venue: the venue to get the options greeks from, e.g. "CME", "US-EQUITIES"
        '''
    def get_options_chain_greeks(self, *, expiration: date, underlying: str, wrap: str | None = None, venue: str) -> OptionsChainGreeks:
        """
        Get the greeks for the options chain of a specific underlying.
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
    def get_positions(self, accounts: list[str] | None = None, trader: str | None = None) -> dict[str, Decimal]:
        """
        Get positions for the specified symbols.

        Args:
            symbols: list of symbol strings
        """
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
    def get_open_orders(self, order_ids: list[OrderId] | None = None, venue: str | None = None, account: str | None = None, trader: str | None = None, symbol: str | None = None, parent_order_id: OrderId | None = None, from_inclusive: datetime | None = None, to_exclusive: datetime | None = None, limit: int | None = None) -> list[Order]:
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
        @deprecated(reason="Use place_order instead")
        '''
    def place_limit_order(self, *args, **kwargs) -> Order:
        '''
        @deprecated(reason="Use place_order instead")
        '''
    def place_orders(self, order_requests: Sequence[PlaceOrderRequest]) -> list[Order]:
        """
        A low level function to place multiple orders in a single function.

        This function does NOT check the validity of the parameters, so it is the user's responsibility
        to ensure that the orders are valid and will not be rejected by the OMS.

        Args:
            order_request: the PlaceOrderRequest containing the orders to place


        Example of a PlaceOrderRequest:
            order_request: PlaceOrderRequest = PlaceOrderRequest.new(
                dir=dir,
                quantity=quantity,
                symbol=symbol,
                time_in_force=time_in_force,
                limit_price=limit_price,
                order_type=order_type,
                account=account,
                id=id,
                parent_id=None,
                source=OrderSource.API,
                trader=trader,
                execution_venue=execution_venue,
                post_only=post_only,
                trigger_price=trigger_price,
            )
        """
    def place_order(self, *, id: OrderId | None = None, symbol: TradableProduct | str, execution_venue: str | None = None, dir: OrderDir, quantity: Decimal, limit_price: Decimal | None = None, order_type: OrderType = ..., time_in_force: TimeInForce = ..., price_round_method: TickRoundMethod | None = None, account: str | None = None, trader: str | None = None, post_only: bool | None = None, trigger_price: Decimal | None = None, stop_loss: TriggerLimitOrderType | None = None, take_profit_price: Decimal | None = None, **kwargs: Any) -> Order:
        '''
        Sends a regular order.

        Args:
            id: in case user wants to generate their own order id, otherwise it will be generated automatically
            symbol: the symbol to send the order for
            execution_venue: the execution venue to send the order to,
                if execution_venue is set to None, the OMS will send the order to the primary_exchange
                the primary_exchange can be deduced from `get_product_info` (generally will be "CME" or "US-EQUITIES")
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
            post_only: whether the order should be post only, NOT SUPPORTED BY ALL EXCHANGES (e.g. CME)
            trigger_price: the trigger price for the order, only relevant for stop / take_profit orders
            stop_loss_price: the stop loss price for a bracket order.
            profit_price: the take profit price for a bracket order.
        Returns:
            the Order object for the order
            The order.status should  be "PENDING" until the order is "OPEN" / "REJECTED" / "OUT" / "CANCELED" / "STALE"

            If the order is rejected, the order.reject_reason and order.reject_message will be set
        '''
    def place_batch_order(self, batch: BatchPlaceOrder) -> PlaceBatchOrderResponse:
        """
        Place a batch order.
        """
    def send_market_pro_order(self, *, id: OrderId | None = None, symbol: TradableProduct | str, execution_venue: str, dir: OrderDir, quantity: Decimal, time_in_force: TimeInForce = ..., account: str | None = None, fraction_through_market: Decimal = ...) -> Order:
        '''
        Sends a market-order like limit price based on the BBO.
        Meant to behave as a market order but with more protections.

        Args:
            id: in case user wants to generate their own order id, otherwise it will be generated automatically
            symbol: the symbol to send the order for
            execution_venue: the execution venue to send the order to
            dir: the direction of the order
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
    def cancel_all_orders(self, account: AccountIdOrName | None = None, execution_venue: str | None = None, trader: TraderIdOrEmail | None = None, *, synthetic: bool = True) -> bool:
        """
        Cancels all open orders.

        Some venues support cancel-all natively, in which case pass synthetic=False.

        Otherwise, this function will manually query for open order IDs matching
        the criteria and send cancel requests for each order.  This is also the
        default behavior (synthetic=True).

        Args:
            account: cancel all orders for this account
            execution_venue: cancel all orders for this execution venue
            trader: cancel all orders for this trader
            synthetic: see docstring

        Returns:
            True if all orders were cancelled successfully
            False if there was an error
        """
    def reconcile_out(self, *, order_id: OrderId | None = None, order_ids: list[OrderId] | None = None):
        """
        Manually reconcile orders out.

        Useful for clearing stuck orders or stale orders when a human wants to intervene.
        """
    def place_algo_order(self, *, params: SpreaderParams, id: str | None = None, trader: str | None = None):
        """
        Sends an advanced algo order such as the spreader.
        """
