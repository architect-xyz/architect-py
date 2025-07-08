from decimal import Decimal
from typing import Any, Optional

from .common_types import OrderDir, TimeInForce, TradableProduct
from .grpc.models.definitions import (
    OrderId,
    OrderSource,
    OrderType,
    TriggerLimitOrderType,
)
from .grpc.models.Oms.PlaceOrderRequest import PlaceOrderRequest


class BatchPlaceOrder:
    """
    Helper class for collecting orders into a batch.
    """

    place_orders: list[PlaceOrderRequest]

    def __init__(self):
        self.place_orders = []

    async def place_order(
        self,
        *,
        id: Optional[OrderId] = None,
        symbol: TradableProduct | str,
        execution_venue: Optional[str] = None,
        dir: OrderDir,
        quantity: Decimal,
        limit_price: Optional[Decimal] = None,
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TimeInForce = TimeInForce.DAY,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        post_only: Optional[bool] = None,
        trigger_price: Optional[Decimal] = None,
        stop_loss: Optional[TriggerLimitOrderType] = None,
        take_profit_price: Optional[Decimal] = None,
        **kwargs: Any,
    ):
        assert quantity > 0, "quantity must be positive"

        req: PlaceOrderRequest = PlaceOrderRequest.new(
            dir=dir,
            quantity=quantity,
            symbol=symbol,
            time_in_force=time_in_force,
            limit_price=limit_price,
            order_type=order_type,
            account=account,
            id=id,
            parent_id=None,
            source=OrderSource.API,
            trader=trader,
            execution_venue=execution_venue,
            post_only=post_only,
            trigger_price=trigger_price,
            stop_loss=stop_loss,
            take_profit_price=take_profit_price,
        )
        self.place_orders.append(req)
