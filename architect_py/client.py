from typing import Literal
from .graphql_client import GraphQLClient
from .graphql_client.input_types import CreateOrder, CreateTimeInForce


class Client(GraphQLClient):
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
