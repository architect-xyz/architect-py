import asyncio
import logging
import re
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import (
    AsyncIterator,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    overload,
)

from architect_py.grpc.models.Orderflow.Orderflow import Orderflow
from architect_py.grpc.models.Orderflow.OrderflowRequest import (
    OrderflowRequest,
    OrderflowRequest_route,
    OrderflowRequestUnannotatedResponseType,
)
from architect_py.grpc.models.Orderflow.SubscribeOrderflowRequest import (
    SubscribeOrderflowRequest,
)

from .common_types import OrderDir, TradableProduct, Venue
from .graphql_client import GraphQLClient
from .graphql_client.enums import (
    OrderType,
    TimeInForce,
)
from .graphql_client.exceptions import GraphQLClientGraphQLMultiError
from .graphql_client.fragments import (
    AccountSummaryFields,
    AccountWithPermissionsFields,
    CancelFields,
    ExecutionInfoFields,
    OrderFields,
    ProductInfoFields,
)
from .graphql_client.get_fills_query import GetFillsQueryFolioHistoricalFills
from .graphql_client.place_order_mutation import PlaceOrderMutationOms
from .grpc import *
from .grpc.client import GrpcClient
from .grpc.models import definitions as grpc_definitions
from .utils.nearest_tick import TickRoundMethod
from .utils.orderbook import update_orderbook_side
from .utils.price_bands import price_band_pairs
from .utils.symbol_parsing import nominative_expiration

try:
    import pandas as pd

    from .utils.pandas import candles_to_dataframe

    FEATURE_PANDAS = True
except ImportError:
    FEATURE_PANDAS = False


class AsyncClient:
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    paper_trading: bool
    graphql_client: GraphQLClient
    grpc_core: Optional[GrpcClient] = None
    grpc_marketdata: dict[Venue, GrpcClient] = {}
    grpc_hmart: Optional[GrpcClient] = None
    jwt: str | None = None
    jwt_expiration: datetime | None = None

    l1_books: dict[Venue, dict[TradableProduct, tuple[L1BookSnapshot, asyncio.Task]]]
    l2_books: dict[Venue, dict[TradableProduct, tuple[L2BookSnapshot, asyncio.Task]]]

    # ------------------------------------------------------------
    # Initialization and configuration
    # ------------------------------------------------------------

    @staticmethod
    async def connect(
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        paper_trading: bool,
        endpoint: str = "https://app.architect.co",
        graphql_port: Optional[int] = None,
    ) -> "AsyncClient":
        """
        Connect to an Architect installation.

        Raises ValueError if the API key and secret are not the correct length or contain invalid characters.
        """
        if paper_trading:
            COLOR = "\033[30;43m"
            RESET = "\033[0m"
            print(f"🧻 {COLOR} YOU ARE IN PAPER TRADING MODE {RESET}")

        grpc_host, grpc_port, use_ssl = await resolve_endpoint(endpoint)
        logging.info(
            f"Resolved endpoint {endpoint}: {grpc_host}:{grpc_port} use_ssl={use_ssl}"
        )

        client = AsyncClient(
            api_key=api_key,
            api_secret=api_secret,
            paper_trading=paper_trading,
            grpc_host=grpc_host,
            grpc_port=grpc_port,
            graphql_port=graphql_port,
            use_ssl=use_ssl,
            _i_know_what_i_am_doing=True,
        )

        logging.info("Exchanging credentials...")
        await client.refresh_jwt()

        logging.info("Discovering marketdata endpoints...")
        await client.discover_marketdata()

        return client

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        paper_trading: bool,
        grpc_host: str = "app.architect.co",
        grpc_port: int,
        graphql_port: Optional[int] = None,
        use_ssl: bool = True,
        _i_know_what_i_am_doing: bool = False,
    ):
        """
        Use AsyncClient.connect instead.
        """
        if not _i_know_what_i_am_doing:
            raise ValueError("Use AsyncClient.connect to create an AsyncClient object.")

        if api_key is not None and not re.match(r"^[a-zA-Z0-9]{24}$", api_key):
            raise ValueError("API key must be exactly 24 alphanumeric characters")
        if api_secret is not None and not re.match(
            r"^[a-zA-Z0-9+\/=]{44}$", api_secret
        ):
            raise ValueError(
                "API secret must be a Base64-encoded string, 44 characters long"
            )

        if paper_trading and (graphql_port is not None or grpc_port is not None):
            raise ValueError(
                "If paper_trading is True, graphql_port and grpc_port must be None"
            )

        if graphql_port is None:
            if paper_trading:
                graphql_port = 5678
            else:
                graphql_port = 4567

        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_trading = paper_trading
        self.graphql_client = GraphQLClient(
            host=grpc_host,
            port=graphql_port,
            use_tls=use_ssl,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.grpc_core = GrpcClient(host=grpc_host, port=grpc_port, use_ssl=use_ssl)

    async def refresh_jwt(self, force: bool = False):
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force=True, refresh the JWT unconditionally.

        Query methods on AsyncClient that require auth will call this method internally.
        """
        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret not set")
        if self.grpc_core is None:
            raise ValueError("gRPC client to Architect not initialized")

        if (
            force
            or self.jwt_expiration is None
            or datetime.now() > self.jwt_expiration - timedelta(minutes=1)
        ):
            try:
                req = CreateJwtRequest(api_key=self.api_key, api_secret=self.api_secret)
                res: CreateJwtResponse = await self.grpc_core.unary_unary(req)
                self.jwt = res.jwt
                # CR alee: actually read the JWT to get the expiration time;
                # for now, we just "know" that the JWTs are granted for an hour
                self.jwt_expiration = datetime.now() + timedelta(hours=1)
            except Exception as e:
                logging.error("Failed to refresh gRPC credentials: %s", e)

    def set_jwt(self, jwt: str | None, jwt_expiration: datetime | None = None):
        """
        Manually set the JWT for gRPC authentication.

        Args:
            jwt: the JWT to set;
                None to clear the JWT
            jwt_expiration: when to expire the JWT
        """
        self.jwt = jwt
        self.jwt_expiration = jwt_expiration

    async def discover_marketdata(self):
        """
        Load marketdata endpoints from the server config.

        The Architect core is responsible for telling you where to find marketdata as per
        its configuration.  You can also manually set marketdata endpoints by calling
        set_marketdata directly.

        This method is called on AsyncClient.connect.
        """
        try:
            grpc_client = await self.core()
            req = ConfigRequest()
            res: ConfigResponse = await grpc_client.unary_unary(req)
            for venue, endpoint in res.marketdata.items():
                try:
                    grpc_host, grpc_port, use_ssl = await resolve_endpoint(endpoint)
                    logging.info(
                        "Setting marketdata endpoint for %s: %s:%d use_ssl=%s",
                        venue,
                        grpc_host,
                        grpc_port,
                        use_ssl,
                    )
                    self.grpc_marketdata[venue] = GrpcClient(
                        host=grpc_host, port=grpc_port, use_ssl=use_ssl
                    )
                except Exception as e:
                    logging.error("Failed to set marketdata endpoint: %s", e)
        except Exception as e:
            logging.error("Failed to get marketdata config: %s", e)

    async def set_marketdata(self, venue: Venue, endpoint: str):
        """
        Manually set the marketdata endpoint for a venue.
        """
        try:
            grpc_host, grpc_port, use_ssl = await resolve_endpoint(endpoint)
            self.grpc_marketdata[venue] = GrpcClient(
                host=grpc_host, port=grpc_port, use_ssl=use_ssl
            )
        except Exception as e:
            logging.error("Failed to set marketdata endpoint: %s", e)

    async def marketdata(self, venue: Venue) -> GrpcClient:
        """
        Get the marketdata client for a venue.
        """
        if venue not in self.grpc_marketdata:
            raise ValueError(f"Marketdata not configured for venue: {venue}")

        await self.refresh_jwt()
        self.grpc_marketdata[venue].set_jwt(self.jwt)
        return self.grpc_marketdata[venue]

    async def set_hmart(self, endpoint: str):
        """
        Manually set the hmart (historical marketdata service) endpoint.
        """
        try:
            grpc_host, grpc_port, use_ssl = await resolve_endpoint(endpoint)
            logging.info(
                "Resolved hmart endpoint %s: %s:%d use_ssl=%s",
                endpoint,
                grpc_host,
                grpc_port,
                use_ssl,
            )
            self.grpc_hmart = GrpcClient(
                host=grpc_host, port=grpc_port, use_ssl=use_ssl
            )
        except Exception as e:
            logging.error("Failed to set hmart endpoint: %s", e)

    async def hmart(self) -> GrpcClient:
        """
        Get the hmart (historical marketdata service) client.
        """
        if self.grpc_hmart is None:
            # default to historical.marketdata.architect.co
            await self.set_hmart("https://historical.marketdata.architect.co")

        if self.grpc_hmart is None:
            raise ValueError("hmart client not initialized")

        await self.refresh_jwt()
        self.grpc_hmart.set_jwt(self.jwt)
        return self.grpc_hmart

    async def core(self) -> GrpcClient:
        """
        Get the core client.
        """
        if self.grpc_core is None:
            raise ValueError("gRPC client to Architect not initialized")

        await self.refresh_jwt()
        self.grpc_core.set_jwt(self.jwt)
        return self.grpc_core

    async def who_am_i(self) -> tuple[str, str]:
        """
        Gets the user_id and user_email for the user that the API key belongs to.

        Returns:
            (user_id, user_email)
        """
        res = await self.graphql_client.user_id_query()
        return res.user_id, res.user_email

    # ------------------------------------------------------------
    # Symbology
    # ------------------------------------------------------------

    async def list_symbols(self, *, marketdata: Optional[Venue] = None) -> list[str]:
        """
        List all symbols.

        Args:
            marketdata: query marketdata endpoint for the specified venue directly;
                If provided, query the venue's marketdata endpoint directly,
                instead of the Architect core.  This is sometimes useful for
                cross-referencing symbols or checking availability.
        """
        if marketdata is not None:
            grpc_client = await self.marketdata(marketdata)
        else:
            grpc_client = await self.core()
        req = SymbolsRequest()
        res: SymbolsResponse = await grpc_client.unary_unary(req)
        return res.symbols

    async def search_symbols(
        self,
        search_string: Optional[str] = None,
        execution_venue: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[TradableProduct]:
        """
        Search for tradable products on Architect.

        Args:
            search_string: a string to search for in the symbol
                Can be "*" for wild card search.
                Examples: "ES", "NQ", "GC"
            execution_venue: the execution venue to search in
                Examples: "CME"
        """
        res = await self.graphql_client.search_symbols_query(
            search_string=search_string,
            execution_venue=execution_venue,
            offset=offset,
            limit=limit,
        )
        return res.search_symbols

    async def get_product_info(self, symbol: str) -> Optional[ProductInfoFields]:
        """
        Get information about a product, e.g. product_type, underlying, multiplier.

        Args:
            symbol: the symbol to get information for

        Returns:
            None if the symbol does not exist
        """
        res = await self.graphql_client.get_product_info_query(symbol)
        return res.product_info

    async def get_product_infos(
        self, symbols: Optional[list[str]]
    ) -> Sequence[ProductInfoFields]:
        """
        Get information about products, e.g. product_type, underlying, multiplier.

        Args:
            symbols: the symbols to get information for, or None for all symbols

        Returns:
            Product infos for each symbol.  Not guaranteed to contain all symbols
            that were asked for, or in the same order; any duplicates or invalid
            symbols will be ignored.
        """
        res = await self.graphql_client.get_product_infos_query(symbols)
        return res.product_infos

    async def get_execution_info(
        self, symbol: TradableProduct | str, execution_venue: str
    ) -> Optional[ExecutionInfoFields]:
        """
        Get information about tradable product execution, e.g. tick_size,
        step_size, margins.

        Args:
            symbol: the symbol to get execution information for
            execution_venue: the execution venue e.g. "CME"

        Returns:
            None if the symbol doesn't exist
        """
        try:
            execution_info = await self.graphql_client.get_execution_info_query(
                TradableProduct(symbol), execution_venue
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
        Get information about tradable product execution, e.g. tick_size,
        step_size, margins, for many symbols.

        Args:
            symbols: the symbols to get execution information for, or None for all symbols
            execution_venue: the execution venue e.g. "CME"

        Returns:
            Execution infos for each symbol.  Not guaranteed to contain all symbols
            that were asked for, or in the same order; any duplicates or invalid
            symbols will be ignored.
        """
        res = await self.graphql_client.get_execution_infos_query(
            symbols, execution_venue
        )
        return res.execution_infos

    async def get_cme_first_notice_date(self, symbol: str) -> Optional[date]:
        """
        @deprecated(reason="Use get_product_info instead; first_notice_date is now a field")

        Get the first notice date for a CME future.

        Args:
            symbol: the symbol to get the first notice date for a CME future

        Returns:
            The first notice date as a date object if it exists
        """
        res = await self.graphql_client.get_first_notice_date_query(symbol)
        if res is None or res.product_info is None:
            return None
        return res.product_info.first_notice_date

    async def get_futures_series(self, series_symbol: str) -> list[str]:
        """
        List all futures in a given series.

        Args:
            series_symbol: the futures series
                e.g. "ES CME Futures" would yield a list of all the ES futures
        Returns:
            List of futures products
        """
        if not series_symbol.endswith("Futures"):
            raise ValueError("series_symbol must end with 'Futures'")
        res = await self.graphql_client.get_future_series_query(series_symbol)
        return res.futures_series

    @staticmethod
    def get_expiration_from_CME_name(name: str) -> Optional[date]:
        """
        @deprecated(reason="Use utils.symbol_parsing.nominative_expiration instead")

        Get the expiration date from a CME future name.

        Args:
            name: the CME future name
                e.g. "ES 20211217 CME Future" -> date(2021, 12, 17)
        Returns:
            the expiration date as a date object
        """
        return nominative_expiration(name)

    async def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]:
        """
        @deprecated(reason="Use get_futures_series instead")

        List all futures in a given CME series.

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
        futures = await self.get_futures_series(series)
        exp_and_futures = []
        for future in futures:
            exp = nominative_expiration(future)
            if exp is not None:
                exp_and_futures.append((exp, future))
        exp_and_futures.sort(key=lambda x: x[0])
        return exp_and_futures

    async def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> str:
        """
        Get the symbol for a CME future from the root, month, and year.
        This is a simple wrapper around search_symbols.

        Args:
            root: the root symbol for the future e.g. "ES"
            month: the month of the future
            year: the year of the future
        Returns:
            The future symbol if it exists and is unique.
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
    # Marketdata
    # ------------------------------------------------------------

    async def get_market_status(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> MarketStatus:
        """
        Returns market status for symbol (e.g. if it's currently quoting or trading).

        Args:
            symbol: the symbol to get the market status for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        """
        grpc_client = await self.marketdata(venue)
        req = MarketStatusRequest(symbol=str(symbol), venue=venue)
        res: MarketStatus = await grpc_client.unary_unary(req)
        return res

    async def get_market_snapshot(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> L1BookSnapshot:
        """
        @deprecated(reason="Use get_l1_snapshot instead")

        This is an alias for l1_book_snapshot.

        Args:
            symbol: the symbol to get the market snapshot for, e.g. "ES 20250321 CME Future/USD"
            venue: the venue that the symbol is traded at, e.g. CME
        Returns:
            MarketTickerFields for the symbol
        """
        return await self.get_l1_book_snapshot(symbol=symbol, venue=venue)

    async def get_market_snapshots(
        self, symbols: list[TradableProduct | str], venue: Venue
    ) -> Sequence[L1BookSnapshot]:
        """
        @deprecated(reason="Use get_l1_snapshots instead")

            This is an alias for l1_book_snapshots.

            Args:
                symbols: the symbols to get the market snapshots for
                venue: the venue that the symbols are traded at
        """
        return await self.get_l1_book_snapshots(
            venue=venue,
            symbols=symbols,  # type: ignore
        )

    @overload
    async def get_historical_candles(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
        candle_width: CandleWidth,
        start: datetime,
        end: datetime,
        *,
        as_dataframe: Literal[True],
    ) -> pd.DataFrame: ...

    @overload
    async def get_historical_candles(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
        candle_width: CandleWidth,
        start: datetime,
        end: datetime,
    ) -> List[Candle]: ...

    async def get_historical_candles(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
        candle_width: CandleWidth,
        start: datetime,
        end: datetime,
        *,
        as_dataframe: bool = False,
    ) -> Union[List[Candle], pd.DataFrame]:
        """
        Gets historical candles for a symbol.

        Args:
            symbol: the symbol to get the candles for
            venue: the venue of the symbol
            candle_width: the width of the candles
            start: the start date to get candles for;
                For naive datetimes, the server will assume UTC.
            end: the end date to get candles for;
                For naive datetimes, the server will assume UTC.
            as_dataframe: if True, return a pandas DataFrame

        """
        grpc_client = await self.hmart()
        req = HistoricalCandlesRequest(
            venue=venue,
            symbol=str(symbol),
            candle_width=candle_width,
            start_date=start,
            end_date=end,
        )
        res: HistoricalCandlesResponse = await grpc_client.unary_unary(req)

        if as_dataframe and FEATURE_PANDAS:
            return candles_to_dataframe(res.candles)
        elif as_dataframe and not FEATURE_PANDAS:
            raise RuntimeError("as_dataframe is True but pandas is not installed")
        else:
            return res.candles

    async def get_l1_book_snapshot(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
    ) -> L1BookSnapshot:
        """
        Gets the L1 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l1 book snapshot for
            venue: the venue that the symbol is traded at
        """
        grpc_client = await self.marketdata(venue)
        req = L1BookSnapshotRequest(symbol=str(symbol), venue=venue)
        res: L1BookSnapshot = await grpc_client.unary_unary(req)
        return res

    async def get_l1_book_snapshots(
        self, symbols: list[TradableProduct | str], venue: Venue
    ) -> Sequence[L1BookSnapshot]:
        """
        Gets the L1 book snapshots for a list of symbols.

        Args:
            symbols: the symbols to get the l1 book snapshots for
            venue: the venue that the symbols are traded at
        """
        grpc_client = await self.marketdata(venue)
        req = L1BookSnapshotsRequest(symbols=symbols)
        res: ArrayOfL1BookSnapshot = await grpc_client.unary_unary(req)  # type: ignore
        return res

    async def get_l2_book_snapshot(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> L2BookSnapshot:
        """
        Gets the L2 book snapshot for a symbol.

        Args:
            symbol: the symbol to get the l2 book snapshot for
            venue: the venue that the symbol is traded at
        """
        grpc_client = await self.marketdata(venue)
        req = L2BookSnapshotRequest(symbol=str(symbol), venue=venue)
        res: L2BookSnapshot = await grpc_client.unary_unary(req)
        return res

    async def get_ticker(self, symbol: TradableProduct | str, venue: Venue) -> Ticker:
        """
        Gets the ticker for a symbol.
        """
        grpc_client = await self.marketdata(venue)
        req = TickerRequest(symbol=str(symbol), venue=venue)
        res: Ticker = await grpc_client.unary_unary(req)
        return res

    async def stream_l1_book_snapshots(
        self, symbols: Sequence[TradableProduct | str], venue: Venue
    ) -> AsyncIterator[L1BookSnapshot]:
        """
        Subscribe to the stream of L1BookSnapshots for a symbol.

        Args:
            symbols: the symbols to subscribe to;
                If symbols=None, subscribe to all symbols available for the venue.
            venue: the venue to subscribe to
        """
        grpc_client = await self.marketdata(venue)
        req = SubscribeL1BookSnapshotsRequest(symbols=list(symbols), venue=venue)
        return grpc_client.unary_stream(req)

    async def stream_l2_book_updates(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> AsyncIterator[L2BookUpdate]:
        """
        Subscribe to the stream of L2BookUpdates for a symbol.

        This stream is a diff stream; to construct and maintain the actual state of
        the L2 book, apply the updates stream using the method described.

        Args:
            symbol: the symbol to subscribe to
            venue: the marketdata venue
        """
        grpc_client = await self.marketdata(venue)
        req = SubscribeL2BookUpdatesRequest(symbol=str(symbol), venue=venue)
        return grpc_client.unary_stream(req)  # type: ignore

    async def subscribe_l1_book(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> L1BookSnapshot:
        """
        Subscribe to the L1 stream for a symbol in the background.

        If a subscription is already active, the existing reference will be
        returned; otherwise, a new subscription will be created.

        Snapshots will have an initial value of timestamp=0 and bid/ask=None.

        Args:
            symbol: the symbol to subscribe to
            venue: the marketdata venue

        Return:
            An L1 book object that is constantly updating in the background.
        """
        symbol = TradableProduct(symbol)

        if venue in self.l1_books:
            if symbol in self.l1_books[venue]:
                return self.l1_books[venue][symbol][0]
        else:
            self.l1_books[venue] = {}

        grpc_client = await self.marketdata(venue)
        book = L1BookSnapshot(symbol, 0, 0)
        self.l1_books[venue][symbol] = (
            book,
            asyncio.create_task(
                self.__subscribe_l1_book_task(symbol, venue, grpc_client, book)
            ),
        )
        return book

    async def unsubscribe_l1_book(self, symbol: TradableProduct | str, venue: Venue):
        symbol = TradableProduct(symbol)
        try:
            task = self.l1_books[venue][symbol][1]
            task.cancel()
        except Exception as e:
            logging.error(
                f"Error unsubscribing from L1 book for {symbol}, venue {venue}: {e}"
            )
        finally:
            if venue in self.l1_books and symbol in self.l1_books[venue]:
                del self.l1_books[venue][symbol]

    async def __subscribe_l1_book_task(
        self,
        symbol: TradableProduct,
        venue: Venue,
        grpc_client: GrpcClient,
        book: L1BookSnapshot,
    ):
        try:
            req = SubscribeL1BookSnapshotsRequest(symbols=[symbol], venue=venue)
            stream = grpc_client.unary_stream(req)
            async for snap in stream:
                book.tn = snap.tn
                book.ts = snap.ts
                book.a = snap.a
                book.b = snap.b
                book.rt = snap.rt
                book.rtn = snap.rtn
        except Exception as e:
            logging.error(
                f"Error subscribing to L1 book for {symbol}, venue {venue}: {e}"
            )
        finally:
            del self.l1_books[venue][symbol]

    async def subscribe_l2_book(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
    ) -> L2BookSnapshot:
        """
        Subscribe to the L2 stream for a symbol in the background.

        If a subscription is already active, the existing reference will be
        returned; otherwise, a new subscription will be created.

        Snapshots will have an initial value of timestamp=0 and bids/asks=[].

        Args:
            symbol: the symbol to subscribe to
            venue: the marketdata venue

        Return:
            An L2 book object that is constantly updating in the background.
        """
        symbol = TradableProduct(symbol)

        if venue in self.l2_books:
            if symbol in self.l2_books[venue]:
                return self.l2_books[venue][symbol][0]
        else:
            self.l2_books[venue] = {}

        grpc_client = await self.marketdata(venue)
        book = L2BookSnapshot([], [], 0, 0, 0, 0)
        self.l2_books[venue][symbol] = (
            book,
            asyncio.create_task(
                self.__subscribe_l2_book_task(symbol, venue, grpc_client, book)
            ),
        )
        return book

    async def __subscribe_l2_book_task(
        self,
        symbol: TradableProduct,
        venue: Venue,
        grpc_client: GrpcClient,
        book: L2BookSnapshot,
    ):
        try:
            req = SubscribeL2BookUpdatesRequest(symbol=str(symbol), venue=venue)
            stream = grpc_client.unary_stream(req)  # type: ignore
            async for up in stream:
                if isinstance(up, L2BookDiff):
                    if (
                        up.sequence_id != book.sequence_id
                        or up.sequence_number != book.sequence_number + 1
                    ):
                        raise ValueError(
                            f"Received update out-of-order for L2 book: {symbol}"
                        )
                    book.sid = up.sid
                    book.sn = up.sn
                    book.ts = up.ts
                    book.tn = up.tn
                    for px, sz in up.bids:
                        update_orderbook_side(book.bids, px, sz, ascending=False)
                    for px, sz in up.asks:
                        update_orderbook_side(book.asks, px, sz, ascending=True)
                elif isinstance(up, L2BookSnapshot):
                    book.sid = up.sid
                    book.sn = up.sn
                    book.ts = up.ts
                    book.tn = up.tn
                    book.a = up.a
                    book.b = up.b
        except Exception as e:
            logging.error(
                f"Error subscribing to L2 book for {symbol}, venue {venue}: {e}"
            )
        finally:
            del self.l2_books[venue][symbol]

    async def stream_trades(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> AsyncIterator[Trade]:
        """
        Subscribe to a stream of trades for a symbol.
        """
        grpc_client = await self.marketdata(venue)
        req = SubscribeTradesRequest(symbol=str(symbol), venue=venue)
        return grpc_client.unary_stream(req)

    async def stream_candles(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
        candle_widths: Optional[list[CandleWidth]],
    ) -> AsyncIterator[Candle]:
        """
        Subscribe to a stream of candles for a symbol.
        """
        grpc_client = await self.marketdata(venue)
        req = SubscribeCandlesRequest(
            symbol=str(symbol),
            venue=venue,
            candle_widths=candle_widths,
        )
        return grpc_client.unary_stream(req)

    # ------------------------------------------------------------
    # Portfolio management
    # ------------------------------------------------------------

    async def list_accounts(self) -> Sequence[AccountWithPermissionsFields]:
        """
        List accounts for the user that the API key belongs to.

        Returns:
            a list of AccountWithPermissionsFields for the user that the API key belongs to
            a list of AccountWithPermissions for the user that the API key belongs to
            (use who_am_i to get the user_id / email)
        """
        res = await self.graphql_client.list_accounts_query()
        return res.accounts

        """
    async def list_accounts(self) -> List[grpc_definitions.AccountWithPermissions]:
        request = AccountsRequest()
        accounts = await self.grpc_client.request(request)
        return accounts.accounts
        """

    async def get_account_summary(self, account: str) -> AccountSummaryFields:
        """
        Get account summary, including balances, positions, pnls, etc.

        Args:
            account: account uuid or name
                Examples: "00000000-0000-0000-0000-000000000000", "STONEX:000000/JDoe"
        """
        res = await self.graphql_client.get_account_summary_query(account=account)
        return res.account_summary
        """
        async def get_account_summary(self, account: str) -> AccountSummary:
            request = AccountSummaryRequest(account=account)
            account_summary = await self.grpc_client.request(request)
            return account_summary
        """

    async def get_account_summaries(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> Sequence[AccountSummaryFields]:
        """
        Get account summaries for accounts matching the filters.

        Args:
            accounts: list of account uuids or names
            trader: if specified, return summaries for all accounts for this trader

        If both arguments are given, the union of matching accounts are returned.
        """
        res = await self.graphql_client.get_account_summaries_query(
            trader=trader, accounts=accounts
        )
        return res.account_summaries
        """
    async def get_account_summaries(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> list[AccountSummary]:
        request = AccountSummariesRequest(
            accounts=accounts,
            trader=trader,
        )
        account_summaries = await self.grpc_client.request(request)
        return account_summaries.account_summaries        
        """

    async def get_account_history(
        self,
        account: str,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
    ) -> Sequence[AccountSummaryFields]:
        """
        Get historical sequence of account summaries for the given account.
        """
        res = await self.graphql_client.get_account_history_query(
            account=account, from_inclusive=from_inclusive, to_exclusive=to_exclusive
        )
        return res.account_history

        """
    async def get_account_history(
        self,
        account: str,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
    ) -> list[AccountSummary]:        
        if from_inclusive is not None:
            assert from_inclusive.tzinfo is timezone.utc, (
                "from_inclusive must be a utc datetime:\n"
                "for example datetime.now(timezone.utc) or \n"
                "dt = datetime(2025, 4, 15, 12, 0, 0, tzinfo=timezone.utc)"
            )

        if to_exclusive is not None:
            assert to_exclusive.tzinfo is timezone.utc, (
                "to_exclusive must be a utc datetime:\n"
                "for example datetime.now(timezone.utc) or \n"
                "dt = datetime(2025, 4, 15, 12, 0, 0, tzinfo=timezone.utc)"
            )

        request = AccountHistoryRequest(
            account=account, from_inclusive=from_inclusive, to_exclusive=to_exclusive
        )
        history = await self.grpc_client.request(request)
        return history.history
        """

    # ------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------

    async def get_open_orders(
        self,
        order_ids: Optional[list[str]] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        symbol: Optional[str] = None,
        parent_order_id: Optional[str] = None,
    ) -> Sequence[OrderFields]:
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
        res = await self.graphql_client.get_open_orders_query(
            venue=venue,
            account=account,
            trader=trader,
            symbol=symbol,
            parent_order_id=parent_order_id,
            order_ids=order_ids,
        )
        return res.open_orders

    async def get_all_open_orders(self) -> Sequence[OrderFields]:
        """
        @deprecated(reason="Use get_open_orders with no parameters instead")

        Returns a list of all open orders for the authenticated user.
        """
        res = await self.graphql_client.get_open_orders_query()
        return res.open_orders

    async def get_historical_orders(
        self,
        order_ids: Optional[list[str]] = None,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        parent_order_id: Optional[str] = None,
    ) -> Sequence[OrderFields]:
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
        res = await self.graphql_client.get_historical_orders_query(
            order_ids=order_ids,
            venue=venue,
            account=account,
            parent_order_id=parent_order_id,
            from_inclusive=from_inclusive,
            to_exclusive=to_exclusive,
        )
        return res.historical_orders

    async def get_order(self, order_id: str) -> Optional[OrderFields]:
        """
        Returns the specified order.  Useful for looking at past sent orders.
        Queries open_orders first, then queries historical_orders.

        Args:
            order_id: the order id to get
        """
        res = await self.graphql_client.get_open_orders_query(order_ids=[order_id])
        for open_order in res.open_orders:
            if open_order.id == order_id:
                return open_order

        res = await self.graphql_client.get_historical_orders_query(
            order_ids=[order_id]
        )
        if res.historical_orders and len(res.historical_orders) > 0:
            return res.historical_orders[0]

    async def get_orders(self, order_ids: list[str]) -> list[Optional[OrderFields]]:
        """
        Returns the specified orders.  Useful for looking at past sent orders.
        Plural form of get_order.

        Args:
            order_ids: a list of order ids to get
        """
        orders_dict: dict[str, Optional[OrderFields]] = {
            order_id: None for order_id in order_ids
        }

        res = await self.graphql_client.get_open_orders_query(order_ids=order_ids)
        open_orders = res.open_orders
        for open_order in open_orders:
            orders_dict[open_order.id] = open_order

        not_open_order_ids = [
            order_id for order_id in order_ids if orders_dict[order_id] is None
        ]

        res = await self.graphql_client.get_historical_orders_query(
            order_ids=not_open_order_ids
        )
        historical_orders = res.historical_orders
        for historical_order in historical_orders:
            orders_dict[historical_order.id] = historical_order

        return [orders_dict[order_id] for order_id in order_ids]

    async def get_fills(
        self,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        order_id: Optional[str] = None,
    ) -> GetFillsQueryFolioHistoricalFills:
        """
        Returns all fills matching the given filters.

        Args:
            from_inclusive: the start date to get fills for
            to_exclusive: the end date to get fills for
            venue: the venue to get fills for, e.g. "CME"
            account: account uuid or name
            order_id: the order id to get fills for
        """
        res = await self.graphql_client.get_fills_query(
            venue, account, order_id, from_inclusive, to_exclusive
        )
        return res.historical_fills

    async def orderflow(
        self,
        request_iterator: AsyncIterator[OrderflowRequest],
    ) -> AsyncIterator[Orderflow]:
        """
        A two-way channel for both order entry and listening to order updates (fills, acks, outs, etc.).

        This is considered the most efficient way to trade in this SDK.

        Example:
            See test_orderflow.py for an example.

        This WILL block the event loop until the stream is closed.
        """
        grpc_client = await self.core()
        decoder = grpc_client.get_decoder(OrderflowRequestUnannotatedResponseType)
        stub = grpc_client.channel.stream_stream(
            OrderflowRequest_route,
            request_serializer=grpc_client.encoder().encode,
            response_deserializer=decoder.decode,
        )
        call = stub(
            request_iterator, metadata=(("authorization", f"Bearer {grpc_client.jwt}"),)
        )
        async for update in call:
            yield update

    async def stream_orderflow(
        self,
        account: Optional[grpc_definitions.AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        trader: Optional[grpc_definitions.TraderIdOrEmail] = None,
    ) -> AsyncIterator[Orderflow]:
        """
        A stream for listening to order updates (fills, acks, outs, etc.).

        Example:
            ```python
            request = SubscribeOrderflowRequest.new()
            async for of in client.subscribe_orderflow_stream(request):
                print(of)
            ```

        This WILL block the event loop until the stream is closed.
        """
        grpc_client = await self.core()
        request: SubscribeOrderflowRequest = SubscribeOrderflowRequest(
            account=account, execution_venue=execution_venue, trader=trader
        )
        grpc_client = await self.core()
        decoder = grpc_client.get_decoder(SubscribeOrderflowRequest)
        stub = grpc_client.channel.unary_stream(
            SubscribeOrderflowRequest.get_route(),
            request_serializer=grpc_client.encoder().encode,
            response_deserializer=decoder.decode,
        )
        call = stub(request, metadata=(("authorization", f"Bearer {grpc_client.jwt}"),))
        async for update in call:
            yield update

    # ------------------------------------------------------------
    # Order entry
    # ------------------------------------------------------------

    async def place_limit_order(
        self,
        *,
        id: Optional[str] = None,
        symbol: TradableProduct | str,
        execution_venue: Optional[str],
        odir: OrderDir,
        quantity: Decimal,
        limit_price: Decimal,
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TimeInForce = TimeInForce.DAY,
        good_til_date: Optional[datetime] = None,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        post_only: bool = False,
        trigger_price: Optional[Decimal] = None,
    ) -> OrderFields:
        """
        Sends a regular limit order.

        Args:
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
            the OrderFields object for the order
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

        order: PlaceOrderMutationOms = await self.graphql_client.place_order_mutation(
            symbol,
            odir,
            quantity,
            order_type,
            time_in_force,
            id,
            trader,
            account,
            limit_price,
            post_only,
            trigger_price,
            good_til_date,
            execution_venue,
        )

        return order.place_order

    async def send_market_pro_order(
        self,
        *,
        id: Optional[str] = None,
        symbol: TradableProduct | str,
        execution_venue: str,
        odir: OrderDir,
        quantity: Decimal,
        time_in_force: TimeInForce = TimeInForce.DAY,
        account: Optional[str] = None,
        fraction_through_market: Decimal = Decimal("0.001"),
    ) -> OrderFields:
        """
        Sends a market-order like limit price based on the BBO.
        Meant to behave as a market order but with more protections.

        Args:
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

        ticker = await self.get_ticker(symbol, execution_venue)
        if ticker is None:
            raise ValueError(
                f"Failed to send market order with reason: no ticker for {symbol}"
            )

        price_band = price_band_pairs.get(symbol, None)

        if odir == OrderDir.BUY:
            if ticker.ask_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no ask price for {symbol}"
                )
            limit_price = ticker.ask_price * (1 + fraction_through_market)

            if price_band and ticker.last_price:
                price_band_reference_price = ticker.last_price + price_band
                limit_price = min(limit_price, price_band_reference_price)

        else:
            if ticker.bid_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no bid price for {symbol}"
                )
            limit_price = ticker.bid_price * (1 - fraction_through_market)
            if price_band and ticker.last_price:
                price_band_reference_price = ticker.last_price - price_band
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

        return await self.place_limit_order(
            id=id,
            symbol=symbol,
            execution_venue=execution_venue,
            odir=odir,
            quantity=quantity,
            account=account,
            order_type=OrderType.LIMIT,
            limit_price=limit_price,
            time_in_force=time_in_force,
        )

    async def cancel_order(self, order_id: str) -> CancelFields:
        """
        Cancels an order by order id.

        Args:
            order_id: the order id to cancel
        Returns:
            the CancelFields object
        """
        cancel = await self.graphql_client.cancel_order_mutation(order_id)
        return cancel.cancel_order

    async def cancel_all_orders(self) -> bool:
        """
        Cancels all open orders.

        Returns:
            True if all orders were cancelled successfully
            False if there was an error
        """
        b = await self.graphql_client.cancel_all_orders_mutation()
        return b.cancel_all_orders
