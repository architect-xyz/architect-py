from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal, Optional

from architect_py.graphql_client.enums import CreateOrderType, OrderSource
from .graphql_client import GraphQLClient
from .graphql_client.input_types import (
    CreateOrder,
    CreateTimeInForce,
    CreateTimeInForceInstruction,
)


class Client(GraphQLClient):
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
                order_type=order_type,
                dir=side,
                limit_price=str(limit_price),
                quantity=str(quantity),
                post_only=post_only,
                trigger_price=str(trigger_price),
                time_in_force=CreateTimeInForce(
                    instruction=time_in_force_instruction,
                    good_til_date=good_til_date_str,
                ),
                order_source=source,
            )
        )

        return await self.get_order(order.order.id)
