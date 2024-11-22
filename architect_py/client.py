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
import dns.resolver
import grpc
from datetime import date, datetime
from decimal import Decimal
import time
from typing import Any, List, Optional, Sequence, TypeAlias, Union

from architect_py.graphql_client.base_model import UNSET, UnsetType
from architect_py.graphql_client.get_market import GetMarketMarket
from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.scalars import OrderDir
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
from .graphql_client import GraphQLClient
from .graphql_client.enums import (
    CreateOrderType,
    OrderSource,
    ReferencePrice,
)
from .graphql_client.fragments import (
    MarketFields,
    MarketFieldsKindExchangeMarketKind,
    MarketFieldsKindExchangeMarketKindBase,
    OrderFields,
)
from .graphql_client.get_order import GetOrderOrder
from .graphql_client.input_types import (
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

logger = logging.getLogger(__name__)


class Client(GraphQLClient):
    def __init__(self, no_gql: bool = False, **kwargs):
        """
        Please see the GraphQLClient class for the full list of arguments.
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
                "API key and secret cannot contain spaces, please double check your credentials"
            )
        elif len(kwargs["api_key"]) != 24 or len(kwargs["api_secret"]) != 44:
            raise ValueError(
                "API key and secret are not the correct length, please double check your credentials."
            )

        super().__init__(**kwargs)
        self.no_gql = no_gql
        self.route_by_id = {}
        self.venue_by_id = {}
        self.product_by_id = {}
        self.market_by_id = {}
        self.market_names_by_route = {}  # route => venue => base => quote => market

    def grpc_channel(self, endpoint: Any):
        srv_records = dns.resolver.resolve(endpoint, "SRV")
        if len(srv_records) == 0:
            raise ValueError(f"No SRV records found for {endpoint}")
        connect_str = f"{srv_records[0].target}:{srv_records[0].port}"  # type: ignore
        return grpc.insecure_channel(connect_str)

    def start_session(self):
        self.load_and_index_symbology()

    def get_market(self, id: str, **kwargs: Any) -> Optional[GetMarketMarket]:
        return self._get_cached_market(id, **kwargs)

    @lru_cache(maxsize=10)
    def _get_cached_market(self, id: str, **kwargs: Any) -> Optional[GetMarketMarket]:
        return super().get_market(id, **kwargs)

    def search_markets(
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
        markets = super().search_markets(
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

    def load_and_index_symbology(self, cpty: Optional[str] = None):
        self.route_by_id = {}
        self.venue_by_id = {}
        self.product_by_id = {}
        self.market_by_id = {}
        self.market_names_by_route = {}
        if not self.no_gql:
            logger.info("Loading symbology...")
            markets = self.search_markets()
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

    def get_open_orders(
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
        open_orders = self.get_all_open_orders()
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

    def send_limit_order(
        self,
        *,
        market: str,
        odir: OrderDir,
        quantity: Decimal,
        order_type: CreateOrderType = CreateOrderType.LIMIT,
        limit_price: Decimal,
        post_only: bool = False,
        trigger_price: Optional[Decimal] = None,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC,
        good_til_date: Optional[datetime] = None,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        quote_id: Optional[str] = None,
        source: OrderSource = OrderSource.API,
        wait_for_confirm: bool = False,
    ) -> Optional[GetOrderOrder]:
        """
        `account` is optional depending on the final cpty it gets to
        For CME orders, the account is required
        """

        if price_round_method is not None:
            market_info = self.get_market(market)
            if market_info is not None:
                limit_price = nearest_tick(
                    limit_price,
                    method=price_round_method,
                    tick_size=market_info.tick_size,
                )
            else:
                raise ValueError(f"Could not find market information for {market}")

        order: str = self.send_order(
            CreateOrder(
                market=market,
                dir=odir,
                quantity=quantity,
                account=account,
                orderType=order_type,
                limitPrice=limit_price,
                postOnly=post_only,
                triggerPrice=trigger_price,
                timeInForce=CreateTimeInForce(
                    instruction=time_in_force_instruction,
                    goodTilDate=good_til_date,
                ),
                quoteId=quote_id,
                source=source,
            )
        )

        if wait_for_confirm:
            i = 0
            while i < 30:
                order_info = self.get_order(order_id=order)
                if order_info is None:
                    return None
                else:
                    if len(order_info.order_state) > 1:
                        return order_info
                    elif order_info.order_state[0] != "OPEN":
                        return order_info
                    else:
                        i += 1
                time.sleep(0.1)
        return self.get_order(order_id=order)

    def send_market_pro_order(
        self,
        *,
        market: str,
        odir: OrderDir,
        quantity: Decimal,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.DAY,
        account: Optional[str] = None,
        source: OrderSource = OrderSource.API,
        percent_through_market: Decimal = Decimal(0.02),
    ) -> Optional[GetOrderOrder]:

        # Check for GQL failures
        bbo_snapshot = self.get_market_snapshot(market)
        if bbo_snapshot is None:
            raise ValueError(
                "Failed to send market order with reason: no market snapshot for {market}"
            )

        market_details = self.get_market(market)
        if market_details is None:
            raise ValueError(
                "Failed to send market order with reason: no market details for {market}"
            )

        best_bid = float(bbo_snapshot.bid_price)
        best_ask = float(bbo_snapshot.ask_price)
        last_price = float(bbo_snapshot.last_price)

        limit_price = (
            best_ask * (1 + percent_through_market)
            if odir == OrderDir.BUY
            else best_bid * (1 - percent_through_market)
        )

        # Avoid sending price outside CME's price bands
        if market_details.venue.name == "CME":
            price_band = market_details.cme_product_group_info.price_band
            if price_band is None:
                raise ValueError(
                    "Failed to send market order with reason: no CME price band for {market}"
                )
            else:
                price_band = float(price_band)

            if odir == OrderDir.BUY:
                limit_price = min(limit_price, last_price + price_band)
            else:
                limit_price = max(limit_price, last_price - price_band)

        # Conservatively round price to nearest tick
        tick_round_method = (
            TickRoundMethod.FLOOR if odir == OrderDir.BUY else TickRoundMethod.CEIL
        )
        limit_price = nearest_tick(
            Decimal(limit_price), tick_round_method, Decimal(market_details.tick_size)
        )

        return self.send_limit_order(
            market=market,
            odir=odir,
            quantity=str(quantity),
            account=account,
            order_type=CreateOrderType.LIMIT,
            limit_price=str(limit_price),
            time_in_force_instruction=time_in_force_instruction,
            source=source,
        )

    def send_twap_algo(
        self,
        *,
        name: str,
        market: str,
        odir: OrderDir,
        quantity: Decimal,
        interval_ms: int,
        reject_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[Decimal] = None,
    ) -> str:

        end_time_str = convert_datetime_to_utc_str(end_time)
        return self.send_twap_algo_request(
            CreateTwapAlgo(
                name=name,
                market=market,
                dir=odir,
                quantity=quantity,
                intervalMs=interval_ms,
                rejectLockoutMs=reject_lockout_ms,
                endTime=end_time,
                account=account,
                takeThroughFrac=take_through_frac,
            )
        )

    def send_pov_algo(
        self,
        *,
        name: str,
        market: str,
        odir: OrderDir,
        target_volume_frac: Decimal,
        min_order_quantity: Decimal,
        max_quantity: Decimal,
        order_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[Decimal] = None,
    ) -> str:
        end_time_str = convert_datetime_to_utc_str(end_time)
        return self.send_pov_algo_request(
            CreatePovAlgo(
                name=name,
                market=market,
                dir=odir,
                targetVolumeFrac=target_volume_frac,
                minOrderQuantity=min_order_quantity,
                maxQuantity=max_quantity,
                orderLockoutMs=order_lockout_ms,
                endTime=end_time,
                account=account,
                takeThroughFrac=(take_through_frac),
            )
        )

    def send_smart_order_router_algo(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        odir: OrderDir,
        limit_price: Decimal,
        target_size: Decimal,
        execution_time_limit_ms: int,
    ) -> str:
        return self.send_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=odir,
                limitPrice=limit_price,
                targetSize=target_size,
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

    def preview_smart_order_router(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        odir: OrderDir,
        limit_price: Decimal,
        target_size: Decimal,
        execution_time_limit_ms: int,
    ) -> Optional[Sequence[OrderFields]]:
        algo = self.preview_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=odir,
                limitPrice=limit_price,
                targetSize=target_size,
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

        if algo is None:
            return None
        else:
            return algo.orders

    def send_mm_algo(
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
        ref_dist_frac: Decimal,
        tolerance_frac: Decimal,
        fill_lockout_ms: int,
        order_lockout_ms: int,
        reject_lockout_ms: int,
    ):
        return self.send_mm_algo_request(
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

    def send_spread_algo(
        self,
        *,
        name: str,
        market: str,
        buy_quantity: Decimal,
        sell_quantity: Decimal,
        min_position: Decimal,
        max_position: Decimal,
        max_improve_bbo: Decimal,
        position_tilt: Decimal,
        reference_price: ReferencePrice,
        ref_dist_frac: Decimal,
        tolerance_frac: Decimal,
        hedge_market: CreateSpreadAlgoHedgeMarket,
        fill_lockout_ms: int,
        order_lockout_ms: int,
        reject_lockout_ms: int,
        account: Optional[str] = None,
    ) -> str:
        return self.send_spread_algo_request(
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

    def get_cme_futures_series(
        self, series: str
    ) -> list[tuple[date, SearchMarketsFilterMarkets]]:
        markets = self.search_markets(
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

    def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> SearchMarketsFilterMarkets:

        [market] = [
            market
            for market in self.search_markets(
                search_string=f"{root} {year}{month}",
                venue="CME",
            )
            if isinstance(market.kind, MarketFieldsKindExchangeMarketKind)
            and market.kind.base.name.startswith(root)
        ]

        return market

    def get_balances_and_positions(self) -> list["BalancesAndPositions"]:
        # returns data in the shape account => venue => { usd_balance: xxx, ...usd margin info, then product: balance, etc. }
        summaries = self.get_account_summaries()

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

                    quantity: Decimal = Decimal(getattr(position, "quantity", "NaN"))
                    quantity = quantity if position.dir == OrderDir.BUY else -quantity
                    average_price = Decimal(getattr(position, "average_price", "NaN"))

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

    def get_cme_first_notice_date(self, market: str) -> Optional[date]:
        notice = self.get_first_notice_date(market)
        if notice is None or notice.first_notice_date is None:
            return None
        return notice.first_notice_date.date()
