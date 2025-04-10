"""
This file composes the GraphQLClient class to provide a higher-level interface
for order entry with the Architect API.

These are not required to send orders, but provide typed interfaces for the
various order types and algorithms that can be sent to the OMS.


The functions to send orders will return the order ID string
After sending the order, this string can be used to retrieve the order status

send_limit_order -> get_order

The individual graphql types are subject to change, so it is not recommended to use them directly.
"""

import asyncio
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Any, AsyncIterator, List, Optional, Sequence

from architect_py.graphql_client.exceptions import GraphQLClientGraphQLMultiError

from architect_py.grpc_client.Accounts.AccountsRequest import AccountsRequest
from architect_py.grpc_client.Folio.AccountHistoryRequest import AccountHistoryRequest
from architect_py.grpc_client.Folio.AccountSummariesRequest import (
    AccountSummariesRequest,
)
from architect_py.grpc_client.Folio.AccountSummary import AccountSummary
from architect_py.grpc_client.Folio.AccountSummaryRequest import AccountSummaryRequest
from architect_py.grpc_client.Folio.HistoricalFillsRequest import HistoricalFillsRequest
from architect_py.grpc_client.Folio.HistoricalFillsResponse import (
    HistoricalFillsResponse,
)
from architect_py.grpc_client.Folio.HistoricalOrdersRequest import (
    HistoricalOrdersRequest,
)
from architect_py.grpc_client.Marketdata.Candle import Candle
from architect_py.grpc_client.Marketdata.HistoricalCandlesRequest import (
    HistoricalCandlesRequest,
)
from architect_py.grpc_client.Marketdata.HistoricalCandlesResponse import (
    HistoricalCandlesResponse,
)
from architect_py.grpc_client.Marketdata.SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from architect_py.grpc_client.Oms.Cancel import Cancel
from architect_py.grpc_client.Oms.CancelOrderRequest import CancelOrderRequest
from architect_py.grpc_client.Oms.OpenOrdersRequest import OpenOrdersRequest
from architect_py.grpc_client.Oms.Order import Order
from architect_py.grpc_client.Oms.PlaceOrderRequest import (
    PlaceOrderRequest,
    PlaceOrderRequestType,
)
from architect_py.grpc_client.Orderflow.Orderflow import Orderflow
from architect_py.grpc_client.Orderflow.OrderflowRequest import (
    OrderflowRequest,
    OrderflowRequest_route,
    OrderflowRequestUnannotatedResponseType,
)
from architect_py.grpc_client.Orderflow.SubscribeOrderflowRequest import (
    SubscribeOrderflowRequest,
)
import architect_py.grpc_client.definitions as grpc_definitions
from architect_py.grpc_client.Marketdata.L1BookSnapshot import L1BookSnapshot
from architect_py.grpc_client.Marketdata.L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_client.Marketdata.L2BookUpdate import L2BookUpdate
from architect_py.grpc_client.Marketdata.SubscribeCandlesRequest import (
    SubscribeCandlesRequest,
)
from architect_py.grpc_client.Marketdata.SubscribeTradesRequest import (
    SubscribeTradesRequest,
)
from architect_py.grpc_client.Marketdata.Trade import Trade
from architect_py.scalars import OrderDir, TradableProduct
from architect_py.utils.nearest_tick import TickRoundMethod

from .graphql_client import GraphQLClient
from .graphql_client.fragments import (
    ExecutionInfoFields,
    L2BookFields,
    MarketStatusFields,
    MarketTickerFields,
    ProductInfoFields,
)

# from .graphql_client.input_types import (
#     CreateMMAlgo,
#     CreateOrder,
#     CreatePovAlgo,
#     CreateSmartOrderRouterAlgo,
#     CreateSpreadAlgo,
#     CreateSpreadAlgoHedgeMarket,
#     CreateTimeInForce,
#     CreateTimeInForceInstruction,
#     CreateTwapAlgo,
# )
from .grpc_client import GRPCClient

from .utils.price_bands import price_band_pairs

logger = logging.getLogger(__name__)


class AsyncClient:
    graphql_client: GraphQLClient
    grpc_client: GRPCClient

    # ------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------

    @staticmethod
    async def connect(
        *,
        api_key: str,
        api_secret: str,
        paper_trading: bool,
        host: str = "app.architect.co",
        grpc_endpoint: str = "cme.marketdata.architect.co",
        _port: Optional[int] = None,
        **kwargs: Any,
    ) -> "AsyncClient":
        """
        The main way to create an AsyncClient object.

        Args:
            api_key: API key for the user
            api_secret: API secret for the user
            host: Host for the GraphQL server, defaults to "app.architect.co"
            paper_trading: Whether to use the paper trading environment, defaults to True
            _port: Port for the GraphQL server, more for debugging purposes, do not set this unless you are sure of the port

        the API key and secret can be generated on the app.architect.co website

        Returns:
            Client object

        Raises:
            ValueError: If the API key or secret are not the correct length or contain invalid characters

        For any request, if you get a "GraphQLClientHttpError: HTTP status code: 500" it likely means that your
        API key and secret are incorrect. Please double check your credentials.

        If you get a "GraphQLClientHttpError: HTTP status code: 400", please contact support so we can fix the function.

        If you get an AttributeError on the grpc_client, it means that the GRPC client has not been initialized
        likely due to the client not being instantiated with the connect method
        """
        if paper_trading:
            logger.critical(
                "You are using the paper trading environment. Please make sure to switch to the live environment when you are ready."
            )

        async_client = AsyncClient(
            api_key=api_key,
            api_secret=api_secret,
            host=host,
            paper_trading=paper_trading,
            _port=_port,
            _i_know_what_i_am_doing=True,
            **kwargs,
        )

        async_client.grpc_client = GRPCClient(
            async_client.graphql_client, grpc_endpoint
        )
        await async_client.grpc_client.initialize()
        return async_client

    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        host: str = "app.architect.co",
        paper_trading: bool = True,
        _port: Optional[int] = None,
        _i_know_what_i_am_doing: bool = False,
        **kwargs: Any,
    ):
        """
        Users should essentially never be using this constructor directly.

        Use the connect method instead.
        See self.connect for arg explanations
        """

        if not _i_know_what_i_am_doing:
            raise ValueError(
                "Please use the connect method to create an AsyncClient object."
            )

        if not api_key.isalnum():
            raise ValueError(
                "API key must be alphanumeric, please double check your credentials."
            )
        elif "," in api_key or "," in api_secret:
            raise ValueError(
                "API key and secret cannot contain commas, please double check your credentials."
            )
        elif " " in api_key or " " in api_secret:
            raise ValueError(
                "API key and secret cannot contain spaces, please double check your credentials."
            )
        elif len(api_key) != 24 or len(api_secret) != 44:
            raise ValueError(
                "API key and secret are not the correct length, please double check your credentials."
            )

        if _port is None:
            if paper_trading:
                _port = 5678
            else:
                _port = 4567

        self.graphql_client = GraphQLClient(
            api_key=api_key, api_secret=api_secret, host=host, port=_port, **kwargs
        )

    async def enable_orderflow(self):
        """
        Load and cache product and execution info so that the SDK can send orders.

        CR alee: determine if this is better than @functools.lru_cache
        """
        pass

    # ------------------------------------------------------------
    # Symbology
    # ------------------------------------------------------------

    async def search_symbols(
        self,
        search_string: Optional[str] = None,
        execution_venue: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[TradableProduct]:
        """
        Search for symbols in the Architect database.

        Args:
            search_string: a string to search for in the symbol. Can be "*" for wild card search.
                Examples: "ES", "NQ", "GC"
            execution_venue: the execution venue to search in
                Examples: "CME"
        Returns:
            a list of TradableProduct objects
        """
        markets = (
            await self.graphql_client.search_symbols_query(
                search_string=search_string,
                execution_venue=execution_venue,
                offset=offset,
                limit=limit,
            )
        ).search_symbols

        return markets

    async def get_product_info(self, symbol: str) -> Optional[ProductInfoFields]:
        """
        Get the product information (product_type, underlying, multiplier, etc.) for a symbol.

        Args:
            symbol: the symbol to get information for
        Returns:
            ProductInfoFields object if the symbol exists
        """
        info = await self.graphql_client.get_product_info_query(symbol)
        return info.product_info

    async def get_product_infos(
        self, symbols: Optional[list[str]]
    ) -> Sequence[ProductInfoFields]:
        """
        Get the product information (product_type, underlying, multiplier, etc.) for a list of symbols.

        Args:
            symbols: the symbols to get information for
        Returns:
            a list of ProductInfoFields

        Any duplicate or invalid symbols will be ignored.
        The order of the symbols in the list will not necessarily be preserved in the output.

        If you want the entire universe of symbols, pass in None
        """
        infos = await self.graphql_client.get_product_infos_query(symbols)
        return infos.product_infos

    async def get_execution_info(
        self, symbol: TradableProduct, execution_venue: str
    ) -> Optional[ExecutionInfoFields]:
        """
        Get the execution information (tick_size, step_size, margin, etc.) for a symbol.

        Args:
            symbol: the symbol to get execution information for
            execution_venue: the execution venue e.g. "CME"

        Returns:
            ExecutionInfoFields

        """
        try:
            execution_info = await self.graphql_client.get_execution_info_query(
                symbol, execution_venue
            )
            return execution_info.execution_info
        except GraphQLClientGraphQLMultiError:
            # the try/except is done so it is consistent with product_info
            # execution info not found
            return None

    async def get_execution_infos(
        self,
        symbols: Optional[list[TradableProduct]],
        execution_venue: Optional[str] = None,
    ) -> Sequence[ExecutionInfoFields]:
        """
        Get the execution information (tick_size, step_size, etc.) for a list of symbols.

        Args:
            symbols: the symbols to get execution information for
            execution_venue: the execution venue e.g. "CME"

        Returns:
            a list of ExecutionInfoFields

        If you want the entire universe of execution infos, pass in None
        """
        execution_infos = await self.graphql_client.get_execution_infos_query(
            symbols, execution_venue
        )
        return execution_infos.execution_infos

    async def get_cme_first_notice_date(self, symbol: str) -> Optional[date]:
        """
        Get the first notice date for a CME future.

        Args:
            symbol: the symbol to get the first notice date for a CME future

        Returns:
            the first notice date as a date object if it exists
        """
        notice = await self.graphql_client.get_first_notice_date_query(symbol)
        if notice is None or notice.product_info is None:
            return None
        return notice.product_info.first_notice_date

    async def get_future_series(self, series_symbol: str) -> list[str]:
        """
        Get the series of futures for a given series symbol.

        Args:
            series_symbol: the symbol to get the series for
                e.g. ES CME Futures" would yield a list of all the ES futures
        Returns:
            a list of symbols in the series
        """
        assert (
            " " in series_symbol
        ), 'series_symbol must have the venue in it, e.g. "ES CME Futures" or "GC CME Futures"'

        futures_series = await self.graphql_client.get_future_series_query(
            series_symbol
        )
        return futures_series.futures_series

    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date:
        """
        Get the expiration date from a CME future name.

        Args:
            name: the CME future name
                e.g. "ES 20211217 CME Future" -> date(2021, 12, 17)
        Returns:
            the expiration date as a date object
        """
        _, d, *_ = name.split(" ")
        return datetime.strptime(d, "%Y%m%d").date()

    async def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]:
        """
        Get the futures in a series from the CME.

        Args:
            series: the series to get the futures for
                e.g. "ES CME Futures"
        Returns:
            a list of tuples of the expiration date and
            the symbol for each future in the series

            e.g.
            [(datetime.date(2025, 3, 21), 'ES 20250321 CME Future'),
             (datetime.date(2025, 6, 20), 'ES 20250620 CME Future'),
             (datetime.date(2025, 9, 19), 'ES 20250919 CME Future'),
             ...
            ]
        """
        markets = await self.get_future_series(
            series,
        )

        filtered_markets = [
            (self.get_expiration_from_CME_name(market), market) for market in markets
        ]

        filtered_markets.sort(key=lambda x: x[0])

        return filtered_markets

    async def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> str:
        """
        Get the symbol for a CME future from the root, month, and year.

        Args:
            root: the root symbol for the future e.g. "ES"
            month: the month of the future
            year: the year of the future
        Returns:
            the symbol for the future

            Errors if the result is not unique
            This is a simple wrapper around search_symbols
        """
        [market] = [
            market
            for market in await self.search_symbols(
                f"{root} {year}{month:02d}",
                execution_venue="CME",
            )
            if market.startswith(f"{root} {year}{month:02d}")
        ]

        return market

    # ------------------------------------------------------------
    # Account Management
    # ------------------------------------------------------------

    async def who_am_i(self) -> tuple[str, str]:
        """
        Gets the user_id and user_email for the user that the API key belongs to.

        Returns:
            (user_id, user_email)
        """
        user_id = await self.graphql_client.user_id_query()

        return user_id.user_id, user_id.user_email

    async def list_accounts(self) -> List[grpc_definitions.AccountWithPermissions]:
        """
        List accounts for the user that the API key belongs to.

        Returns:
            a list of AccountWithPermissions for the user that the API key belongs to
            (use who_am_i to get the user_id / email)
        """

        request = AccountsRequest()
        accounts = await self.grpc_client.request(request)
        return accounts.accounts

    async def get_account_summary(self, account: str) -> AccountSummary:
        """
        Gets the account summary for the given account.

        Args:
            account: the account to get the summary for,
                can be the account id( (a UUID) or the account name (e.g. CQG:00000)
        Returns:
            AccountSummary for the account
        """
        request = AccountSummaryRequest(account=account)
        account_summary = await self.grpc_client.request(request)
        return account_summary

    async def get_account_summaries(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> list[AccountSummary]:
        """
        Gets the account summaries for the given accounts and trader.

        Args:
            accounts: a list of account ids to get summaries for,
                can be the account id( (a UUID) or the account name (e.g. CQG:00000)
            trader: the trader / userId to get summaries for

            if both arguments are given, the accounts are all appended and returned together
        Returns:
            a list of AccountSummary for the accounts
        """
        request = AccountSummariesRequest(
            accounts=accounts,
            trader=trader,
        )
        account_summaries = await self.grpc_client.request(request)
        return account_summaries.account_summaries

    async def get_account_history(
        self,
        account: str,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
    ) -> list[AccountSummary]:
        """
        Gets the account history for the given account and dates.

        Returns:
            a list of AccountSummary for the account for the given dates
            use timestamp to get the time of the of the summary
        """
        request = AccountHistoryRequest(
            account=account, from_inclusive=from_inclusive, to_exclusive=to_exclusive
        )
        history = await self.grpc_client.request(request)
        return history.history

    # ------------------------------------------------------------
    # Order Management
    # ------------------------------------------------------------

    async def get_open_orders(
        self,
        order_ids: Optional[list[grpc_definitions.OrderId]] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        symbol: Optional[str] = None,
        parent_order_id: Optional[grpc_definitions.OrderId] = None,
    ) -> List[Order]:
        """
        Returns a list of open orders for the user that match the filters.

        Args:
            order_ids: a list of order ids to get
            venue: the venue to get orders for
            account: the account to get orders for
            trader: the trader to get orders for
            symbol: the symbol to get orders for
            parent_order_id: the parent order id to get orders for

            these filters are combinewd via OR statements so if you pass
            in multiple arguments, it will return the union of the results
        Returns:
            a list of Order of the open orders that match the union of the filters
        """
        open_orders_request = OpenOrdersRequest(
            venue=venue,
            account=account,
            trader=trader,
            symbol=symbol,
            parent_order_id=parent_order_id,
            order_ids=order_ids,
        )

        return (await self.grpc_client.request(open_orders_request)).open_orders

    async def get_all_open_orders(self) -> list[Order]:
        """
        Returns a list of all open orders for the user.

        Returns:
            a list of Order of all the open orders for the user
        """

        open_orders_request = OpenOrdersRequest()

        return (await self.grpc_client.request(open_orders_request)).open_orders

    async def get_historical_orders(
        self,
        order_ids: Optional[list[grpc_definitions.OrderId]] = None,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        parent_order_id: Optional[grpc_definitions.OrderId] = None,
    ) -> Sequence[Order]:
        """
        Gets the historical orders that match the filters.

        Args:
            order_ids: a list of order ids to get
            from_inclusive: the start date to get orders for
            to_exclusive: the end date to get orders for
            venue: the venue to get orders for, e.g. CME
            account: the account to get orders for,
                can be the account id( (a UUID) or the account name (e.g. CQG:00000)
            parent_order_id: the parent order id to get orders for
        Returns:
            a list of Order of the historical orders that match the filters

            either the order_ids parameter needs to be filled
            OR
            the from_inclusive and to_exclusive parameters need to be filled
        """
        historical_orders_request = HistoricalOrdersRequest.new(
            order_ids=order_ids,
            venue=venue,
            account=account,
            parent_order_id=parent_order_id,
            from_inclusive=from_inclusive,
            to_exclusive=to_exclusive,
        )
        orders = await self.grpc_client.request(historical_orders_request)
        return orders.orders

    async def get_order(self, order_id: grpc_definitions.OrderId) -> Optional[Order]:
        """
        Returns the OrderFields object for the specified order.
        Useful for looking at past sent orders.

        Args:
            order_id: the order id to get
        Returns:
            the Order object for the order

        Queries open_orders first then queries historical_orders
        """

        open_orders_request = OpenOrdersRequest.new(
            order_ids=[order_id],
        )

        open_orders = await self.grpc_client.request(open_orders_request)

        for open_order in open_orders.open_orders:
            if open_order.id == order_id:
                return open_order

        historical_orders_request = HistoricalOrdersRequest.new(
            order_ids=[order_id],
        )

        historical_orders = await self.grpc_client.request(historical_orders_request)

        if historical_orders.orders:
            return historical_orders.orders[0]

    async def get_orders(
        self, order_ids: list[grpc_definitions.OrderId]
    ) -> list[Optional[Order]]:
        """
        Returns a list of OrderFields objects for the specified orders.
        Useful for looking at past sent orders.

        Args:
            order_ids: a list of order ids to get
        Returns:
            a list of Order objects for the orders

        Plural form of get_order
        """
        orders_dict: dict[grpc_definitions.OrderId, Optional[Order]] = {
            order_id: None for order_id in order_ids
        }

        open_orders_request = OpenOrdersRequest.new(
            order_ids=order_ids,
        )

        open_orders = await self.grpc_client.request(open_orders_request)
        for open_order in open_orders.open_orders:
            orders_dict[open_order.id] = open_order

        not_open_order_ids = [
            order_id for order_id in order_ids if orders_dict[order_id] is None
        ]

        historical_orders_request = HistoricalOrdersRequest.new(
            order_ids=not_open_order_ids,
        )
        historical_orders = await self.grpc_client.request(historical_orders_request)

        for historical_order in historical_orders.orders:
            orders_dict[historical_order.id] = historical_order

        return [orders_dict[order_id] for order_id in order_ids]

    async def get_fills(
        self,
        from_inclusive: Optional[datetime],
        to_exclusive: Optional[datetime],
        venue: Optional[str] = None,
        account: Optional[str] = None,
        order_id: Optional[grpc_definitions.OrderId] = None,
        limit: Optional[int] = None,
    ) -> HistoricalFillsResponse:
        """
        Returns a list of fills for the given filters.

        Args:
            from_inclusive: the start date to get fills for
            to_exclusive: the end date to get fills for
            venue: the venue to get fills for, e.g. "CME"
            account: the account to get fills for,
                can be the account id( (a UUID) or the account name (e.g. CQG:00000)
            order_id: the order id to get fills for
        Returns:
            HistoricalFillsResponse
        """

        fills_request = HistoricalFillsRequest(
            account,
            from_inclusive,
            limit,
            order_id,
            to_exclusive,
            venue,
        )

        fills = await self.grpc_client.request(fills_request)

        return fills

    # ------------------------------------------------------------
    # Market Data
    # ------------------------------------------------------------

    async def get_market_status(
        self, symbol: TradableProduct, venue: str
    ) -> MarketStatusFields:
        """
        Returns market status for symbol (ie if it is quoting and trading).

        Args:
            symbol: the symbol to get the market status for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        Returns:
            MarketStatusFields for the symbol
        """
        market_status = await self.graphql_client.get_market_status_query(symbol, venue)
        return market_status.market_status

    async def get_market_snapshot(
        self, symbol: TradableProduct, venue: str
    ) -> MarketTickerFields:
        """
        This is an alias for l1_book_snapshot.

        Args:
            symbol: the symbol to get the market snapshot for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        Returns:
            MarketTickerFields for the symbol
        """
        return await self.get_l1_book_snapshot(symbol=symbol, venue=venue)

    async def get_market_snapshots(
        self, symbols: list[TradableProduct], venue: str
    ) -> Sequence[MarketTickerFields]:
        """
        This is an alias for l1_book_snapshot.

        Args:
            symbols: the symbols to get the market snapshots for
            venue: the venue that the symbols are traded at
        Returns:
            a list of MarketTickerFields for the symbols
        """
        return await self.get_l1_book_snapshots(
            venue=venue, symbols=symbols  # type: ignore
        )

    async def get_historical_candles(
        self,
        symbol: str,
        candle_width: grpc_definitions.CandleWidth,
        start: datetime,
        end: datetime,
    ) -> HistoricalCandlesResponse:
        """
        Gets the historical candles for a symbol.

        Args:
            symbol: the symbol to get the candles for
            venue: the venue of the symbol
            candle_width: the width of the candles
            start: the start date to get candles for
            end: the end date to get candles for
        Returns:
            a list of CandleFields for the specified candles
        """
        request = HistoricalCandlesRequest(
            symbol=symbol,
            candle_width=candle_width,
            start_date=start,
            end_date=end,
        )

        return await self.grpc_client.request(request)

    async def get_l1_book_snapshot(
        self,
        symbol: str,
        venue: str,
    ) -> MarketTickerFields:
        """
        Gets the L1 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l1 book snapshot for
            venue: the venue that the symbol is traded at
        Returns:
            MarketTickerFields for the symbol
        """
        snapshot = await self.graphql_client.get_l_1_book_snapshot_query(
            symbol=symbol, venue=venue
        )
        return snapshot.ticker

    async def get_l1_book_snapshots(
        self, symbols: list[str], venue: str
    ) -> Sequence[MarketTickerFields]:
        """
        Gets the L1 book snapshots for a list of symbols.

        Args:
            symbols: the symbols to get the l1 book snapshots for
            venue: the venue that the symbols are traded at
        Returns:
            a list of MarketTickerFields for the symbols
        """
        snapshot = await self.graphql_client.get_l_1_book_snapshots_query(
            venue=venue, symbols=symbols
        )
        return snapshot.tickers

    async def get_l2_book_snapshot(self, symbol: str, venue: str) -> L2BookFields:
        """
        Gets the L2 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l2 book snapshot for
            venue: the venue that the symbol is traded at
        Returns:
            L2BookFields for the symbol

            Note: this does NOT update, it is a snapshot at a given time
            For an object that updates, use subscribe_l2_book
        """
        l2_book = await self.graphql_client.get_l_2_book_snapshot_query(
            symbol=symbol, venue=venue
        )
        return l2_book.l_2_book_snapshot

    async def subscribe_l1_books_stream(
        self, symbols: list[TradableProduct]
    ) -> AsyncIterator[L1BookSnapshot]:
        """
        Subscribe to the stream of L1BookSnapshots for a symbol.

        Args:
            symbol: the symbol to subscribe to
            venue: the venue to subscribe to
        Returns:
            an async iterator that yields L1BookSnapshot, representing the l1 book updates

        Example usage:
            async for snap in async_client.subscribe_l1_books_stream(symbols):
                print(snap.datetime_local, snap)
        """
        request = SubscribeL1BookSnapshotsRequest(symbols=symbols)  # type: ignore

        async for snap in self.grpc_client.subscribe(
            request,
        ):
            yield snap

    async def subscribe_l2_book_stream(
        self, symbol: TradableProduct, venue: str
    ) -> AsyncIterator[L2BookUpdate]:
        """
        Subscribe to the stream of L2BookUpdates for a symbol.

        IMPORTANT: note that the Snapshot is a different type than
        L2BookSnapshot
        Args:
            symbol: the symbol to subscribe to
            venue: the venue to subscribe to
        Returns:
            an async iterator that yields L2BookFields
            L2BookFields is either a Snapshot or a Diff
            See the grpc_client code for how to handle the different types
        """
        return self.grpc_client.subscribe_l2_books_stream(symbol=symbol, venue=venue)

    async def subscribe_l1_book(
        self, symbols: list[TradableProduct]
    ) -> list[L1BookSnapshot]:
        """
        Returns a L1BookSnapshot object that is constantly updating in the background.

        Args:
            symbols: the symbols to subscribe to
        Return:
            a list of L1BookSnapshot objects that are constantly updating in the background
            For the duration of the program, the client will be subscribed to the stream
            and be updating the L1BookSnapshot.

            IMPORTANT: The L1BookSnapshot will be initialized with
            a timestamp (field tn and ts) of 0
            along with None for bid and ask

            The reference to the object should be kept, but can also be referenced via
            client.grpc_client.l1_books.get(symbol)

        If you want direct access to the stream to do on_update type code, you can
        call client.grpc_client.stream_l1_books
        """
        books = self.grpc_client.initialize_l1_books(symbols)
        asyncio.create_task(self.grpc_client.watch_l1_books(symbols=symbols))
        i = 0
        while not all(book.ts > 0 for book in books) and i < 10:
            await asyncio.sleep(0.2)
            i += 1
        if i == 10:
            raise ValueError(
                f"Could not get L1 books for {symbols}. Check if market is quoting via client.get_market_status."
            )

        return books

    async def subscribe_l2_book(
        self,
        symbol: TradableProduct,
        venue: Optional[str],
    ) -> L2BookSnapshot:
        """
        Returns a L2BookSnapshot object that is constantly updating in the background.

        Args:
            symbols: the symbols to subscribe to
        Return:
            a list of L2BookSnapshot object that is constantly updating in the background
            For the duration of the program, the client will be subscribed to the stream
            and be updating the L2BookSnapshot.

            IMPORTANT: The LBBookSnapshot will be initialized with
            a timestamp (field tn and ts) of 0
            along with None for bid and ask

            The reference to the object should be kept, but can also be referenced via
            client.grpc_client.l1_books.get(symbol)

        If you want direct access to the stream to do on_update type code, you can
        call client.grpc_client.stream_l2_book
        """
        book = self.grpc_client.initialize_l2_book(symbol, venue)
        asyncio.create_task(self.grpc_client.watch_l2_book(symbol, venue))
        i = 0
        while book.ts == 0 and i < 10:
            await asyncio.sleep(0.2)
            i += 1
        if book.ts == 0:
            if venue:
                market_status = await self.get_market_status(symbol, venue)
                if not market_status.is_quoting:
                    raise ValueError(
                        f"Market {symbol} is currently closed, cannot get L2."
                    )
            raise ValueError(f"Could not get L2 book for {symbol}.")

        return book

    def subscribe_trades_stream(
        self, symbol: TradableProduct, venue: Optional[str]
    ) -> AsyncIterator[Trade]:
        """
        Subscribe to a stream of trades for a symbol.

        Example usage:
        tp = TradableProduct("ES 20250620 CME Future/USD")
        async for trade in client.subscribe_trades_stream(tp, "CME"):
            print(trade.datetime_local, trade)

        This WILL block the event loop until the stream is closed.
        """
        request = SubscribeTradesRequest(symbol=symbol, venue=venue)
        return self.grpc_client.subscribe(request)

    def subscribe_candles_stream(
        self,
        symbol: TradableProduct,
        venue: Optional[str],
        candle_widths: Optional[list[grpc_definitions.CandleWidth]],
    ) -> AsyncIterator[Candle]:
        """
        Subscribe to a stream of candles for a symbol.

        Example usage:
        tp = TradableProduct("ES 20250620 CME Future/USD")
        async for candle in client.subscribe_candles_stream(tp, "CME"):
            print(trade.datetime_local, trade)

        This WILL block the event loop until the stream is closed.
        """
        request = SubscribeCandlesRequest(
            symbol=str(symbol),
            venue=venue,
            candle_widths=candle_widths,
        )
        return self.grpc_client.subscribe(request)

    async def subscribe_orderflow_duplex(
        self,
        request_iterator: AsyncIterator[OrderflowRequest],
    ) -> AsyncIterator[Orderflow]:
        """
        A duplex stream for both SENDING orders and RECEIVING order updates (fills, acks, outs, etc.).

        The sending will go in the request_iterator and the receiving will be yielded from the function.

        This WILL block the event loop until the stream is closed.
        """
        decoder = self.grpc_client.get_decoder(OrderflowRequestUnannotatedResponseType)
        stub = self.grpc_client.channel.stream_stream(
            OrderflowRequest_route,
            request_serializer=self.grpc_client.encoder().encode,
            response_deserializer=decoder.decode,
        )
        jwt = await self.grpc_client.refresh_grpc_credentials()
        call = stub(request_iterator, metadata=(("authorization", f"Bearer {jwt}"),))
        async for update in call:
            yield update

    async def subscribe_orderflow_stream(
        self,
        account: Optional[grpc_definitions.AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        trader: Optional[grpc_definitions.TraderIdOrEmail] = None,
    ) -> AsyncIterator[Orderflow]:
        """
        A stream for receiving order updates (fills, acks, outs, etc.).

        Example:
            request = SubscribeOrderflowRequest.new()
            async for of in client.subscribe_orderflow_stream(request):
                print(of)

        This WILL block the event loop until the stream is closed.
        """
        request: SubscribeOrderflowRequest = SubscribeOrderflowRequest(
            account=account, execution_venue=execution_venue, trader=trader
        )
        decoder = self.grpc_client.get_decoder(SubscribeOrderflowRequest)
        stub = self.grpc_client.channel.unary_stream(
            SubscribeOrderflowRequest.get_route(),
            request_serializer=self.grpc_client.encoder().encode,
            response_deserializer=decoder.decode,
        )
        jwt = await self.grpc_client.refresh_grpc_credentials()
        call = stub(request, metadata=(("authorization", f"Bearer {jwt}"),))
        async for update in call:
            yield update

    # ------------------------------------------------------------
    # Order Entry and Cancellation
    # ------------------------------------------------------------

    async def send_limit_order(
        self,
        *,
        id: Optional[grpc_definitions.OrderId] = None,
        symbol: TradableProduct,
        execution_venue: Optional[str],
        odir: OrderDir,
        quantity: Decimal,
        limit_price: Decimal,
        order_type: PlaceOrderRequestType = PlaceOrderRequestType.LIMIT,
        time_in_force: grpc_definitions.TimeInForce = grpc_definitions.TimeInForceEnum.DAY,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        post_only: bool = False,
        trigger_price: Optional[Decimal] = None,
    ) -> Order:
        """
        Sends a regular limit order.

        Args:
            id: in case user wants to generate their own order id, otherwise it will be generated automatically
            symbol: the symbol to send the order for
            execution_venue: the execution venue to send the order to,
                if execution_venue is set to None, the OMS will send the order to the primary_exchange
                the primary_exchange can be deduced from `get_product_info`
            odir: the direction of the order
            quantity: the quantity of the order
            limit_price: the limit price of the order
                It is highly recommended to make this a Decimal object from the decimal module to avoid floating point errors
            order_type: the type of the order
            time_in_force: the time in force of the order
            good_til_date: the date the order is good until, only relevant for time_in_force = "GTD"
            price_round_method: the method to round the price to the nearest tick, will not round if None
            account: the account to send the order for
                While technically optional, for most order types, the account is required
            trader: the trader to send the order for, defaults to the user's trader
                for when sending order for another user, not relevant for vast majority of users
            post_only: whether the order should be post only, not supported by all exchanges
            trigger_price: the trigger price for the order, only relevant for stop / take_profit orders
        Returns:
            the Order object for the order
            The order.status should  be "PENDING" until the order is "OPEN" / "REJECTED" / "OUT" / "CANCELED" / "STALE"

            If the order is rejected, the order.reject_reason and order.reject_message will be set
        """
        assert quantity > 0, "quantity must be positive"

        if price_round_method is not None:
            if execution_venue is None:
                product_info = await self.get_product_info(symbol)
                if product_info is None:
                    raise ValueError(
                        f"Could not find product information for {symbol} while trying to get execution venue for rounding price"
                    )
                execution_venue = product_info.primary_venue
                if execution_venue is None:
                    raise ValueError(
                        f"Could not find primary exchange for {symbol} while trying to get execution venue for rounding price"
                    )
            execution_info = await self.get_execution_info(
                TradableProduct(symbol), execution_venue
            )
            if execution_info is None:
                raise ValueError(
                    "Could not find execution information for {symbol} for rounding price for limit order. Please round price manually."
                )
            if (tick_size := execution_info.tick_size) is not None:
                if tick_size:
                    limit_price = price_round_method(limit_price, tick_size)
            else:
                raise ValueError(f"Could not find market information for {symbol}")

        if not isinstance(trigger_price, Decimal) and trigger_price is not None:
            trigger_price = Decimal(trigger_price)

        place_order_request: PlaceOrderRequest = PlaceOrderRequest.new(
            odir,
            quantity,
            symbol,
            time_in_force,
            limit_price,
            order_type,
            account,
            id,
            None,
            grpc_definitions.OrderSource.API,
            trader,
            execution_venue,
            post_only,
            trigger_price,
        )

        order = await self.grpc_client.request(place_order_request)

        return order

    async def send_market_pro_order(
        self,
        *,
        id: Optional[grpc_definitions.OrderId] = None,
        symbol: TradableProduct,
        execution_venue: str,
        odir: OrderDir,
        quantity: Decimal,
        time_in_force: grpc_definitions.TimeInForce = grpc_definitions.TimeInForceEnum.DAY,
        account: Optional[str] = None,
        fraction_through_market: Decimal = Decimal("0.001"),
    ) -> Order:
        """
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
        """

        # Check for GQL failures
        bbo_snapshot = await self.get_market_snapshot(
            symbol=symbol, venue=execution_venue
        )
        if bbo_snapshot is None:
            raise ValueError(
                f"Failed to send market order with reason: no market snapshot for {symbol}"
            )

        price_band = price_band_pairs.get(symbol, None)

        if odir == OrderDir.BUY:
            if bbo_snapshot.ask_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no ask price for {symbol}"
                )
            limit_price = bbo_snapshot.ask_price * (1 + fraction_through_market)

            if price_band and bbo_snapshot.last_price:
                price_band_reference_price = bbo_snapshot.last_price + price_band
                limit_price = min(limit_price, price_band_reference_price)

        else:
            if bbo_snapshot.bid_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no bid price for {symbol}"
                )
            limit_price = bbo_snapshot.bid_price * (1 - fraction_through_market)
            if price_band and bbo_snapshot.last_price:
                price_band_reference_price = bbo_snapshot.last_price - price_band
                limit_price = min(limit_price, price_band_reference_price)

        # Conservatively round price to nearest tick
        tick_round_method = (
            TickRoundMethod.FLOOR if odir == OrderDir.BUY else TickRoundMethod.CEIL
        )

        execution_info = await self.get_execution_info(
            execution_venue=execution_venue, symbol=symbol
        )

        if (
            execution_info is not None
            and (tick_size := execution_info.tick_size) is not None
        ):
            limit_price = tick_round_method(limit_price, tick_size)

        return await self.send_limit_order(
            id=id,
            symbol=symbol,
            execution_venue=execution_venue,
            odir=odir,
            quantity=quantity,
            account=account,
            order_type=PlaceOrderRequestType.LIMIT,
            limit_price=limit_price,
            time_in_force=time_in_force,
        )

    async def cancel_order(self, order_id: grpc_definitions.OrderId) -> Cancel:
        """
        Cancels an order by order id.

        Args:
            order_id: the order id to cancel
        Returns:
            the Cancel object
        """
        cancel_request = CancelOrderRequest.new(order_id=order_id)
        cancel = await self.grpc_client.request(cancel_request)
        return cancel

    async def cancel_all_orders(self) -> bool:
        """
        Cancels all open orders.

        Returns:
            True if all orders were cancelled successfully
            False if there was an error
        """
        b = await self.graphql_client.cancel_all_orders_mutation()
        return b.cancel_all_orders
