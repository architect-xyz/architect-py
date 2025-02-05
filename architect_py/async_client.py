"""
This file extends the GraphQLClient class to provide a higher-level interface
for order entry with the Architect API.

These are not required to send orders, but provide typed interfaces for the
various order types and algorithms that can be sent to the OMS.


The functions to send orders will return the order ID string
After sending the order, this string can be used to retrieve the order status

send_limit_order -> get_order
send_twap_algo -> get_twap_status / get_twap_order
send_pov_algo -> get_pov_status / get_pov_order
etc.

get_algo_status / get_algo_order
are the generic functions to get the status of an algo
it may not have all the information that the specific get_algo functions have
"""

import asyncio
import fnmatch
import logging
import re
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, AsyncIterator, Dict, List, Optional, Sequence, Union
from urllib.parse import urlparse
from uuid import UUID

import dns.asyncresolver
import dns.name

import grpc.aio

from architect_py.graphql_client.base_model import UNSET, UnsetType
from architect_py.graphql_client.place_order import PlaceOrderOms
from architect_py.graphql_client.subscribe_trades import SubscribeTradesTrades
from architect_py.scalars import OrderDir
from architect_py.utils.nearest_tick import nearest_tick, TickRoundMethod

from .graphql_client import GraphQLClient
from .graphql_client.enums import (
    OrderType,
    TimeInForce,
)
from .graphql_client.fragments import OrderFields

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
from .json_ws_client import JsonWsClient
from .protocol.marketdata import (
    JsonMarketdataStub,
    L1BookSnapshot,
    ExternalL2BookSnapshot,
    L2BookDiff,
    L2BookSnapshot,
    L2BookSnapshotRequest,
    L2BookUpdate,
    L3BookSnapshot,
    SubscribeL1BookSnapshotsRequest,
    SubscribeL2BookUpdatesRequest,
)
from .protocol.symbology import Market, Product, Route, Venue

from .utils.price_bands import price_band_pairs

logger = logging.getLogger(__name__)


class AsyncClient(GraphQLClient):
    def __init__(
        self,
        no_gql: bool = False,
        **kwargs,
    ):
        """
        Please see the GraphQLClient class for the full list of arguments.

        TODO: make paper trading port change to 6789 automatic
        """
        if kwargs["api_key"] is None:
            raise ValueError("API key is required.")
        elif kwargs["api_secret"] is None:
            raise ValueError("API secret is required.")
        elif not kwargs["api_key"].isalnum():
            raise ValueError(
                "API key must be alphanumeric, please double check your credentials."
            )
        elif "," in kwargs["api_key"] or "," in kwargs["api_secret"]:
            raise ValueError(
                "API key and secret cannot contain commas, please double check your credentials."
            )
        elif " " in kwargs["api_key"] or " " in kwargs["api_secret"]:
            raise ValueError(
                "API key and secret cannot contain spaces, please double check your credentials."
            )
        elif len(kwargs["api_key"]) != 24 or len(kwargs["api_secret"]) != 44:
            raise ValueError(
                "API key and secret are not the correct length, please double check your credentials."
            )

        super().__init__(**kwargs)
        self.no_gql = no_gql
        self.grpc_jwt: Optional[str] = None
        self.grpc_jwt_expiration: Optional[datetime] = None
        self.grpc_root_certificates = b"""
-----BEGIN CERTIFICATE-----
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
H2IV
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
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
/NH29tMBSSc6bhrkTx1vPgu2ZyjMGgpbEw==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIGWDCCBECgAwIBAgIUW1jgElSiP7SDKEaBkxtAHbYpoH0wDQYJKoZIhvcNAQEL
BQAwYzEbMBkGA1UEAwwScm9vdC5hcmNoaXRlY3QueHl6MQswCQYDVQQGEwJVUzER
MA8GA1UECAwISWxsaW5vaXMxEDAOBgNVBAcMB0NoaWNhZ28xEjAQBgNVBAoMCWFy
Y2hpdGVjdDAeFw0yMzA0MDgxOTMxMzRaFw0yNDA0MDcxOTMxMzRaMGExGTAXBgNV
BAMMEGwyLmFyY2hpdGVjdC54eXoxCzAJBgNVBAYTAlVTMREwDwYDVQQIDAhJbGxp
bm9pczEQMA4GA1UEBwwHQ2hpY2FnbzESMBAGA1UECgwJYXJjaGl0ZWN0MIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0Gb0dwwk15NYiQRm/DPgoqx0ru1S
FdFQam0MoL8LMRQriZJKnWj/EQv2kyyEWRhxdQrbjSNI4p6RaLcGBz3fZbDdzffS
JzBHShrItc6c10/kTwHJmCMSTXvH6fi1OY6IzTOU70FiXT4FjWxCK1nbaYq+d8Np
nhhJtFaM0rM4laZZ/EoxQenh3QvxZG0CcAP93rloDid70HgOu2uss3BpAzfMBwtX
PJu6N/XHtf+lX6O349E1FrIAgMdQlNcigH8DzLpfLmZlFynyDHG6TD+67XaS9w3s
AzQXBNcRxIApeB82X8N7LRxf2zlRdxQcZyi+ZkANJRl5g2Zi6QnEiUwvp0hHd7RS
zaIaIfDxUcC9gbrF6Dre3DhxIhcwqLq3yzGXCsd2WOwGX7k/iGotdogaUNwT0OgZ
3POr44hEDXMHbfSnAzHVaauoqDF2SjFwlqIRy4QuBoLgXLQjUZI+wZwwMpN6rDeJ
AnwLWuLmIIE7AoeKCPnbrOoow0QuR+bEaibIus9JyToZ80hIzeb50Kq1ATjTXt2V
ZE9kYBwOtdCKRrEgag08omDzQEQJOGpnd17mzMccfJSU0d2CCNb+MBxEsz1u/yf2
X5Mu5rlMpwhJRtdUeIYD9S7dsh+V/9v5fsBbzL9bOkU3dgE16VTt/A/k4ZZ+V17D
TJa0TzP1l31Sm8ECAwEAAaOCAQQwggEAMBIGA1UdEwEB/wQIMAYBAf8CAQEwHQYD
VR0OBBYEFEiHawfI89zZEHcbZpYjgOumsR5DMIGgBgNVHSMEgZgwgZWAFPactYgo
/THaW4JPMS+/04UvKuDVoWekZTBjMRswGQYDVQQDDBJyb290LmFyY2hpdGVjdC54
eXoxCzAJBgNVBAYTAlVTMREwDwYDVQQIDAhJbGxpbm9pczEQMA4GA1UEBwwHQ2hp
Y2FnbzESMBAGA1UECgwJYXJjaGl0ZWN0ghQc6t2vhCFLPpKo8MUtYKoUCYB6tzAL
BgNVHQ8EBAMCAeYwGwYDVR0RBBQwEoIQbDIuYXJjaGl0ZWN0Lnh5ejANBgkqhkiG
9w0BAQsFAAOCAgEACO4hCEz21SxNBt0lwUMUAIVwmD7H0zERXxmPClJyNiBDLr6N
CoQngMS9pvGoB6b2OFijDCx+/GR4UBzv0PG1x2fGMTjVUAcY8L2/hujWX8IuJN3J
zTq8gGSU/ih1nXGSWNlaqPk942o8Yl/5kbx4i/OhCZbWhAK3ij7xGR0sPNTP4WM7
b+kEf0qAdU/0Rghn4EtG9YKA+GIYcq2wzsyP8hWjJv86alQ1Lqln0uzKz0bt1X7V
nh2bO5PX3h7Jrj5QiETgtUMz4TKiBxGyT9LZfsAuES3JJlfZjwXQA2uLWeqO0i2c
KAO0SNtbc4Vkstme6nHhr9YsZ5X50H/pukbq4L1Aq1AhwrG7lwO9lwu6fskp+gk9
lreA6DrKwx9ZL2QxG8E+vGI5tHAiYj8tep/dGDoL0uNVLeLPVLGEizAZ5oRSofF5
EJWI9wjpxtzpV6HrdzZLjReDn03iy4YsLH7PtoyS4/Kq9tl+12GdYSlwiUfeY7YW
ju7y2BORbiY6Bdf8VSJ54VKpO76WXFzmcsEDQ4PdTKh5B6Vv6mGvyFpWBohPCgG0
wB0pIqDEag2H7dFUtuibRkTPIIvkaohr/q9YGVSSVlUizlWzM8mlDzF7zDSNhEfF
P4NC7VHNfGr8p4Zk29eaRBJy78sqSzkrQpiO4RxMf5r8XTmhjwEjlo0KYjU=
-----END CERTIFICATE-----
"""
        self.marketdata: Dict[str, JsonWsClient] = {}  # cpty => JsonWsClient
        self.route_by_id: Dict[UUID, Route] = {}
        self.venue_by_id: Dict[UUID, Venue] = {}
        self.product_by_id: Dict[UUID, Product] = {}
        self.market_by_id: Dict[UUID, Market] = {}
        # route => venue => base => quote => market
        self.market_names_by_route: dict[str, dict[str, dict[str, dict[str, str]]]] = {}
        self.l2_books: dict[str, L2Book] = {}

    async def grpc_channel(self, endpoint: str):
        if "://" not in endpoint:
            endpoint = f"http://{endpoint}"
        url = urlparse(endpoint)
        if url.hostname is None:
            raise Exception(f"Invalid endpoint: {endpoint}")
        is_https = url.scheme == "https"
        srv_records: list = await dns.asyncresolver.resolve(url.hostname, "SRV")
        if len(srv_records) == 0:
            raise Exception(f"No SRV records found for {url.hostname}")
        connect_str = f"{srv_records[0].target}:{srv_records[0].port}"
        if is_https:
            credentials = grpc.ssl_channel_credentials(
                root_certificates=self.grpc_root_certificates
            )
            options = (("grpc.ssl_target_name_override", "service.architect.xyz"),)
            return grpc.aio.secure_channel(connect_str, credentials, options=options)
        else:
            return grpc.aio.insecure_channel(connect_str)

    async def refresh_grpc_credentials(self, force: bool = False) -> Optional[str]:
        """
        Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
        If force is True, refresh the JWT unconditionally.
        """
        if (
            force
            or self.grpc_jwt is None
            or (
                self.grpc_jwt_expiration is not None
                and datetime.now() > self.grpc_jwt_expiration - timedelta(minutes=1)
            )
        ):
            try:
                self.grpc_jwt = (await self.create_jwt()).create_jwt
                self.grpc_jwt_expiration = datetime.now() + timedelta(
                    hours=23
                )  # TODO: actually inspect the JWT exp
            except Exception as e:
                logger.error("Failed to refresh gRPC credentials: %s", e)

        return self.grpc_jwt

    def configure_marketdata(self, *, cpty: str, url: str):
        self.marketdata[cpty] = JsonWsClient(url=url)

    async def start_session(self):
        await self.load_and_index_symbology()

    async def search_symbols(
        self,
        *,
        execution_venue: str | None | UnsetType = UNSET,
        marketdata_venue: str | None | UnsetType = UNSET,
        underlying: str | None | UnsetType = UNSET,
        max_results: int | None | UnsetType = UNSET,
        results_offset: int | None | UnsetType = UNSET,
        search_string: str | None | UnsetType = UNSET,
        sort_by_volume_desc: bool | None | UnsetType = UNSET,
        glob: str | None = None,
        regex: str | None = None,
        **kwargs: Any,
    ) -> List[str]:

        if glob or regex:
            markets = (
                await self.search_symbols_request(
                    (
                        sort_by_volume_desc
                        if isinstance(sort_by_volume_desc, bool)
                        else False
                    ),
                    search_string,
                    execution_venue,
                    marketdata_venue,
                    underlying,
                    UNSET,
                    results_offset,
                )
            ).search_symbols

            if glob is not None:
                markets = [
                    market for market in markets if fnmatch.fnmatch(market, glob)
                ]

            if regex is not None:
                markets = [market for market in markets if re.match(regex, market)]

            if isinstance(max_results, int):
                markets = markets[:max_results]

        else:
            markets = (
                await self.search_symbols_request(
                    (
                        sort_by_volume_desc
                        if isinstance(sort_by_volume_desc, bool)
                        else False
                    ),
                    search_string,
                    execution_venue,
                    marketdata_venue,
                    underlying,
                    max_results,
                    results_offset,
                )
            ).search_symbols

        return markets

    async def load_and_index_symbology(self, cpty: Optional[str] = None):
        # TODO: consider locking
        self.route_by_id = {}
        self.venue_by_id = {}
        self.product_by_id = {}
        self.market_by_id = {}
        self.market_names_by_route = {}
        if not self.no_gql:
            logger.info("Loading symbology...")
            symbols = await self.search_symbols()
            logger.info("Loaded %d markets", len(symbols))
            for symbol in symbols:
                market = self.get_product_info(symbol)

                if market.route.name not in self.market_names_by_route:
                    self.market_names_by_route[market.route.name] = {}
                by_venue = self.market_names_by_route[market.route.name]
                if market.venue.name not in by_venue:
                    by_venue[market.venue.name] = {}
                by_base = by_venue[market.venue.name]

                if isinstance(market.kind, MarketFieldsKindExchangeMarketKind):
                    if market.kind.base.name not in by_base:
                        by_base[market.kind.base.name] = {}
                    by_quote = by_base[market.kind.base.name]
                    by_quote[market.kind.quote.name] = market.name
            logger.info("Indexed %d markets", len(markets))
        # get symbology from marketdata clients
        clients: list[JsonWsClient] = []
        if cpty is None:
            clients = list(self.marketdata.values())
        elif cpty in self.marketdata:
            clients = [self.marketdata[cpty]]
        for client in clients:
            snap = await client.get_symbology_snapshot()
            for route in snap.routes:
                self.route_by_id[route.id] = route
            for venue in snap.venues:
                self.venue_by_id[venue.id] = venue
            for product in snap.products:
                self.product_by_id[product.id] = product
            for snap_market in snap.markets:
                self.market_by_id[snap_market.id] = snap_market
                route = self.route_by_id[snap_market.route]
                if route.name not in self.market_names_by_route:
                    self.market_names_by_route[route.name] = {}
                by_venue = self.market_names_by_route[route.name]
                venue = self.venue_by_id[snap_market.venue]
                if venue.name not in by_venue:
                    by_venue[venue.name] = {}
                by_base = by_venue[venue.name]
                base = self.product_by_id[snap_market.base()]
                if base.name not in by_base:
                    by_base[base.name] = {}
                by_quote = by_base[base.name]
                quote = self.product_by_id[snap_market.quote()]
                by_quote[quote.name] = snap_market.name

    # CR alee: make base, venue, route optional, and add optional quote.
    # Have to think harder about efficient indexing.
    def find_markets(
        self,
        base: str,
        venue: str,
        route: str = "DIRECT",
    ) -> list[str]:
        """
        Lookup all markets matching the given criteria.  Requires the client to be initialized
        and symbology to be loaded and indexed.
        """
        if route not in self.market_names_by_route:
            return []
        by_venue = self.market_names_by_route[route]
        if venue not in by_venue:
            return []
        by_base = by_venue[venue]
        if not by_base:
            return []
        by_quote = by_base.get(base, {})
        return list(by_quote.values())

    async def subscribe_l1_book_snapshots(
        self, endpoint: str, market_ids: list[str] | None = None
    ) -> AsyncIterator[L1BookSnapshot]:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = SubscribeL1BookSnapshotsRequest(market_ids=market_ids)
        return stub.SubscribeL1BookSnapshots(req)

    async def l2_book_snapshot(self, endpoint: str, market_id: str) -> L2BookSnapshot:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = L2BookSnapshotRequest(market_id=market_id)
        jwt = await self.refresh_grpc_credentials()
        # TODO: use secure channel or force allow auth header over insecure channel
        # credentials = None if jwt is None else grpc.access_token_call_credentials(jwt)
        return await stub.L2BookSnapshot(
            req, metadata=(("authorization", f"Bearer {jwt}"),)
        )

    async def subscribe_l2_book_updates(
        self, endpoint: str, market_id: str
    ) -> AsyncIterator[L2BookUpdate]:
        channel = await self.grpc_channel(endpoint)
        stub = JsonMarketdataStub(channel)
        req = SubscribeL2BookUpdatesRequest(market_id=market_id)
        jwt = await self.refresh_grpc_credentials()
        return stub.SubscribeL2BookUpdates(
            req, metadata=(("authorization", f"Bearer {jwt}"),)
        )

    async def watch_l2_book(
        self, endpoint: str, market_id: str
    ) -> AsyncIterator[tuple[int, int]]:
        async for up in await self.subscribe_l2_book_updates(endpoint, market_id):
            if isinstance(up, L2BookSnapshot):
                self.l2_books[market_id] = L2Book(up)
            elif isinstance(up, L2BookDiff):
                if market_id not in self.l2_books:
                    raise ValueError(
                        f"received update before snapshot for L2 book {market_id}"
                    )
                book = self.l2_books[market_id]
                if (
                    up.sequence_id != book.sequence_id
                    or up.sequence_number != book.sequence_number + 1
                ):
                    raise ValueError(
                        f"received update out of order for L2 book {market_id}"
                    )
                book.update_from_diff(up)

            yield (up.sequence_id, up.sequence_number)

    async def get_external_l2_book_snapshot(
        self, market: str
    ) -> ExternalL2BookSnapshot:
        [_, cpty] = market.split("*", 1)
        if cpty in self.marketdata:
            client = self.marketdata[cpty]
            market_id = Market.derive_id(market)
            return await client.get_l2_book_snapshot(market_id)
        else:
            raise ValueError(f"cpty {cpty} not configured for L2 marketdata")

    async def get_l3_book_snapshot(self, market: str) -> L3BookSnapshot:
        [_, cpty] = market.split("*", 1)
        if cpty in self.marketdata:
            client = self.marketdata[cpty]
            market_id = Market.derive_id(market)
            return await client.get_l3_book_snapshot(market_id)
        else:
            raise ValueError(f"cpty {cpty} not configured for L3 marketdata")

    def subscribe_trades(
        self, market: str, *args, **kwargs
    ) -> AsyncIterator[SubscribeTradesTrades]:
        [_, cpty] = market.split("*", 1)
        if cpty in self.marketdata:
            client = self.marketdata[cpty]
            market_id = Market.derive_id(market)
            return client.subscribe_trades(market_id)
        elif not self.no_gql:
            return super().subscribe_trades(market, *args, **kwargs)
        else:
            raise ValueError(
                f"cpty {cpty} not configured for marketdata and no GQL server"
            )

    async def send_limit_order(
        self,
        *,
        symbol: str,
        odir: OrderDir,
        quantity: Decimal,
        limit_price: Decimal,
        order_type: OrderType = OrderType.LIMIT,
        post_only: bool = False,
        trigger_price: Optional[Decimal] = None,
        time_in_force: TimeInForce = TimeInForce.DAY,
        good_til_date: Optional[datetime] = None,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        execution_venue: Optional[str] = None,
    ) -> OrderFields:
        """
        `account` is optional depending on the final cpty it gets to
        For CME orders, the account is required
        """

        if price_round_method is not None:
            execution_info = await self.get_execution_info(symbol, execution_venue)
            if (tick_size := execution_info.execution_info.tick_size) is not None:
                if tick_size:
                    limit_price = nearest_tick(
                        limit_price, method=price_round_method, tick_size=tick_size
                    )
            else:
                raise ValueError(f"Could not find market information for {symbol}")

        if not isinstance(trigger_price, Decimal) and trigger_price is not None:
            trigger_price = Decimal(trigger_price)

        order: PlaceOrderOms = await self.place_order(
            symbol,
            odir,
            quantity,
            order_type,
            time_in_force,
            None,
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
        symbol: str,
        marketdata_venue: Optional[str] = None,
        odir: OrderDir,
        quantity: Decimal,
        time_in_force: TimeInForce = TimeInForce.DAY,
        account: Optional[str] = None,
        fraction_through_market: Decimal = Decimal("0.001"),
    ) -> OrderFields:

        product_info = await self.get_product_info(symbol)
        if product_info is None:
            raise ValueError(
                f"Failed to send market order with reason: no market details for {symbol}"
            )

        # Check for GQL failures
        bbo_snapshot = await self.get_market_snapshot(marketdata_venue, symbol)
        bbo_snapshot = bbo_snapshot.ticker
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
            execution_venue=marketdata_venue, symbol=symbol
        )

        if (
            execution_info.execution_info is not None
            and (tick_size := execution_info.execution_info.tick_size) is not None
        ):
            limit_price = nearest_tick(
                Decimal(limit_price),
                tick_round_method,
                tick_size=tick_size,
            )

        return await self.send_limit_order(
            symbol=symbol,
            odir=odir,
            quantity=quantity,
            account=account,
            order_type=OrderType.LIMIT,
            limit_price=limit_price,
            time_in_force=time_in_force,
        )

    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date:
        _, d, *_ = name.split(" ")
        return datetime.strptime(d, "%Y%m%d").date()

    async def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]:
        markets = await self.future_series(
            series,
        )

        filtered_markets = [
            (self.get_expiration_from_CME_name(market), market)
            for market in markets.futures_series
        ]

        filtered_markets.sort(key=lambda x: x[0])

        return filtered_markets

    async def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> str:
        [market] = [
            market
            for market in await self.search_symbols(
                regex=f"^{root} {year}{month:02d}",
                venue="CME",
            )
        ]

        return market

    async def get_cme_first_notice_date(self, market: str) -> Optional[date]:
        notice = await self.get_first_notice_date(market)
        if notice is None or notice.product_info is None:
            return None
        return notice.product_info.first_notice_date


# TODO: move this somewhere else
class L2Book:
    timestamp_s: int
    timestamp_ns: int
    sequence_id: int
    sequence_number: int
    bids: dict[Decimal, Decimal]
    asks: dict[Decimal, Decimal]

    def __init__(self, snapshot: L2BookSnapshot):
        self.timestamp_s = snapshot.timestamp_s
        self.timestamp_ns = snapshot.timestamp_ns
        self.sequence_id = snapshot.sequence_id
        self.sequence_number = snapshot.sequence_number
        self.bids = {}
        self.asks = {}
        for price, size in snapshot.bids:
            self.bids[price] = size
        for price, size in snapshot.asks:
            self.asks[price] = size

    def update_from_diff(self, diff: L2BookDiff):
        self.timestamp_s = diff.timestamp_s
        self.timestamp_ns = diff.timestamp_ns
        self.sequence_id = diff.sequence_id
        self.sequence_number = diff.sequence_number
        for price, size in diff.bids:
            if size.is_zero():
                if price in self.bids:
                    del self.bids[price]
            else:
                self.bids[price] = size
        for price, size in diff.asks:
            if size.is_zero():
                if price in self.asks:
                    del self.asks[price]
            else:
                self.asks[price] = size

    def timestamp(self):
        dt = datetime.fromtimestamp(self.timestamp_s)
        return dt.replace(microsecond=self.timestamp_ns // 1000)

    def snapshot(self) -> L2BookSnapshot:
        return L2BookSnapshot(
            timestamp_s=self.timestamp_s,
            timestamp_ns=self.timestamp_ns,
            sequence_id=self.sequence_id,
            sequence_number=self.sequence_number,
            bids=list(self.bids.items()),
            asks=list(self.asks.items()),
        )
