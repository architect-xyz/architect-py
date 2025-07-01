import asyncio
import logging
import uuid
from datetime import datetime
from decimal import Decimal
from typing import AsyncIterable, Dict, Optional, Sequence, Union

import grpc
import msgspec

from .grpc.client import dec_hook
from .grpc.models.Cpty.CptyRequest import (
    CancelAllOrders,
    CancelOrder,
    Login,
    Logout,
    PlaceOrder,
    UnannotatedCptyRequest,
)
from .grpc.models.Cpty.CptyResponse import (
    ReconcileOpenOrders,
    Symbology,
    UpdateAccountSummary,
)
from .grpc.models.definitions import (
    AccountIdOrName,
    AccountPosition,
    AccountStatistics,
    CptyLoginRequest,
    CptyLogoutRequest,
    ExecutionInfo,
    FillKind,
    OrderDir,
    OrderId,
    OrderRejectReason,
    UserId,
)
from .grpc.models.Oms.Cancel import Cancel
from .grpc.models.Oms.Order import Order
from .grpc.models.Orderflow.OrderflowRequest import (
    OrderflowRequestUnannotatedResponseType,
    TaggedCancelReject,
    TaggedFill,
    TaggedOrderAck,
    TaggedOrderCanceled,
    TaggedOrderOut,
    TaggedOrderReject,
)
from .grpc.models.Orderflow.SubscribeOrderflowRequest import SubscribeOrderflowRequest
from .grpc.utils import encoder

FILLS_NS = uuid.UUID("c4b64693-40d2-5613-8d13-bf35b89f92e0")


class AsyncCpty:
    """
    To implement an external cpty, subclass `AsyncCpty` and implement the callback
    stubs `on_login`, `on_place_order`, etc.  Use provided methods `ack_order`,
    `out_order`, etc. to drive orderflow events to consumers.

    Call `add_execution_info` to add execution info for a symbol.

    Call `serve` to start the server and wait for termination.

    For manual control of the grpc server, create your own `grpc.aio.Server`
    and call `_add_method_handlers` to add the method handlers.

    You can use as much or as little of this helper as desired.
    """

    def __init__(self, execution_venue: str):
        self.execution_venue = execution_venue
        self.execution_venue_fills_ns = uuid.uuid5(FILLS_NS, execution_venue)
        self.execution_info: Dict[str, Dict[str, ExecutionInfo]] = {}
        self.cpty_notifications: dict[int, CptyNotifications] = {}
        self.orderflow_subscriptions: dict[int, OrderflowSubscription] = {}
        self.next_subscription_id = 1

    def add_execution_info(self, symbol: str, execution_info: ExecutionInfo):
        """
        Add execution info for a symbol.
        """
        self.execution_info[self.execution_venue][symbol] = execution_info

    async def on_login(self, _request: CptyLoginRequest):
        raise NotImplementedError

    async def on_logout(self, _request: CptyLogoutRequest):
        raise NotImplementedError

    async def on_place_order(self, _order: Order):
        """
        Called when the cpty receives an order to place.

        Call `ack_order` or `reject_order` to advance the order state;
        otherwise, the order will be left in the `PENDING` state.
        """
        raise NotImplementedError

    async def on_cancel_order(
        self, _cancel: Cancel, _original_order: Optional[Order] = None
    ):
        """
        Called when the cpty receives a cancel order request.

        Call `reject_cancel` if there's a problem with canceling the order;
        make sure to reference the `cancel.cancel_id` to identify the cancel.

        Args:
            cancel: The cancel order request.
            original_order: The original order that was cancelled, if the OMS knows it.
        """
        raise NotImplementedError

    async def on_cancel_all_orders(
        self,
        _cancel_id: str,
        _trader: Optional[UserId] = None,
        _account: Optional[AccountIdOrName] = None,
    ):
        """
        Called when the cpty receives a cancel-all orders request.
        """
        raise NotImplementedError

    async def get_open_orders(self) -> Sequence[Order]:
        """
        Get all open orders.  This is called at least once per client
        connection/login.  Return a list of known open orders.
        """
        return []

    def ack_order(self, order_id: OrderId, *, exchange_order_id: Optional[str] = None):
        """
        Acknowledge an order has reached the exchange.

        Optionally, provide the exchange order id to correlate with the order;
        this helps with order reconciliation.
        """
        order_ack = TaggedOrderAck(order_id, exchange_order_id)
        self._put_orderflow_event(order_ack)

    def reject_order(
        self,
        order_id: OrderId,
        *,
        reject_reason: OrderRejectReason,
        reject_message: Optional[str] = None,
    ):
        """
        Reject an order.
        """
        order_reject = TaggedOrderReject(order_id, reject_reason, reject_message)
        self._put_orderflow_event(order_reject)

    def out_order(self, order_id: OrderId, *, canceled: bool = False):
        """
        Notify that an order is outed.  If it was outed because of a cancel,
        pass `canceled=True`.  For all other reasons, pass `canceled=False`.
        """
        if canceled:
            order_out = TaggedOrderCanceled(order_id)
        else:
            order_out = TaggedOrderOut(order_id)
        self._put_orderflow_event(order_out)

    def fill_order(
        self,
        *,
        dir: OrderDir,
        exchange_fill_id: str,
        # if not provided, a suitable uuiv5 will be generated from the exchange_fill_id
        fill_id: Optional[str] = None,
        fill_kind: FillKind = FillKind.Normal,
        price: Decimal,
        quantity: Decimal,
        symbol: str,
        trade_time: datetime,
        account: AccountIdOrName,
        is_taker: bool,
        fee: Optional[Decimal] = None,
        fee_currency: Optional[str] = None,
        order_id: OrderId,
        trader: Optional[UserId] = None,
    ):
        """
        Notify that an order has been filled, either partially or in full.
        """
        now = datetime.now()
        if fill_id is None:
            fill_id = str(uuid.uuid5(self.execution_venue_fills_ns, exchange_fill_id))
        self._put_orderflow_event(
            TaggedFill(
                dir,
                fill_id,
                fill_kind,
                price,
                quantity,
                symbol,
                int(trade_time.timestamp()),
                trade_time.microsecond * 1000,
                self.execution_venue,
                account,
                1 if is_taker else 0,
                int(now.timestamp()),
                now.microsecond * 1000,
                fee,
                fee_currency,
                order_id,
                trader,
                exchange_fill_id,
            )
        )

    def reject_cancel(
        self,
        cancel_id: str,
        *,
        reject_reason: str,
        reject_message: Optional[str] = None,
    ):
        """
        Reject a cancel.
        """
        self._put_orderflow_event(
            TaggedCancelReject(cancel_id, reject_reason, reject_message)
        )

    def _put_orderflow_event(self, event):
        for sub_id, sub in self.orderflow_subscriptions.items():
            try:
                sub.queue.put_nowait(event)
            except asyncio.QueueFull:
                logging.warn(f"orderflow subscription queue full #{sub_id}")

    def update_account_summary(
        self,
        account: AccountIdOrName,
        *,
        is_snapshot: bool,
        timestamp: datetime,
        balances: Optional[Dict[str, Decimal]] = None,
        positions: Optional[Dict[str, AccountPosition]] = None,
        cash_excess: Optional[Decimal] = None,
        equity: Optional[Decimal] = None,
        yesterday_equity: Optional[Decimal] = None,
        position_margin: Optional[Decimal] = None,
        purchasing_power: Optional[Decimal] = None,
        realized_pnl: Optional[Decimal] = None,
        unrealized_pnl: Optional[Decimal] = None,
    ):
        """
        Update account summary, as reported by the exchange.

        Not all fields are required--fill only the fields that are relevant.
        """
        positions_dict = None
        if positions is not None:
            positions_dict = {}
            for symbol, position in positions.items():
                positions_dict[symbol] = [position]
        self._put_cpty_event(
            UpdateAccountSummary(
                account,
                is_snapshot,
                int(timestamp.timestamp()),
                timestamp.microsecond * 1000,
                balances,
                positions_dict,
                AccountStatistics(
                    cash_excess=cash_excess,
                    equity=equity,
                    yesterday_equity=yesterday_equity,
                    position_margin=position_margin,
                    purchasing_power=purchasing_power,
                    realized_pnl=realized_pnl,
                    unrealized_pnl=unrealized_pnl,
                ),
            )
        )

    def _put_cpty_event(self, event):
        for sub_id, sub in self.cpty_notifications.items():
            try:
                sub.queue.put_nowait(event)
            except asyncio.QueueFull:
                logging.warn(f"cpty notification queue full #{sub_id}")

    async def Cpty(
        self,
        request_iterator: AsyncIterable[UnannotatedCptyRequest],
        context: grpc.aio.ServicerContext,
    ):
        context.set_code(grpc.StatusCode.OK)
        await context.send_initial_metadata([])
        logged_in: Optional[Login] = None
        subscription_id = self.next_subscription_id
        self.next_subscription_id += 1

        def cleanup_subscription(_context):
            if subscription_id is not None:
                try:
                    del self.cpty_notifications[subscription_id]
                    logging.debug(f"cleaned up cpty notification #{subscription_id}")
                except KeyError:
                    pass

        context.add_done_callback(cleanup_subscription)
        async for request in request_iterator:
            logging.debug(f"Cpty: {request}")
            if not logged_in and not isinstance(request, Login):
                logging.error("not logged in, skipping request")
                continue
            if isinstance(request, Login):
                try:
                    await self.on_login(request)
                    logged_in = request
                    logging.debug(f"registered cpty notification #{subscription_id}")
                    self.cpty_notifications[subscription_id] = CptyNotifications(
                        account=request.account,
                        trader=request.trader,
                    )
                except NotImplementedError:
                    logging.error("on_login not implemented")
                if logged_in:
                    # send symbology info to client
                    yield Symbology(self.execution_info)
                    # send open orders to client
                    open_orders = await self.get_open_orders()
                    yield ReconcileOpenOrders(list(open_orders))
            elif isinstance(request, Logout):
                try:
                    del self.cpty_notifications[subscription_id]
                    logged_in = None
                    await self.on_logout(request)
                except NotImplementedError:
                    logging.error("on_logout not implemented")
            elif isinstance(request, PlaceOrder):
                try:
                    await self.on_place_order(request)
                except NotImplementedError:
                    logging.error("on_place_order not implemented")
            elif isinstance(request, CancelOrder):
                try:
                    await self.on_cancel_order(request.cancel, request.original_order)
                except NotImplementedError:
                    logging.error("on_cancel_order not implemented")
            elif isinstance(request, CancelAllOrders):
                try:
                    await self.on_cancel_all_orders(
                        request.cancel_id, request.trader, request.account
                    )
                except NotImplementedError:
                    logging.error("on_cancel_all_orders not implemented")
            else:
                logging.error(f"unhandled cpty request: {request}")

    async def SubscribeOrderflow(
        self, request: SubscribeOrderflowRequest, context: grpc.aio.ServicerContext
    ):
        context.set_code(grpc.StatusCode.OK)
        await context.send_initial_metadata([])
        logging.debug(f"Orderflow: {request}")
        subscription_id = self.next_subscription_id
        self.next_subscription_id += 1
        logging.debug(f"registered orderflow subscription #{subscription_id}")

        def cleanup_subscription(_context):
            del self.orderflow_subscriptions[subscription_id]
            logging.debug(f"cleaned up orderflow subscription #{subscription_id}")

        context.add_done_callback(cleanup_subscription)
        subscription = OrderflowSubscription(request)
        self.orderflow_subscriptions[subscription_id] = subscription
        while True:
            next_item = await subscription.queue.get()
            yield next_item

    def _add_cpty_method_handlers(self, server: grpc.aio.Server):
        decoder = msgspec.json.Decoder(type=UnannotatedCptyRequest, dec_hook=dec_hook)
        rpc_method_handlers = {
            "Cpty": grpc.stream_stream_rpc_method_handler(
                self.Cpty,
                request_deserializer=decoder.decode,
                response_serializer=encoder.encode,
            ),
        }
        generic_handler = grpc.method_handlers_generic_handler(
            "json.architect.Cpty", rpc_method_handlers
        )
        server.add_generic_rpc_handlers((generic_handler,))

    def _add_orderflow_method_handlers(self, server: grpc.aio.Server):
        decoder = msgspec.json.Decoder(
            type=SubscribeOrderflowRequest, dec_hook=dec_hook
        )
        rpc_method_handlers = {
            "SubscribeOrderflow": grpc.unary_stream_rpc_method_handler(
                self.SubscribeOrderflow,
                request_deserializer=decoder.decode,
                response_serializer=encoder.encode,
            ),
        }
        generic_handler = grpc.method_handlers_generic_handler(
            "json.architect.Orderflow", rpc_method_handlers
        )
        server.add_generic_rpc_handlers((generic_handler,))

    def _add_method_handlers(self, server: grpc.aio.Server):
        self._add_cpty_method_handlers(server)
        self._add_orderflow_method_handlers(server)

    async def serve(self, bind: str):
        server = grpc.aio.server()
        self._add_method_handlers(server)
        server.add_insecure_port(bind)
        await server.start()
        logging.info(f"grpc server started on {bind}")
        await server.wait_for_termination()


class CptyNotifications:
    account: Optional[AccountIdOrName] = None
    trader: Optional[str] = None
    queue: asyncio.Queue[Union[Symbology, ReconcileOpenOrders, UpdateAccountSummary]]

    def __init__(
        self, account: Optional[AccountIdOrName] = None, trader: Optional[str] = None
    ):
        self.account = account
        self.trader = trader
        self.queue = asyncio.Queue()


class OrderflowSubscription:
    request: SubscribeOrderflowRequest
    queue: asyncio.Queue[OrderflowRequestUnannotatedResponseType]

    def __init__(self, request: SubscribeOrderflowRequest):
        self.request = request
        self.queue = asyncio.Queue()
