import asyncio
import logging
import re
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import (
    Any,
    AsyncGenerator,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload,
)

import pandas as pd

from architect_py.batch_place_order import BatchPlaceOrder

# cannot do architect_py import * due to circular import
from architect_py.common_types import OrderDir, TimeInForce, TradableProduct, Venue
from architect_py.graphql_client import GraphQLClient
from architect_py.graphql_client.exceptions import GraphQLClientGraphQLMultiError
from architect_py.graphql_client.fragments import (
    ExecutionInfoFields,
    ProductInfoFields,
)
from architect_py.grpc.client import GrpcClient
from architect_py.grpc.models import *
from architect_py.grpc.models.definitions import (
    AccountIdOrName,
    AccountWithPermissions,
    CandleWidth,
    L2BookDiff,
    OrderId,
    OrderSource,
    OrderType,
    SortTickersBy,
    SpreaderParams,
    TraderIdOrEmail,
    TriggerLimitOrderType,
)
from architect_py.grpc.orderflow import OrderflowChannel
from architect_py.grpc.resolve_endpoint import PAPER_GRPC_PORT, resolve_endpoint
from architect_py.utils.nearest_tick import TickRoundMethod
from architect_py.utils.orderbook import update_orderbook_side
from architect_py.utils.pandas import candles_to_dataframe, tickers_to_dataframe
from architect_py.utils.price_bands import price_band_pairs
from architect_py.utils.symbol_parsing import nominative_expiration


class AsyncClient:
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    paper_trading: bool
    as_user: Optional[str] = None
    as_role: Optional[str] = None
    graphql_client: GraphQLClient
    grpc_options: Sequence[Tuple[str, Any]] | None = None
    grpc_core: Optional[GrpcClient] = None
    grpc_marketdata: dict[Venue, GrpcClient] = {}
    grpc_hmart: Optional[GrpcClient] = None
    jwt: str | None = None
    jwt_expiration: datetime | None = None

    l1_books: dict[
        Venue, dict[TradableProduct, tuple[L1BookSnapshot, asyncio.Task]]
    ] = {}
    l2_books: dict[
        Venue, dict[TradableProduct, tuple[L2BookSnapshot, asyncio.Task]]
    ] = {}

    # ------------------------------------------------------------
    # Initialization and configuration
    # ------------------------------------------------------------

    @staticmethod
    async def connect(
        *,
        api_key: str,
        api_secret: str,
        paper_trading: bool,
        endpoint: str = "https://app.architect.co",
        graphql_port: Optional[int] = None,
        grpc_options: Sequence[Tuple[str, Any]] | None = None,
        as_user: Optional[str] = None,
        as_role: Optional[str] = None,
        **kwargs: Any,
    ) -> "AsyncClient":
        """
        Connect to an Architect installation.

        An `api_key` and `api_secret` can be created at https://app.architect.co/api-keys.

        Raises ValueError if the API key and secret are not the correct length or contain invalid characters.

        ## Advanced configuration

        ### gRPC channel options

        Use `grpc_options` to configure gRPC channels created by this client.
        See https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments for reference.
        """
        if paper_trading:
            COLOR = "\033[30;43m"
            RESET = "\033[0m"
            print(f"🧻 {COLOR} YOU ARE IN PAPER TRADING MODE {RESET}")

        if "grpc_endpoint" in kwargs:
            logging.warning(
                "as of v5.0.0: grpc_endpoint parameter is deprecated; ignored"
            )
        if "host" in kwargs:
            logging.warning(
                "as of v5.0.0: host parameter is deprecated, use endpoint instead; setting endpoint to %s",
                kwargs["endpoint"],
            )
            endpoint = kwargs["endpoint"]

        grpc_host, grpc_port, use_ssl = await resolve_endpoint(
            endpoint, paper_trading=paper_trading
        )
        logging.info(
            f"Resolved endpoint {endpoint}: {grpc_host}:{grpc_port} use_ssl={use_ssl}"
        )

        # Sanity check paper trading on prod environments
        if paper_trading:
            if grpc_host == "app.architect.co" or grpc_host == "staging.architect.co":
                if grpc_port != PAPER_GRPC_PORT:
                    raise ValueError("Wrong gRPC port for paper trading")
                if graphql_port is not None and graphql_port != 5678:
                    raise ValueError("Wrong GraphQL port for paper trading")

        client = AsyncClient(
            api_key=api_key,
            api_secret=api_secret,
            paper_trading=paper_trading,
            as_user=as_user,
            as_role=as_role,
            grpc_host=grpc_host,
            grpc_port=grpc_port,
            grpc_options=grpc_options,
            graphql_port=graphql_port,
            use_ssl=use_ssl,
            _i_know_what_i_am_doing=True,
        )

        logging.info("Exchanging credentials...")
        await client.refresh_jwt()

        logging.info("Discovering marketdata endpoints...")
        await client._discover_marketdata()

        return client

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        paper_trading: bool,
        as_user: Optional[str] = None,
        as_role: Optional[str] = None,
        grpc_host: str = "app.architect.co",
        grpc_port: int,
        grpc_options: Sequence[Tuple[str, Any]] | None = None,
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

        if graphql_port is None:
            if paper_trading:
                graphql_port = 5678
            else:
                graphql_port = 4567

        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_trading = paper_trading
        self.as_user = as_user
        self.as_role = as_role
        self.graphql_client = GraphQLClient(
            host=grpc_host,
            port=graphql_port,
            use_tls=use_ssl,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.grpc_options = grpc_options
        self.grpc_core = GrpcClient(
            host=grpc_host,
            port=grpc_port,
            use_ssl=use_ssl,
            options=grpc_options,
            as_user=as_user,
            as_role=as_role,
        )
        self.l1_books = {}
        self.l2_books = {}

    async def close(self):
        """
        Close the gRPC channel and GraphQL client.

        This fixes the:
        Error in sys.excepthook:

        Original exception was:

        One might get when closing the client
        """
        if self.grpc_core is not None:
            await self.grpc_core.close()

        for grpc_client in self.grpc_marketdata.values():
            await grpc_client.close()

        self.grpc_marketdata.clear()
        # NB: this line removes the "Error in sys.excepthook:" on close

        if self.graphql_client is not None:
            await self.graphql_client.close()

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
                res: CreateJwtResponse = await self.grpc_core.unary_unary(
                    req, no_metadata=True
                )
                self.jwt = res.jwt
                # CR alee: actually read the JWT to get the expiration time;
                # for now, we just "know" that the JWTs are granted for an hour
                self.jwt_expiration = datetime.now() + timedelta(hours=1)
            except Exception as e:
                logging.error("Failed to refresh gRPC credentials: %s", e)

    def _set_jwt(self, jwt: str | None, jwt_expiration: datetime | None = None):
        """
        Manually set the JWT for gRPC authentication.

        Args:
            jwt: the JWT to set;
                None to clear the JWT
            jwt_expiration: when to expire the JWT
        """
        self.jwt = jwt
        self.jwt_expiration = jwt_expiration

    async def _discover_marketdata(self):
        """
        Load marketdata endpoints from the server config.

        The Architect core is responsible for telling you where to find marketdata as per
        its configuration.  You can also manually set marketdata endpoints by calling
        _set_marketdata directly.

        This method is called on AsyncClient.connect.
        """
        try:
            grpc_client = await self._core()
            req = ConfigRequest()
            res: ConfigResponse = await grpc_client.unary_unary(req)
            logging.info("Architect configuration: %s", res)
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
                        host=grpc_host,
                        port=grpc_port,
                        use_ssl=use_ssl,
                        options=self.grpc_options,
                        as_user=self.as_user,
                        as_role=self.as_role,
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
                host=grpc_host,
                port=grpc_port,
                use_ssl=use_ssl,
                options=self.grpc_options,
                as_user=self.as_user,
                as_role=self.as_role,
            )
            logging.debug(
                f"Setting marketdata endpoint for {venue}: {grpc_host}:{grpc_port} use_ssl={use_ssl}"
            )
        except Exception as e:
            logging.error("Failed to set marketdata endpoint: %s", e)

    async def _marketdata(self, venue: Venue) -> GrpcClient:
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
                host=grpc_host,
                port=grpc_port,
                use_ssl=use_ssl,
                options=self.grpc_options,
                as_user=self.as_user,
                as_role=self.as_role,
            )
        except Exception as e:
            logging.error("Failed to set hmart endpoint: %s", e)

    async def _hmart(self) -> GrpcClient:
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

    async def _core(self) -> GrpcClient:
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

    async def _auth_info(self) -> AuthInfoResponse:
        """
        Gets auth info mapping
        """
        grpc_client = await self._core()
        req = AuthInfoRequest()
        res: AuthInfoResponse = await grpc_client.unary_unary(req)
        return res

    def enable_orderflow(self):
        """
        @deprecated(reason="No longer needed; orderflow is enabled by default")
        """
        logging.warning(
            "as of v5.0.0: enable_orderflow is deprecated; orderflow is enabled by default"
        )

    async def cpty_status(
        self, kind: str, instance: Optional[str] = None
    ) -> CptyStatus:
        """
        Get cpty status.
        """
        grpc_client = await self._core()
        req = CptyStatusRequest(kind=kind, instance=instance)
        res: CptyStatus = await grpc_client.unary_unary(req)
        return res

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
            grpc_client = await self._marketdata(marketdata)
        else:
            grpc_client = await self._core()
        req = SymbolsRequest()
        res: SymbolsResponse = await grpc_client.unary_unary(req)
        return res.symbols

    async def search_symbols(
        self,
        search_string: Optional[str] = None,
        execution_venue: Optional[str] = None,
        include_expired: bool = False,
        sort_alphabetically: bool = True,
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
            include_expired=include_expired,
            sort_alphabetically=sort_alphabetically,
            offset=offset,
            limit=limit,
        )
        return res.search_symbols

    async def get_product_info(self, symbol: str) -> Optional[ProductInfoFields]:
        """
        Get information about a product, e.g. product_type, underlying, multiplier.

        Args:
            symbol: the symbol to get information for
                the symbol should *not* have a quote,
                ie "ES 20250620 CME Future" instead of "ES 20250620 CME Future/USD"

                If you used TradableProduct, you can use the base() method to get the symbol

        Returns:
            None if the symbol does not exist
        """
        res = await self.graphql_client.get_product_info_query(symbol)
        if res.product_info is None:
            if "/" in symbol:
                assert ValueError(
                    f"Product info not found for symbol: {symbol}.\n"
                    "for calling get_product_info, "
                    f"symbol {symbol} should not have a quote (ie should not end with /USD);"
                    "either use the base() method of TradableProduct, or remove the quote from the symbol"
                )
            raise ValueError(
                f"Product info not found for symbol: {symbol}."
                "Please ensure it is of the form 'ES 20250620 CME Future' or 'AAPL US Equity'."
                "(note that Future and Equity are not completely capitalized)."
            )

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
        symbols: Optional[list[TradableProduct | str]],
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
        if symbols is not None:
            tps = [TradableProduct(symbol) for symbol in symbols]
        else:
            tps = None
        res = await self.graphql_client.get_execution_infos_query(tps, execution_venue)
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

    async def get_future_series(self, series_symbol: str) -> list[str]:
        """
        @deprecated(reason="Use get_futures_series instead")
        """
        futures = await self.get_futures_series(series_symbol)
        return futures

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

        today = date.today()

        futures = [
            future
            for future in res.futures_series
            if (exp := nominative_expiration(future)) is not None and exp > today
        ]
        futures.sort()

        return futures

    async def get_front_future(
        self, series_symbol: str, venue: Optional[str] = None
    ) -> TradableProduct:
        """
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
        """
        futures = await self.get_futures_series(series_symbol)
        if not venue:
            futures.sort()
            return TradableProduct(futures[0], "USD")
        else:
            grpc_client = await self._marketdata(venue)
            req = TickersRequest(
                symbols=[TradableProduct(f"{future}/USD") for future in futures],
                k=SortTickersBy.VOLUME_DESC,
                venue=venue,
            )
            res: TickersResponse = await grpc_client.unary_unary(req)
            return TradableProduct(res.tickers[0].symbol)

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
            ```
            [
                (datetime.date(2025, 3, 21), 'ES 20250321 CME Future'),
                (datetime.date(2025, 6, 20), 'ES 20250620 CME Future'),
                (datetime.date(2025, 9, 19), 'ES 20250919 CME Future'),
                # ...
            ]
            ```
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
        grpc_client = await self._marketdata(venue)
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
            L1BookSnapshot for the symbol
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
            symbols=symbols,  # pyright: ignore[reportArgumentType]
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
            end: the end date to get candles for;
            as_dataframe: if True, return a pandas DataFrame

        """
        grpc_client = await self._hmart()
        if not start.tzinfo:
            raise ValueError("start time must be timezone-aware")
        if not end.tzinfo:
            raise ValueError("end time must be timezone-aware")
        req = HistoricalCandlesRequest(
            venue=venue,
            symbol=str(symbol),
            candle_width=candle_width,
            start_date=start.astimezone(timezone.utc),
            end_date=end.astimezone(timezone.utc),
        )
        res: HistoricalCandlesResponse = await grpc_client.unary_unary(req)

        if as_dataframe:
            return candles_to_dataframe(res.candles)
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
        grpc_client = await self._marketdata(venue)
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
        grpc_client = await self._marketdata(venue)
        req = L1BookSnapshotsRequest(symbols=symbols)
        res: ArrayOfL1BookSnapshot = await grpc_client.unary_unary(
            req  # pyright: ignore[reportArgumentType]
        )
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
        grpc_client = await self._marketdata(venue)
        req = L2BookSnapshotRequest(symbol=str(symbol), venue=venue)
        res: L2BookSnapshot = await grpc_client.unary_unary(req)
        return res

    async def get_ticker(self, symbol: TradableProduct | str, venue: Venue) -> Ticker:
        """
        Gets the ticker for a symbol.
        """
        grpc_client = await self._marketdata(venue)
        req = TickerRequest(symbol=str(symbol), venue=venue)
        res: Ticker = await grpc_client.unary_unary(req)
        return res

    async def get_tickers(
        self,
        *,
        venue: Venue,
        symbols: Optional[Sequence[TradableProduct | str]] = None,
        include_options: bool = False,
        sort_by: Optional[SortTickersBy | str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        as_dataframe: bool = False,
    ) -> Union[Sequence[Ticker], pd.DataFrame]:
        """
        Gets the tickers for a list of symbols.
        """
        grpc_client = await self._marketdata(venue)
        sort_by = SortTickersBy(sort_by) if sort_by else None
        symbols = [str(symbol) for symbol in symbols] if symbols else None
        req = TickersRequest.new(
            offset=offset,
            include_options=include_options,
            sort_by=sort_by,
            limit=limit,
            symbols=symbols,
            venue=venue,
        )
        res: TickersResponse = await grpc_client.unary_unary(req)
        if as_dataframe:
            return tickers_to_dataframe(res.tickers)
        else:
            return res.tickers

    async def stream_l1_book_snapshots(
        self,
        symbols: Sequence[TradableProduct | str],
        venue: Venue,
        *,
        send_initial_snapshots: Optional[bool] = False,
    ) -> AsyncGenerator[L1BookSnapshot, None]:
        """
        Subscribe to the stream of L1BookSnapshots for a symbol.

        Args:
            symbols: the symbols to subscribe to;
                If symbols=None, subscribe to all symbols available for the venue.
            venue: the venue to subscribe to, e.g. "CME", "US-EQUITIES"
        """
        grpc_client = await self._marketdata(venue)
        req = SubscribeL1BookSnapshotsRequest(
            symbols=list(symbols),
            venue=venue,
            send_initial_snapshots=send_initial_snapshots,
        )
        async for res in grpc_client.unary_stream(req):
            yield res

    async def stream_l2_book_updates(
        self, symbol: TradableProduct | str, venue: Venue
    ) -> AsyncGenerator[L2BookUpdate, None]:
        """
        Subscribe to the stream of L2BookUpdates for a symbol.

        This stream is a diff stream; to construct and maintain the actual state of
        the L2 book, apply the updates stream using the method described.

        Args:
            symbol: the symbol to subscribe to
            venue: the marketdata venue, e.g. "CME", "US-EQUITIES"
        """
        grpc_client = await self._marketdata(venue)
        req = SubscribeL2BookUpdatesRequest(symbol=str(symbol), venue=venue)
        async for res in grpc_client.unary_stream(
            req  # pyright: ignore[reportArgumentType]
        ):
            yield res

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
            venue: the marketdata venue, e.g. "CME", "US-EQUITIES"

        Return:
            An L1 book object that is constantly updating in the background.
        """
        symbol = TradableProduct(symbol)

        if venue in self.l1_books:
            if symbol in self.l1_books[venue]:
                return self.l1_books[venue][symbol][0]
        else:
            self.l1_books[venue] = {}

        grpc_client = await self._marketdata(venue)
        book = L1BookSnapshot(symbol, 0, 0)
        self.l1_books[venue][symbol] = (
            book,
            asyncio.create_task(
                self.__subscribe_l1_book_task(symbol, venue, grpc_client, book)
            ),
        )
        return book

    async def unsubscribe_l1_book(self, symbol: TradableProduct | str, venue: Venue):
        """
        Unsubscribe from the L1 stream for a symbol, ie undoes subscribe_l1_book.
        """
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
            req = SubscribeL1BookSnapshotsRequest(symbols=[str(symbol)], venue=venue)
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

        grpc_client = await self._marketdata(venue)
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
            stream = grpc_client.unary_stream(
                req  # pyright: ignore[reportArgumentType]
            )
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
    ) -> AsyncGenerator[Trade, None]:
        """
        Subscribe to a stream of trades for a symbol.
        """
        grpc_client = await self._marketdata(venue)
        req = SubscribeTradesRequest(symbol=str(symbol), venue=venue)
        async for res in grpc_client.unary_stream(req):
            yield res

    async def stream_candles(
        self,
        symbol: TradableProduct | str,
        venue: Venue,
        candle_widths: Optional[list[CandleWidth]],
    ) -> AsyncGenerator[Candle, None]:
        """
        Subscribe to a stream of candles for a symbol.
        """
        grpc_client = await self._marketdata(venue)
        req = SubscribeCandlesRequest(
            symbol=str(symbol),
            venue=venue,
            candle_widths=candle_widths,
        )
        async for res in grpc_client.unary_stream(req):
            yield res

    # ------------------------------------------------------------
    # Options
    # ------------------------------------------------------------

    async def get_options_chain(
        self,
        *,
        expiration: date,
        underlying: str,
        wrap: Optional[str] = None,
        venue: str,
    ) -> OptionsChain:
        """
        Get the options chain for a symbol.

        Args:
            expiration: the expiration date of the options chain
            underlying: the underlying symbol for the options chain
            wrap: the disambiguation for underlyings with multiple chains, see method `get_options_wraps`
            venue: the venue to get the options chain from, e.g. "CME", "US-EQUITIES"

        Returns:
            A list of Option objects for the symbol.
        """
        grpc_client = await self._marketdata(venue)
        req = OptionsChainRequest(
            expiration=expiration,
            underlying=underlying,
            wrap=wrap,
        )
        res: OptionsChain = await grpc_client.unary_unary(req)
        return res

    @staticmethod
    def get_option_symbol(options_contract: OptionsContract) -> TradableProduct:
        """
        Get the tradable product symbol for an options contract.
        Users can get the OptionsContract from the method `get_options_chain`

        Args:
            options_contract: the options contract to get the symbol for

        Returns:
            The tradable product symbol for the options contract.
            e.g. "AAPL US 20250718 200.00 P Option/USD"
        """
        expiration = options_contract.expiration.strftime("%Y%m%d")
        return TradableProduct(
            f"{options_contract.underlying} US {expiration} "
            f"{options_contract.strike} {options_contract.put_or_call} "
            f"Option/USD"
        )

    async def get_options_expirations(
        self, *, underlying: str, wrap: Optional[str] = None, venue: str
    ) -> OptionsExpirations:
        """
        Get the available expirations for a symbol's options chain.

        Args:
            symbol: the underlying symbol for the options chain, e.g. "TSLA US Equity"
            wrap: the disambiguation for underlyings with multiple chains, see method `get_options_wraps`
            venue: the venue to get the options expirations from, e.g. "CME", "US-EQUITIES"
        """
        grpc_client = await self._marketdata(venue)
        req = OptionsExpirationsRequest(underlying=underlying, wrap=wrap)
        res: OptionsExpirations = await grpc_client.unary_unary(req)
        return res

    async def get_options_wraps(self, *, underlying: str, venue: str) -> OptionsWraps:
        """
        Get the available wraps for a symbol's options chain.
        For disambiguation of underlyings with multiple chains.

        Args:
            underlying: the underlying symbol for the options chain
                e.g. "TSLA US Equity"
            venue: the venue to get the options wraps from, e.g. "CME", "US-EQUITIES"

        Returns:
            A list of wraps for the options chain.
            e.g. "TSLA US Equity" might yield wraps=["1TSLA", "2TSLA", "TSLA"]
        """
        grpc_client = await self._marketdata(venue)
        req = OptionsWrapsRequest(underlying=underlying)
        res: OptionsWraps = await grpc_client.unary_unary(req)
        return res

    async def get_options_contract_greeks(
        self, *, contract: str, venue: str
    ) -> OptionsGreeks:
        """
        Get the greeks for a specific options contract.

        Args:
            contract: the specific options contract to get the greeks for, e.g. "AAPL US 20250718 200.00 P Option/USD"
            venue: the venue to get the options greeks from, e.g. "CME", "US-EQUITIES"
        """
        grpc_client = await self._marketdata(venue)
        req = OptionsContractGreeksRequest(tradable_product=contract)
        res: OptionsGreeks = await grpc_client.unary_unary(req)
        return res

    async def get_options_chain_greeks(
        self,
        *,
        expiration: date,
        underlying: str,
        wrap: Optional[str] = None,
        venue: str,
    ) -> OptionsChainGreeks:
        """
        Get the greeks for the options chain of a specific underlying.
        """
        grpc_client = await self._marketdata(venue)
        req = OptionsChainGreeksRequest(
            underlying=underlying, expiration=expiration, wrap=wrap
        )
        res: OptionsChainGreeks = await grpc_client.unary_unary(req)
        return res

    # ------------------------------------------------------------
    # Portfolio management
    # ------------------------------------------------------------

    async def list_accounts(self) -> List[AccountWithPermissions]:
        """
        List accounts for the user that the API key belongs to.

        Returns:
            a list of AccountWithPermissionsFields for the user that the API key belongs to
            a list of AccountWithPermissions for the user that the API key belongs to
            (use who_am_i to get the user_id / email)
        """
        grpc_client = await self._core()
        req = AccountsRequest(paper=self.paper_trading)
        res = await grpc_client.unary_unary(req)
        return res.accounts

    async def get_account_summary(self, account: str) -> AccountSummary:
        """
        Get account summary, including balances, positions, pnls, etc.

        Args:
            account: account uuid or name
                Examples: "00000000-0000-0000-0000-000000000000", "STONEX:000000/JDoe"
        """
        grpc_client = await self._core()
        req = AccountSummaryRequest(account=account)
        res = await grpc_client.unary_unary(req)
        return res

    async def get_positions(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> dict[str, Decimal]:
        """
        Get positions for the specified symbols.

        Args:
            symbols: list of symbol strings
        """
        account_summaries = await self.get_account_summaries(
            accounts=accounts, trader=trader
        )
        positions: dict[str, Decimal] = {}
        for summary in account_summaries:
            for symbol, summary in summary.positions.items():
                for pos in summary:
                    positions[symbol] = positions.get(symbol, Decimal(0)) + pos.quantity
        return positions

    async def get_account_summaries(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> list[AccountSummary]:
        """
        Get account summaries for accounts matching the filters.

        Args:
            accounts: list of account uuids or names
            trader: if specified, return summaries for all accounts for this trader

        If both arguments are given, the union of matching accounts are returned.
        """
        grpc_client = await self._core()
        request = AccountSummariesRequest(
            accounts=accounts,
            trader=trader,
        )
        res = await grpc_client.unary_unary(request)
        return res.account_summaries

    async def get_account_history(
        self,
        account: str,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
    ) -> list[AccountSummary]:
        """
        Get historical sequence of account summaries for the given account.
        """
        grpc_client = await self._core()
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

        req = AccountHistoryRequest(
            account=account, from_inclusive=from_inclusive, to_exclusive=to_exclusive
        )
        res = await grpc_client.unary_unary(req)
        return res.history

    # ------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------

    async def get_open_orders(
        self,
        order_ids: Optional[list[OrderId]] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        symbol: Optional[str] = None,
        parent_order_id: Optional[OrderId] = None,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> list[Order]:
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
        grpc_client = await self._core()

        if from_inclusive is not None:
            if not from_inclusive.tzinfo:
                raise ValueError("start time must be timezone-aware")
            from_inclusive = from_inclusive.astimezone(timezone.utc)

        if to_exclusive is not None:
            if not to_exclusive.tzinfo:
                raise ValueError("end time must be timezone-aware")
            to_exclusive = to_exclusive.astimezone(timezone.utc)

        open_orders_request = OpenOrdersRequest(
            venue=venue,
            account=account,
            trader=trader,
            symbol=symbol,
            parent_order_id=parent_order_id,
            order_ids=order_ids,
            from_inclusive=from_inclusive,
            to_exclusive=to_exclusive,
            limit=limit,
        )

        open_orders = await grpc_client.unary_unary(open_orders_request)
        return open_orders.open_orders

    async def get_all_open_orders(self) -> list[Order]:
        """
        @deprecated(reason="Use get_open_orders with no parameters instead")

        Returns a list of all open orders for the authenticated user.
        """
        return await self.get_open_orders()

    async def get_historical_orders(
        self,
        order_ids: Optional[list[OrderId]] = None,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        parent_order_id: Optional[OrderId] = None,
    ) -> list[Order]:
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
        grpc_client = await self._core()

        if from_inclusive is not None:
            if not from_inclusive.tzinfo:
                raise ValueError("start time must be timezone-aware")
            from_inclusive = from_inclusive.astimezone(timezone.utc)

        if to_exclusive is not None:
            if not to_exclusive.tzinfo:
                raise ValueError("end time must be timezone-aware")
            to_exclusive = to_exclusive.astimezone(timezone.utc)

        historical_orders_request = HistoricalOrdersRequest.new(
            order_ids=order_ids,
            venue=venue,
            account=account,
            parent_order_id=parent_order_id,
            from_inclusive=from_inclusive,
            to_exclusive=to_exclusive,
        )
        orders = await grpc_client.unary_unary(historical_orders_request)
        if orders is None:
            raise ValueError(
                "No orders found for the given filters. "
                "If order_ids is not specified, then from_inclusive and to_exclusive "
                "MUST be specified."
            )
        return orders.orders

    async def get_order(self, order_id: OrderId) -> Optional[Order]:
        """
        Returns the specified order.  Useful for looking at past sent orders.
        Queries open_orders first, then queries historical_orders.

        Args:
            order_id: the order id to get
        """
        grpc_client = await self._core()
        req = OpenOrdersRequest.new(
            order_ids=[order_id],
        )
        res = await grpc_client.unary_unary(req)
        for open_order in res.open_orders:
            if open_order.id == order_id:
                return open_order

        req = HistoricalOrdersRequest.new(
            order_ids=[order_id],
        )
        res = await grpc_client.unary_unary(req)
        if res.orders and len(res.orders) == 1:
            return res.orders[0]

    async def get_orders(self, order_ids: list[OrderId]) -> list[Optional[Order]]:
        """
        Returns the specified orders.  Useful for looking at past sent orders.
        Plural form of get_order.

        Args:
            order_ids: a list of order ids to get
        """
        grpc_client = await self._core()
        orders_dict: dict[OrderId, Optional[Order]] = {
            order_id: None for order_id in order_ids
        }
        req = OpenOrdersRequest.new(
            order_ids=order_ids,
        )

        res = await grpc_client.unary_unary(req)
        for open_order in res.open_orders:
            orders_dict[open_order.id] = open_order

        not_open_order_ids = [
            order_id for order_id in order_ids if orders_dict[order_id] is None
        ]

        req = HistoricalOrdersRequest.new(
            order_ids=not_open_order_ids,
        )
        res = await grpc_client.unary_unary(req)
        for historical_order in res.orders:
            orders_dict[historical_order.id] = historical_order

        return [orders_dict[order_id] for order_id in order_ids]

    async def get_fills(
        self,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        order_id: Optional[OrderId] = None,
        limit: Optional[int] = None,
    ) -> HistoricalFillsResponse:
        """
        Returns all fills matching the given filters.

        Args:
            from_inclusive: the start date to get fills for
            to_exclusive: the end date to get fills for
            venue: the venue to get fills for, e.g. "CME"
            account: account uuid or name
            order_id: the order id to get fills for
        """
        grpc_client = await self._core()
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
        req = HistoricalFillsRequest(
            account=account,
            from_inclusive=from_inclusive,
            limit=limit,
            order_id=order_id,
            to_exclusive=to_exclusive,
            venue=venue,
        )
        res = await grpc_client.unary_unary(req)
        return res

    async def orderflow(
        self,
        max_queue_size: int = 1024,
    ) -> OrderflowChannel:
        """
        A two-way channel for both order entry and listening to order updates (fills, acks, outs, etc.).

        This is considered the most efficient way to trade in this SDK.

        This requires advanced knowledge of the SDK and asyncio, not recommended for beginners.
        See the OrderflowManager documentation for more details.
        """
        return OrderflowChannel(self, max_queue_size=max_queue_size)

    async def stream_orderflow(
        self,
        account: Optional[AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        trader: Optional[TraderIdOrEmail] = None,
    ) -> AsyncGenerator[Orderflow, None]:
        """
        A stream for listening to order updates (fills, acks, outs, etc.).

        Example:
            ```python
            async for event in client.stream_orderflow(account, execution_venue, trader):
                print(event)
            ```
        """
        grpc_client = await self._core()
        req: SubscribeOrderflowRequest = SubscribeOrderflowRequest(
            account=account, execution_venue=execution_venue, trader=trader
        )
        async for res in grpc_client.unary_stream(req):  # type: ignore
            yield res

    # ------------------------------------------------------------
    # Order entry
    # ------------------------------------------------------------

    async def send_limit_order(
        self,
        *args,
        **kwargs,
    ) -> Order:
        """
        @deprecated(reason="Use place_order instead")
        """
        logging.warning(
            "send_limit_order is deprecated, use place_order instead. "
            "This will be removed in a future version."
        )
        return await self.place_order(*args, **kwargs)

    async def place_limit_order(
        self,
        *args,
        **kwargs,
    ) -> Order:
        """
        @deprecated(reason="Use place_order instead")
        """
        logging.warning(
            "place_limit_order is deprecated, use place_order instead. "
            "This will be removed in a future version."
        )
        return await self.place_order(*args, **kwargs)

    async def place_orders(
        self, order_requests: Sequence[PlaceOrderRequest]
    ) -> list[Order]:
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
        grpc_client = await self._core()

        res = await asyncio.gather(
            *[
                grpc_client.unary_unary(order_request)
                for order_request in order_requests
            ]
        )

        return res

    async def place_order(
        self,
        *,
        id: Optional[OrderId] = None,
        symbol: TradableProduct | str,
        execution_venue: Optional[str] = None,
        dir: OrderDir,
        quantity: Decimal,
        limit_price: Optional[Decimal] = None,
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TimeInForce = TimeInForce.DAY,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        post_only: Optional[bool] = None,
        trigger_price: Optional[Decimal] = None,
        stop_loss: Optional[TriggerLimitOrderType] = None,
        take_profit_price: Optional[Decimal] = None,
        **kwargs: Any,
    ) -> Order:
        """
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
            trader: the trader to send the order for, defaults to the user's trader
                for when sending order for another user, not relevant for vast majority of users
            post_only: whether the order should be post only, NOT SUPPORTED BY ALL EXCHANGES (e.g. CME)
            trigger_price: the trigger price for the order, only relevant for stop / take_profit orders
            stop_loss_price: the stop loss price for a bracket order.
            profit_price: the take profit price for a bracket order.
        Returns:
            the Order object for the order
            The order.status should  be "PENDING" until the order is "OPEN" / "REJECTED" / "OUT" / "CANCELED" / "STALE"

            If the order is rejected, the order.reject_reason and order.reject_message will be set
        """
        grpc_client = await self._core()
        assert quantity > 0, "quantity must be positive"

        if limit_price is not None and price_round_method is not None:
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
                    f"Could not find execution information for {symbol} for rounding price for limit order. Please round price manually."
                )
            if (tick_size := execution_info.tick_size) is not None:
                if tick_size:
                    limit_price = price_round_method(limit_price, tick_size)
            else:
                raise ValueError(f"Could not find market information for {symbol}")

        req: PlaceOrderRequest = PlaceOrderRequest.new(
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
            stop_loss=stop_loss,
            take_profit_price=take_profit_price,
        )
        res = await grpc_client.unary_unary(req)
        return res

    async def place_batch_order(
        self, batch: BatchPlaceOrder
    ) -> PlaceBatchOrderResponse:
        """
        Place a batch order.
        """
        grpc_client = await self._core()
        req: PlaceBatchOrderRequest = PlaceBatchOrderRequest.new(
            place_orders=batch.place_orders,
        )
        res = await grpc_client.unary_unary(req)
        return res

    async def send_market_pro_order(
        self,
        *,
        id: Optional[OrderId] = None,
        symbol: TradableProduct | str,
        execution_venue: str,
        dir: OrderDir,
        quantity: Decimal,
        time_in_force: TimeInForce = TimeInForce.DAY,
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
        """

        ticker = await self.get_ticker(symbol, execution_venue)
        if ticker is None:
            raise ValueError(
                f"Failed to send market order with reason: no ticker for {symbol}"
            )

        price_band = price_band_pairs.get(symbol, None)

        if dir == OrderDir.BUY:
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
                limit_price = max(limit_price, price_band_reference_price)

        # Conservatively round price to nearest tick
        tick_round_method = (
            TickRoundMethod.FLOOR if dir == OrderDir.BUY else TickRoundMethod.CEIL
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
            dir=dir,
            quantity=quantity,
            account=account,
            order_type=OrderType.LIMIT,
            limit_price=limit_price,
            time_in_force=time_in_force,
        )

    async def cancel_order(self, order_id: OrderId) -> Cancel:
        """
        Cancels an order by order id.

        Args:
            order_id: the order id to cancel
        Returns:
            the CancelFields object
        """
        grpc_client = await self._core()
        req = CancelOrderRequest(id=order_id)
        res = await grpc_client.unary_unary(req)
        return res

    async def cancel_all_orders(
        self,
        account: Optional[AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        trader: Optional[TraderIdOrEmail] = None,
        *,
        synthetic: bool = True,
    ) -> bool:
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
        if synthetic:
            open_orders = await self.get_open_orders(
                account=account,
                venue=execution_venue,
                trader=trader,
            )
            outputs = await asyncio.gather(
                *(self.cancel_order(order.id) for order in open_orders)
            )
            for cancel in outputs:
                if cancel.reject_reason is not None:
                    return False

            return True
        else:
            grpc_client = await self._core()
            req = CancelAllOrdersRequest(
                id=str(uuid.uuid4()),  # Unique ID for the request
                account=account,
                execution_venue=execution_venue,
                trader=trader,
            )
            _res = await grpc_client.unary_unary(req)
            return True

    async def reconcile_out(
        self,
        *,
        order_id: Optional[OrderId] = None,
        order_ids: Optional[list[OrderId]] = None,
    ):
        """
        Manually reconcile orders out.

        Useful for clearing stuck orders or stale orders when a human wants to intervene.
        """
        grpc_client = await self._core()
        req = ReconcileOutRequest(order_id=order_id, order_ids=order_ids)
        await grpc_client.unary_unary(req)

    async def place_algo_order(
        self,
        *,
        params: SpreaderParams,
        id: Optional[str] = None,
        trader: Optional[str] = None,
    ):
        """
        Sends an advanced algo order such as the spreader.
        """
        grpc_client = await self._core()

        if isinstance(params, SpreaderParams):
            algo = "SPREADER"
        else:
            raise ValueError(
                "Unsupported algo type. Only SpreaderParams is supported for now."
            )

        req = CreateAlgoOrderRequest(algo=algo, params=params, id=id, trader=trader)
        res = await grpc_client.unary_unary(req)
        return res
