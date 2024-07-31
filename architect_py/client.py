from typing import Literal, Optional
from .graphql_client import GraphQLClient
from .graphql_client.input_types import CreateOrder, CreateTimeInForce


class Client(GraphQLClient):
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
