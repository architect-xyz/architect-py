from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal, Optional

from architect_py.graphql_client.enums import CreateOrderType, OrderSource
import logging

from .graphql_client import GraphQLClient
from .graphql_client.input_types import (
    CreateOrder,
    CreateTimeInForce,
    CreateTimeInForceInstruction,
)

logger = logging.getLogger(__name__)


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
        side: Literal["buy", "sell"],
        quantity: float | Decimal,
        order_type: CreateOrderType = CreateOrderType.LIMIT,
        limit_price: float | Decimal,
        post_only: bool = False,
        trigger_price: Optional[float | Decimal] = None,
        time_in_force_instruction: CreateTimeInForceInstruction = CreateTimeInForceInstruction.GTC,
        good_til_date: Optional[datetime] = None,
        source: OrderSource = OrderSource.API,
    ):
        if good_til_date is not None:
            if good_til_date.tzinfo is None:
                raise ValueError(
                    "in sent_limit_order, the good_til_date must be timezone-aware. "
                    "Try datetime(..., tzinfo={your_local_timezone})"
                )
            else:
                utc_datetime = good_til_date.astimezone(timezone.utc)
                good_til_date_str = f"{utc_datetime.isoformat()}Z"
        else:
            good_til_date_str = None

        order = await self.send_order(
            CreateOrder(
                market=market,
                dir=side,
                quantity=str(quantity),
                orderType=order_type,
                limitPrice=str(limit_price),
                postOnly=post_only,
                triggerPrice=str(trigger_price),
                timeInForce=CreateTimeInForce(
                    instruction=time_in_force_instruction,
                    goodTilDate=good_til_date_str,
                ),
                source=source,
            )
        )

        return await self.get_order(order.order.id)
