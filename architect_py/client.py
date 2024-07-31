from collections import defaultdict
from typing import Literal, Optional
import logging
from .graphql_client import GraphQLClient
from .graphql_client.input_types import CreateOrder, CreateTimeInForce

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
        market: str,
        side: Literal["buy", "sell"],
        limit_price: float,
        quantity: float,
        post_only: bool = False,
        time_in_force: str = "GTC",
    ):
        return await self.send_order(
            CreateOrder(
                market=market,
                order_type="LIMIT",
                dir=side,
                limit_price=str(limit_price),
                quantity=str(quantity),
                post_only=post_only,
                time_in_force=CreateTimeInForce(instruction=time_in_force),
            )
        )
