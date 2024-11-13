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

import fnmatch
from functools import lru_cache
import logging
import re
import dns.asyncresolver
import dns.name
import grpc.aio
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, AsyncIterator, List, Optional, Sequence, TypeAlias, Union

import grpc.aio

from architect_py.async_graphql_client.base_model import UNSET, UnsetType
from architect_py.async_graphql_client.get_market import GetMarketMarket
from architect_py.async_graphql_client.subscribe_trades import SubscribeTradesTrades
from architect_py.async_graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.scalars import Dir
from architect_py.utils.balance_and_positions import (
    Balance,
    BalancesAndPositions,
    SimplePosition,
)
from architect_py.utils.dt import (
    convert_datetime_to_utc_str,
    get_expiration_from_CME_name,
)
from architect_py.utils.nearest_tick import TickRoundMethod, nearest_tick

from .async_graphql_client import AsyncGraphQLClient
from .async_graphql_client.enums import (
    CreateOrderType,
    OrderSource,
    ReferencePrice,
)
from .async_graphql_client.fragments import (
    MarketFieldsKindExchangeMarketKind,
    OrderFields,
)
from .async_graphql_client.get_order import GetOrderOrder
from .async_graphql_client.input_types import (
    CreateMMAlgo,
    CreateOrder,
    CreatePovAlgo,
    CreateSmartOrderRouterAlgo,
    CreateSpreadAlgo,
    CreateSpreadAlgoHedgeMarket,
    CreateTimeInForce,
    CreateTimeInForceInstruction,
    CreateTwapAlgo,
)
from .json_ws_client import JsonWsClient
from .protocol.marketdata import (
    JsonMarketdataStub,
    L1BookSnapshot,
    L2BookSnapshot,
    L3BookSnapshot,
    SubscribeL1BookSnapshotsRequest,
)
from .protocol.symbology import Market

logger = logging.getLogger(__name__)


class AsyncClient(AsyncGraphQLClient):
    def __init__(self, no_gql: bool = False, **kwargs):
        """
        Please see the AsyncGraphQLClient class for the full list of arguments.
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
                "API key and secret cannot contain commas, please double check your credentials"
            )
        elif kwargs["api_secret"][-1] != "=":
            raise ValueError(
                "API key and secret cannot contain spaces, please double check your credentials."
            )
        elif len(kwargs["api_key"]) != 24 or len(kwargs["api_secret"]) != 44:
            raise ValueError(
                "API key and secret are not the correct length, please double check your credentials."
            )

        super().__init__(**kwargs)
        self.no_gql = no_gql
        self.marketdata = {}  # cpty => JsonWsClient
        self.route_by_id = {}
        self.venue_by_id = {}
        self.product_by_id = {}
        self.market_by_id = {}
        self.market_names_by_route = {}  # route => venue => base => quote => market

    async def grpc_channel(self, endpoint: Union[dns.name.Name, str]):
        srv_records = await dns.asyncresolver.resolve(endpoint, "SRV")
        if len(srv_records) == 0:
            raise Exception(f"No SRV records found for {endpoint}")
        connect_str = f"{srv_records[0].target}:{srv_records[0].port}"  # type: ignore
        return grpc.aio.insecure_channel(connect_str)

    def configure_marketdata(self, *, cpty, url):
        self.marketdata[cpty] = JsonWsClient(url=url)

    async def start_session(self):
        await self.load_and_index_symbology()

    async def get_market(self, id: str, **kwargs: Any) -> Optional[GetMarketMarket]:
        return await self._get_cached_market(id, **kwargs)

    @lru_cache(maxsize=10)
    async def _get_cached_market(
        self, id: str, **kwargs: Any
    ) -> Optional[GetMarketMarket]:
        return await super().get_market(id, **kwargs)

    async def search_markets(
        self,
        venue: str | None | UnsetType = UNSET,
        base: str | None | UnsetType = UNSET,
        quote: str | None | UnsetType = UNSET,
        underlying: str | None | UnsetType = UNSET,
        max_results: int | None | UnsetType = UNSET,
        results_offset: int | None | UnsetType = UNSET,
        search_string: str | None | UnsetType = UNSET,
        only_favorites: bool | None | UnsetType = UNSET,
        sort_by_volume_desc: bool | None | UnsetType = UNSET,
        glob: str | None = None,
        regex: str | None = None,
        **kwargs: Any,
    ) -> List[SearchMarketsFilterMarkets]:
        markets = await super().search_markets(
            venue,
            base,
            quote,
            underlying,
            max_results,
            results_offset,
            search_string,
            only_favorites,
            sort_by_volume_desc,
            **kwargs,
        )

        if glob is not None:
            markets = [
                market for market in markets if fnmatch.fnmatch(market.name, glob)
            ]

        if regex is not None:
            markets = [market for market in markets if re.match(regex, market.name)]

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
            markets = await self.search_markets()
            logger.info("Loaded %d markets", len(markets))
            for market in markets:
                if market.route.name not in self.market_names_by_route:
                    self.market_names_by_route[market.route.name] = {}
                by_venue = self.market_names_by_route[market.route.name]
                if market.venue.name not in by_venue:
                    by_venue[market.venue.name] = {}
                by_base = by_venue[market.venue.name]

                if market.kind is MarketFieldsKindExchangeMarketKind:
                    if market.kind.base.name not in by_base:
                        by_base[market.kind.base.name] = {}
                    by_quote = by_base[market.kind.base.name]
                    by_quote[market.kind.quote.name] = market.name
            logger.info("Indexed %d markets", len(markets))
        # get symbology from marketdata clients
        clients = []
        if cpty is None:
            clients = self.marketdata.values()
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
            for market in snap.markets:
                self.market_by_id[market.id] = market
                route = self.route_by_id[market.route]
                if route.name not in self.market_names_by_route:
                    self.market_names_by_route[route.name] = {}
                by_venue = self.market_names_by_route[route.name]
                venue = self.venue_by_id[market.venue]
                if venue.name not in by_venue:
                    by_venue[venue.name] = {}
                by_base = by_venue[venue.name]
                base = self.product_by_id[market.base()]
                if base.name not in by_base:
                    by_base[base.name] = {}
                by_quote = by_base[base.name]
                quote = self.product_by_id[market.quote()]
                by_quote[quote.name] = market.name

    # CR alee: make base, venue, route optional, and add optional quote.
    # Have to think harder about efficient indexing.
    def find_markets(
        self,
        base: str,
        venue: str,
        route: str = "DIRECT",
    ) -> list:
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
        return stub.SubscribeL1BookSnapshots(req)  # type: ignore

    async def get_l2_book_snapshot(self, market: str) -> L2BookSnapshot:
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

    async def get_open_orders(
        self,
        venue: Optional[str] = None,
        route: Optional[str] = None,
        cpty: Optional[str] = None,
    ):
        """
        Get open orders known to the OMS.  Optionally filter by specific venue (e.g. "COINBASE")
        or counterparty (e.g. "COINBASE/DIRECT").
        """
        cpty_venue = None
        cpty_route = None
        if cpty:
            cpty_venue, cpty_route = cpty.split("/", 1)
        open_orders = await self.get_all_open_orders()
        filtered_orders = []
        for oo in open_orders:
            if venue and oo.order.market.venue.name != venue:
                continue
            if route and oo.order.market.route.name != route:
                continue
            if cpty_venue and oo.order.market.venue.name != cpty_venue:
                continue
            if cpty_route and oo.order.market.route.name != cpty_route:
                continue
            filtered_orders.append(oo)
        return filtered_orders

    async def send_limit_order(
        self,
        *,
        market: str,
        dir: Dir,
        quantity: Decimal,
        limit_price: Decimal,
        order_type: CreateOrderType = CreateOrderType.LIMIT,
        post_only: bool = False,
        trigger_price: Optional[DecimalLike] = None,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC,
        price_round_method: Optional[TickRoundMethod] = None,
        good_til_date: Optional[datetime] = None,
        account: Optional[str] = None,
        quote_id: Optional[str] = None,
        source: OrderSource = OrderSource.API,
    ) -> Optional[GetOrderOrder]:
        """
        `account` is optional depending on the final cpty it gets to
        For CME orders, the account is required
        """
        if good_til_date is not None:
            good_til_date_str = convert_datetime_to_utc_str(good_til_date)
        else:
            good_til_date_str = None

        if not isinstance(limit_price, Decimal):
            limit_price = Decimal(limit_price)

        if price_round_method is not None:
            market_info = await self.get_market(market)
            if market_info is not None:
                tick_size = Decimal(market_info.tick_size)
                limit_price = nearest_tick(
                    limit_price, method=price_round_method, tick_size=tick_size
                )
            else:
                raise ValueError(f"Could not find market information for {market}")

        if not isinstance(trigger_price, Decimal) and trigger_price is not None:
            trigger_price = Decimal(trigger_price)

        order: str = await self.send_order(
            CreateOrder(
                market=market,
                dir=dir,
                quantity=quantity,
                account=account,
                orderType=order_type,
                limitPrice=limit_price,
                postOnly=post_only,
                triggerPrice=str(trigger_price) if trigger_price is not None else None,
                timeInForce=CreateTimeInForce(
                    instruction=time_in_force_instruction,
                    goodTilDate=good_til_date_str,
                ),
                quoteId=quote_id,
                source=source,
            )
        )

        return await self.get_order(order)

    async def send_twap_algo(
        self,
        *,
        name: str,
        market: str,
        dir: Dir,
        quantity: Decimal,
        interval_ms: int,
        reject_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[Decimal] = None,
    ) -> str:

        end_time_str = convert_datetime_to_utc_str(end_time)
        return await self.send_twap_algo_request(
            CreateTwapAlgo(
                name=name,
                market=market,
                dir=dir,
                quantity=quantity,
                intervalMs=interval_ms,
                rejectLockoutMs=reject_lockout_ms,
                endTime=end_time_str,
                account=account,
                takeThroughFrac=take_through_frac,
            )
        )

    async def send_pov_algo(
        self,
        *,
        name: str,
        market: str,
        dir: Dir,
        target_volume_frac: Decimal,
        min_order_quantity: Decimal,
        max_quantity: Decimal,
        order_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[Decimal] = None,
    ) -> str:
        end_time_str = convert_datetime_to_utc_str(end_time)
        return await self.send_pov_algo_request(
            CreatePovAlgo(
                name=name,
                market=market,
                dir=dir,
                targetVolumeFrac=target_volume_frac,
                minOrderQuantity=min_order_quantity,
                maxQuantity=max_quantity,
                orderLockoutMs=order_lockout_ms,
                endTime=end_time_str,
                account=account,
                takeThroughFrac=(
                    str(take_through_frac) if take_through_frac is not None else None
                ),
            )
        )

    async def send_smart_order_router_algo(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: Dir,
        limit_price: Decimal,
        target_size: Decimal,
        execution_time_limit_ms: int,
    ) -> str:
        return await self.send_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=dir,
                limitPrice=limit_price,
                targetSize=target_size,
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

    async def preview_smart_order_router(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: Dir,
        limit_price: Decimal,
        target_size: Decimal,
        execution_time_limit_ms: int,
    ) -> Optional[Sequence[OrderFields]]:
        algo = await self.preview_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=dir,
                limitPrice=limit_price,
                targetSize=target_size,
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

        if algo:
            return algo.orders
        else:
            return None

    async def send_mm_algo(
        self,
        *,
        name: str,
        market: str,
        account: Optional[str] = None,
        buy_quantity: Decimal,
        sell_quantity: Decimal,
        min_position: Decimal,
        max_position: Decimal,
        max_improve_bbo: Decimal,
        position_tilt: Decimal,
        reference_price: ReferencePrice,
        ref_dist_frac: DecimalLike,
        tolerance_frac: DecimalLike,
        fill_lockout_ms: int,
        order_lockout_ms: int,
        reject_lockout_ms: int,
    ):
        return await self.send_mm_algo_request(
            CreateMMAlgo(
                name=name,
                market=market,
                account=account,
                buyQuantity=buy_quantity,
                sellQuantity=sell_quantity,
                minPosition=min_position,
                maxPosition=max_position,
                maxImproveBbo=max_improve_bbo,
                positionTilt=position_tilt,
                referencePrice=reference_price,
                refDistFrac=ref_dist_frac,
                toleranceFrac=tolerance_frac,
                fillLockoutMs=fill_lockout_ms,
                orderLockoutMs=order_lockout_ms,
                rejectLockoutMs=reject_lockout_ms,
            )
        )

    async def send_spread_algo(
        self,
        *,
        name: str,
        market: str,
        buy_quantity: DecimalLike,
        sell_quantity: DecimalLike,
        min_position: DecimalLike,
        max_position: DecimalLike,
        max_improve_bbo: DecimalLike,
        position_tilt: DecimalLike,
        reference_price: ReferencePrice,
        ref_dist_frac: DecimalLike,
        tolerance_frac: DecimalLike,
        hedge_market: CreateSpreadAlgoHedgeMarket,
        fill_lockout_ms: int,
        order_lockout_ms: int,
        reject_lockout_ms: int,
        account: Optional[str] = None,
    ) -> str:
        return await self.send_spread_algo_request(
            CreateSpreadAlgo(
                name=name,
                market=market,
                account=account,
                buyQuantity=buy_quantity,
                sellQuantity=sell_quantity,
                minPosition=min_position,
                maxPosition=max_position,
                maxImproveBbo=max_improve_bbo,
                positionTilt=position_tilt,
                referencePrice=reference_price,
                refDistFrac=ref_dist_frac,
                toleranceFrac=tolerance_frac,
                hedgeMarket=hedge_market,
                fillLockoutMs=fill_lockout_ms,
                orderLockoutMs=order_lockout_ms,
                rejectLockoutMs=reject_lockout_ms,
            )
        )

    async def get_cme_futures_series(
        self, series: str
    ) -> list[tuple[date, SearchMarketsFilterMarkets]]:
        markets = await self.search_markets(
            search_string=series,
            venue="CME",
        )

        filtered_markets = [
            (get_expiration_from_CME_name(market.kind.base.name), market)
            for market in markets
            if isinstance(market.kind, MarketFieldsKindExchangeMarketKind)
            and market.kind.base.name.startswith(series)
        ]

        filtered_markets.sort(key=lambda x: x[0])

        return filtered_markets

    async def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> SearchMarketsFilterMarkets:

        [market] = [
            market
            for market in await self.search_markets(
                search_string=f"^{root} {year}{month}",
                venue="CME",
            )
            if isinstance(market.kind, MarketFieldsKindExchangeMarketKind)
            and market.kind.base.name.startswith(root)
        ]

        return market

    async def get_balances_and_positions(self) -> list["BalancesAndPositions"]:
        # returns data in the shape account => venue => { usd_balance: xxx, ...usd margin info, then product: balance, etc. }
        summaries = await self.get_account_summaries()

        bps = []

        for summary in summaries:
            for account in summary.by_account:
                if account.account is None:
                    continue
                name = account.account.name

                usd = None
                for balance in account.balances:
                    if balance.product is None:
                        continue
                    if balance.product.name == "USD":
                        usd_amount = Decimal(balance.amount) if balance.amount else None
                        total_margin = (
                            Decimal(balance.total_margin)
                            if balance.total_margin
                            else None
                        )
                        position_margin = (
                            Decimal(balance.position_margin)
                            if balance.position_margin
                            else None
                        )
                        purchasing_power = (
                            Decimal(balance.purchasing_power)
                            if balance.purchasing_power
                            else None
                        )
                        cash_excess = (
                            Decimal(balance.cash_excess)
                            if balance.cash_excess
                            else None
                        )
                        yesterday_balance = (
                            Decimal(balance.yesterday_balance)
                            if balance.yesterday_balance
                            else None
                        )

                        usd = Balance(
                            usd_amount,
                            total_margin,
                            position_margin,
                            purchasing_power,
                            cash_excess,
                            yesterday_balance,
                        )

                if usd is None:
                    raise ValueError(f"Account {name} has no USD balance")

                positions = {}
                for position in account.positions:
                    if position.market is None:
                        continue

                    quantity = Decimal(position.quantity) if position.quantity else None
                    if quantity:
                        quantity = quantity if position.dir == "buy" else -quantity
                    average_price = (
                        position.average_price if position.average_price else None
                    )

                    if isinstance(
                        position.market.kind, MarketFieldsKindExchangeMarketKind
                    ):
                        if position.market.kind.base.mark_usd is None:
                            mark = None
                        else:
                            try:
                                mark = Decimal(position.market.kind.base.mark_usd)
                            except Exception:
                                mark = None
                    else:
                        mark = None

                    positions[position.market.name] = SimplePosition(
                        quantity, average_price, mark
                    )

                bps.append(
                    BalancesAndPositions(
                        name,
                        usd_balance=usd,
                        positions=positions,
                    )
                )
        return bps

    async def get_cme_first_notice_date(self, market: str) -> Optional[date]:
        notice = await self.get_first_notice_date(market)
        if notice is None or notice.first_notice_date is None:
            return None

        return datetime.strptime(notice.first_notice_date[:10], "%Y-%m-%d").date()
