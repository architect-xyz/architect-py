"""
This file extends the GraphQLClient class to provide a higher-level interface for
order entry with the Architect API.

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

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional, TypeAlias, Union


from architect_py.graphql_client.enums import (
    CreateOrderType,
    OrderSource,
    ReferencePrice,
)
import logging

from architect_py.graphql_client.fragments import OrderFields
from architect_py.graphql_client.get_order import GetOrderOrder

from .graphql_client import GraphQLClient
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


ValueInputType: TypeAlias = Union[int, float, Decimal, str]


class Client(GraphQLClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_names_by_route = {}

    async def start_session(self):
        await self.load_and_index_symbology()

    async def load_and_index_symbology(self):
        logger.info("Loading symbology...")
        markets = await self.get_filtered_markets()
        logger.info("Loaded %d markets", len(markets))
        self.market_names_by_route = {}
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
        dir: OrderDirection,
        quantity: ValueInputType,
        order_type: CreateOrderType = CreateOrderType.LIMIT,
        limit_price: ValueInputType,
        post_only: bool = False,
        trigger_price: Optional[ValueInputType] = None,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC,
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

        order: str = await self.send_order(
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

        return await self.get_order(order)

    async def send_twap_algo(
        self,
        *,
        name: str,
        market: str,
        dir: OrderDirection,
        quantity: ValueInputType,
        interval_ms: int,
        reject_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[ValueInputType] = None,
    ) -> str:

        end_time_str = convert_datetime_to_utc_str(end_time)
        return await self.send_twap_algo_request(
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

    async def send_pov_algo(
        self,
        *,
        name: str,
        market: str,
        dir: OrderDirection,
        target_volume_frac: ValueInputType,
        min_order_quantity: ValueInputType,
        max_quantity: ValueInputType,
        order_lockout_ms: int,
        end_time: datetime,
        account: Optional[str] = None,
        take_through_frac: Optional[ValueInputType] = None,
    ) -> str:
        end_time_str = convert_datetime_to_utc_str(end_time)
        return await self.send_pov_algo_request(
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

    async def send_smart_order_router_algo(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: OrderDirection,
        limit_price: ValueInputType,
        target_size: ValueInputType,
        execution_time_limit_ms: int,
    ) -> str:
        return await self.send_smart_order_router_algo_request(
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

    async def preview_smart_order_router(
        self,
        *,
        markets: list[str],
        base: str,
        quote: str,
        dir: OrderDirection,
        limit_price: ValueInputType,
        target_size: ValueInputType,
        execution_time_limit_ms: int,
    ) -> Optional[list[OrderFields]]:
        algo = await self.preview_smart_order_router_algo_request(
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

    async def send_mm_algo(
        self,
        *,
        name: str,
        market: str,
        account: Optional[str] = None,
        buy_quantity: ValueInputType,
        sell_quantity: ValueInputType,
        min_position: ValueInputType,
        max_position: ValueInputType,
        max_improve_bbo: ValueInputType,
        position_tilt: ValueInputType,
        reference_price: ReferencePrice,
        ref_dist_frac: ValueInputType,
        tolerance_frac: ValueInputType,
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
        buy_quantity: ValueInputType,
        sell_quantity: ValueInputType,
        min_position: ValueInputType,
        max_position: ValueInputType,
        max_improve_bbo: ValueInputType,
        position_tilt: ValueInputType,
        reference_price: ReferencePrice,
        ref_dist_frac: ValueInputType,
        tolerance_frac: ValueInputType,
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


def convert_datetime_to_utc_str(dt: datetime):
    if dt.tzinfo is None:
        raise ValueError(
            "in sent_limit_order, the good_til_date must be timezone-aware. Try \n"
            "import pytz\n"
            "datetime(..., tzinfo={your_local_timezone})\n"
            "# examples of local timezones: pytz.timezone('US/Eastern'), "
            "pytz.timezone('US/Pacific'), pytz.timezone('US/Central')"
        )
    utc_str = dt.astimezone(timezone.utc).isoformat()[:-6]
    # [:-6] removes the utc offset

    return f"{utc_str}Z"
