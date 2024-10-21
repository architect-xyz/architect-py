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

from dataclasses import dataclass
import logging
import dns.resolver
import grpc
from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum
import time
from typing import Any, Optional, TypeAlias, Union

from architect_py.graphql_client.search_markets import SearchMarketsFilterMarkets
from architect_py.utils.balance_and_positions import (
    Balance,
    BalancesAndPositions,
    SimplePosition,
)
from architect_py.utils.dt import (
    convert_datetime_to_utc_str,
    get_expiration_from_CME_name,
)
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


class OrderDirection(Enum):
    BUY = "buy"
    SELL = "sell"

    def __int__(self):
        if self == OrderDirection.BUY:
            return 1
        elif self == OrderDirection.SELL:
            return -1
        else:
            raise ValueError(f"Unknown OrderDirection: {self}")


DecimalLike: TypeAlias = Union[int, float, Decimal, str]


class Client(GraphQLClient):
    def __init__(self, *args, no_gql: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
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
                if market.kind.base.name not in by_base:  # type: ignore
                    by_base[market.kind.base.name] = {}  # type: ignore
                by_quote = by_base[market.kind.base.name]  # type: ignore
                by_quote[market.kind.quote.name] = market.name  # type: ignore
            logger.info("Indexed %d markets", len(markets))

    # CR alee: make base, venue, route optional, and add optional quote.
    # Have to think harder about efficient indexing.
    def find_markets(
        self,
        base: str,
        venue: str,
        route: str = "DIRECT",
    ):
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
        dir: OrderDirection,
        quantity: DecimalLike,
        order_type: CreateOrderType = CreateOrderType.LIMIT,
        limit_price: DecimalLike,
        post_only: bool = False,
        trigger_price: Optional[DecimalLike] = None,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC,
        good_til_date: Optional[datetime] = None,
        account: Optional[str] = None,
        quote_id: Optional[str] = None,
        source: OrderSource = OrderSource.API,
        wait_for_confirm: bool = False,
    ) -> Optional[GetOrderOrder]:
        """
        `account` is optional depending on the final cpty it gets to
        For CME orders, the account is required
        """
        if good_til_date is not None:
            good_til_date_str = convert_datetime_to_utc_str(good_til_date)
        else:
            good_til_date_str = None

        order: str = self.send_order(
            CreateOrder(
                market=market,
                dir=dir.value,
                quantity=str(quantity),
                account=account,
                orderType=order_type,
                limitPrice=str(limit_price),
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

    def send_twap_algo(
        self,
        *,
        name: str,
        market: str,
        dir: OrderDirection,
        quantity: DecimalLike,
        interval_ms: int,
        reject_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[DecimalLike] = None,
    ) -> str:

        end_time_str = convert_datetime_to_utc_str(end_time)
        return self.send_twap_algo_request(
            CreateTwapAlgo(
                name=name,
                market=market,
                dir=dir.value,
                quantity=quantity,
                intervalMs=interval_ms,
                rejectLockoutMs=reject_lockout_ms,
                endTime=end_time_str,
                account=account,
                takeThroughFrac=take_through_frac,
            )
        )

    def send_pov_algo(
        self,
        *,
        name: str,
        market: str,
        dir: OrderDirection,
        target_volume_frac: DecimalLike,
        min_order_quantity: DecimalLike,
        max_quantity: DecimalLike,
        order_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[DecimalLike] = None,
    ) -> str:
        end_time_str = convert_datetime_to_utc_str(end_time)
        return self.send_pov_algo_request(
            CreatePovAlgo(
                name=name,
                market=market,
                dir=dir.value,
                targetVolumeFrac=str(target_volume_frac),
                minOrderQuantity=str(min_order_quantity),
                maxQuantity=str(max_quantity),
                orderLockoutMs=order_lockout_ms,
                endTime=end_time_str,
                account=account,
                takeThroughFrac=(
                    str(take_through_frac) if take_through_frac is not None else None
                ),
            )
        )

    def send_smart_order_router_algo(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: OrderDirection,
        limit_price: DecimalLike,
        target_size: DecimalLike,
        execution_time_limit_ms: int,
    ) -> str:
        return self.send_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=dir.value,
                limitPrice=str(limit_price),
                targetSize=str(target_size),
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

    def preview_smart_order_router(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: OrderDirection,
        limit_price: DecimalLike,
        target_size: DecimalLike,
        execution_time_limit_ms: int,
    ) -> Optional[list[OrderFields]]:
        algo = self.preview_smart_order_router_algo_request(
            CreateSmartOrderRouterAlgo(
                markets=markets,
                base=base,
                quote=quote,
                dir=dir.value,
                limitPrice=str(limit_price),
                targetSize=str(target_size),
                executionTimeLimitMs=execution_time_limit_ms,
            )
        )

        return getattr(algo, "orders", None)

    def send_mm_algo(
        self,
        *,
        name: str,
        market: str,
        account: Optional[str] = None,
        buy_quantity: DecimalLike,
        sell_quantity: DecimalLike,
        min_position: DecimalLike,
        max_position: DecimalLike,
        max_improve_bbo: DecimalLike,
        position_tilt: DecimalLike,
        reference_price: ReferencePrice,
        ref_dist_frac: DecimalLike,
        tolerance_frac: DecimalLike,
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
                        usd_amount = Decimal(balance.amount)  # type: ignore
                        total_margin = Decimal(balance.total_margin)  # type: ignore
                        position_margin = Decimal(balance.position_margin)  # type: ignore
                        purchasing_power = Decimal(balance.purchasing_power)  # type: ignore
                        cash_excess = Decimal(balance.cash_excess)  # type: ignore
                        yesterday_balance = Decimal(balance.yesterday_balance)  # type: ignore

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

                    quantity: Decimal = Decimal(position.quantity)  # type: ignore
                    quantity = quantity if position.dir == "buy" else -quantity
                    average_price = Decimal(position.average_price)  # type: ignore

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
