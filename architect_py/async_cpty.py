import asyncio
import logging
import random
import uuid
from datetime import datetime
from decimal import Decimal
from typing import AsyncIterable, Dict, Optional, Sequence, Union

import grpc

from .grpc.models.Cpty.CptyRequest import (
    CancelAllOrders,
    CancelOrder,
    Login,
    Logout,
    PlaceBatchOrder,
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
from .grpc.models.Marketdata.L1BookSnapshot import L1BookSnapshot
from .grpc.models.Marketdata.L1BookSnapshotRequest import L1BookSnapshotRequest
from .grpc.models.Marketdata.L2BookSnapshot import L2BookSnapshot
from .grpc.models.Marketdata.L2BookSnapshotRequest import L2BookSnapshotRequest
from .grpc.models.Marketdata.L2BookUpdate import Diff, Snapshot
from .grpc.models.Marketdata.SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from .grpc.models.Marketdata.SubscribeL2BookUpdatesRequest import (
    SubscribeL2BookUpdatesRequest,
)
from .grpc.models.Marketdata.SubscribeTradesRequest import SubscribeTradesRequest
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
from .grpc.server import (
    add_CptyServicer_to_server,
    add_MarketdataServicer_to_server,
    add_OrderflowServicer_to_server,
)

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
        self.l1_book_snapshots_subscriptions: dict[
            int, L1BookSnapshotsSubscription
        ] = {}
        self.l2_book_updates_subscriptions: dict[int, L2BookUpdatesSubscription] = {}
        self.next_subscription_id = 1

        # marketdata caches
        self.l1_book_snapshots: dict[str, L1BookSnapshot] = {}
        self.l2_book_snapshots: dict[str, L2BookSnapshot] = {}

    def add_execution_info(self, symbol: str, execution_info: ExecutionInfo):
        """
        Add execution info for a symbol.
        """
        if symbol not in self.execution_info:
            self.execution_info[symbol] = {}
        self.execution_info[symbol][self.execution_venue] = execution_info

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

    async def on_place_batch_order(self, _batch: PlaceBatchOrder):
        """
        Called when the cpty receives a batch order to place.

        This may have different semantics (atomic, all-or-nothing) per cpty
        than sending multiple place_orders.
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

    def on_l1_book_snapshot(
        self,
        *,
        symbol: str,
        timestamp: Optional[datetime] = None,
        recv_time: Optional[datetime] = None,
        best_bid: Optional[Sequence[Decimal]] = None,
        best_ask: Optional[Sequence[Decimal]] = None,
    ):
        """
        Call this function to update the L1 book for a symbol.
        """
        if timestamp is None:
            timestamp = datetime.now()
        if recv_time is None:
            recv_time = datetime.now()
        self.l1_book_snapshots[symbol] = L1BookSnapshot(
            symbol,
            timestamp.microsecond * 1000,
            int(timestamp.timestamp()),
            list(best_bid) if best_bid is not None else None,
            list(best_ask) if best_ask is not None else None,
            int(recv_time.timestamp()),
            0,
        )
        for sub_id, sub in self.l1_book_snapshots_subscriptions.items():
            try:
                sub.queue.put_nowait(self.l1_book_snapshots[symbol])
            except asyncio.QueueFull:
                logging.warn(f"l1 book snapshot queue full #{sub_id}")

    def on_l2_book_snapshot(
        self,
        *,
        symbol: str,
        timestamp: Optional[datetime] = None,
        bids: Optional[Sequence[Sequence[Decimal]]] = None,
        asks: Optional[Sequence[Sequence[Decimal]]] = None,
        reset_sequence: bool = False,
        also_update_l1: bool = True,
    ):
        """
        Call this function to update the L2 book for a symbol.

        This also updates the L1 book snapshot unless also_update_l1 is False.
        """
        if timestamp is None:
            timestamp = datetime.now()
        if reset_sequence or symbol not in self.l2_book_snapshots:
            sequence_id = random.randint(0, 2**64 - 1)
            sequence_number = 0
        else:
            # INVARIANT: symbol in self.l2_book_snapshots
            sequence_id = self.l2_book_snapshots[symbol].sequence_id
            sequence_number = self.l2_book_snapshots[symbol].sequence_number + 1

        snap = Snapshot(
            list(map(list, asks)) if asks is not None else [],
            list(map(list, bids)) if bids is not None else [],
            sequence_id,
            sequence_number,
            timestamp.microsecond * 1000,
            int(timestamp.timestamp()),
        )

        self.l2_book_snapshots[symbol] = snap

        if also_update_l1:
            self.on_l1_book_snapshot(
                symbol=symbol,
                timestamp=timestamp,
                best_bid=bids[0] if bids is not None else None,
                best_ask=asks[0] if asks is not None else None,
            )

        for sub_id, sub in self.l2_book_updates_subscriptions.items():
            try:
                if sub.request.symbol == symbol:
                    sub.queue.put_nowait(snap)
            except asyncio.QueueFull:
                logging.warn(f"l2 book snapshot queue full #{sub_id}")

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
            elif isinstance(request, PlaceBatchOrder):
                try:
                    await self.on_place_batch_order(request)
                except NotImplementedError:
                    logging.error("on_place_batch_order not implemented")
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

    async def L1BookSnapshot(
        self, request: L1BookSnapshotRequest, context: grpc.aio.ServicerContext
    ):
        if request.symbol not in self.l1_book_snapshots:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        context.set_code(grpc.StatusCode.OK)
        return self.l1_book_snapshots[request.symbol]

    async def SubscribeL1BookSnapshots(
        self,
        request: SubscribeL1BookSnapshotsRequest,
        context: grpc.aio.ServicerContext,
    ):
        context.set_code(grpc.StatusCode.OK)
        await context.send_initial_metadata([])
        subscription_id = self.next_subscription_id
        self.next_subscription_id += 1
        logging.debug(f"registered l1 book snapshots subscription #{subscription_id}")
        subscription = L1BookSnapshotsSubscription(request)

        def cleanup_subscription(_context):
            del self.l1_book_snapshots_subscriptions[subscription_id]
            logging.debug(
                f"cleaned up l1 book snapshots subscription #{subscription_id}"
            )

        context.add_done_callback(cleanup_subscription)
        self.l1_book_snapshots_subscriptions[subscription_id] = subscription

        while True:
            next_item = await subscription.queue.get()
            if subscription.request.symbols is not None:
                if next_item.symbol not in subscription.request.symbols:
                    continue
            yield next_item

    async def L2BookSnapshot(
        self, request: L2BookSnapshotRequest, context: grpc.aio.ServicerContext
    ):
        if request.symbol not in self.l2_book_snapshots:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        context.set_code(grpc.StatusCode.OK)
        return self.l2_book_snapshots[request.symbol]

    async def SubscribeL2BookUpdates(
        self, request: SubscribeL2BookUpdatesRequest, context: grpc.aio.ServicerContext
    ):
        context.set_code(grpc.StatusCode.OK)
        await context.send_initial_metadata([])
        subscription_id = self.next_subscription_id
        self.next_subscription_id += 1
        logging.debug(f"registered l2 book updates subscription #{subscription_id}")
        subscription = L2BookUpdatesSubscription(request)

        def cleanup_subscription(_context):
            del self.l2_book_updates_subscriptions[subscription_id]
            logging.debug(f"cleaned up l2 book updates subscription #{subscription_id}")

        context.add_done_callback(cleanup_subscription)
        self.l2_book_updates_subscriptions[subscription_id] = subscription

        while True:
            next_item = await subscription.queue.get()
            yield next_item

    async def SubscribeTrades(
        self, request: SubscribeTradesRequest, context: grpc.aio.ServicerContext
    ):
        context.set_code(grpc.StatusCode.OK)
        await context.send_initial_metadata([])
        await asyncio.Future()

    def _add_method_handlers(self, server: grpc.aio.Server):
        add_CptyServicer_to_server(self, server)
        add_OrderflowServicer_to_server(self, server)
        add_MarketdataServicer_to_server(self, server)

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


class L1BookSnapshotsSubscription:
    request: SubscribeL1BookSnapshotsRequest
    queue: asyncio.Queue[L1BookSnapshot]

    def __init__(self, request: SubscribeL1BookSnapshotsRequest):
        self.request = request
        self.queue = asyncio.Queue()


class L2BookUpdatesSubscription:
    request: SubscribeL2BookUpdatesRequest
    queue: asyncio.Queue[Union[Snapshot, Diff]]

    def __init__(self, request: SubscribeL2BookUpdatesRequest):
        self.request = request
        self.queue = asyncio.Queue()
