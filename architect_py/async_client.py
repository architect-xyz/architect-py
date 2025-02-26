"""
This file composes the GraphQLClient class to provide a higher-level interface
for order entry with the Architect API.

These are not required to send orders, but provide typed interfaces for the
various order types and algorithms that can be sent to the OMS.


The functions to send orders will return the order ID string
After sending the order, this string can be used to retrieve the order status

send_limit_order -> get_order

The individual graphql types are subject to change, so it is not recommended to use them directly.

"""

import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Any, AsyncIterator, List, Optional, Sequence

from architect_py.graphql_client.get_fills_query import (
    GetFillsQueryFolioHistoricalFills,
)
from architect_py.graphql_client.place_order_mutation import PlaceOrderMutationOms
from architect_py.graphql_client.subscribe_trades import SubscribeTradesTrades
from architect_py.grpc_models.Marketdata.Marketdata_Array_of_L1BookSnapshot import (
    L1BookSnapshot,
)
from architect_py.grpc_models.Marketdata.Marketdata_L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_models.Marketdata.Marketdata_L2BookUpdate import L2BookUpdate
from architect_py.grpc_models.Marketdata.Marketdata_Trade import Trade
from architect_py.scalars import OrderDir, TradableProduct
from architect_py.utils.nearest_tick import nearest_tick, TickRoundMethod

from .graphql_client import GraphQLClient
from .graphql_client.enums import (
    CandleWidth,
    OrderType,
    TimeInForce,
)
from .graphql_client.fragments import (
    AccountSummaryFields,
    AccountWithPermissionsFields,
    CancelFields,
    CandleFields,
    ExecutionInfoFields,
    L2BookFields,
    MarketTickerFields,
    OrderFields,
    ProductInfoFields,
)

# from .graphql_client.input_types import (
#     CreateMMAlgo,
#     CreateOrder,
#     CreatePovAlgo,
#     CreateSmartOrderRouterAlgo,
#     CreateSpreadAlgo,
#     CreateSpreadAlgoHedgeMarket,
#     CreateTimeInForce,
#     CreateTimeInForceInstruction,
#     CreateTwapAlgo,
# )
from .grpc_client import GRPCClient

from .utils.price_bands import price_band_pairs

logger = logging.getLogger(__name__)


class AsyncClient:
    graphql_client: GraphQLClient
    grpc_client: GRPCClient

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        host: str = "https://app.architect.co",
        paper_trading: bool = True,
        port: Optional[int] = None,
        **kwargs: Any,
    ):
        """ """

        if not api_key.isalnum():
            raise ValueError(
                "API key must be alphanumeric, please double check your credentials."
            )
        elif "," in api_key or "," in api_secret:
            raise ValueError(
                "API key and secret cannot contain commas, please double check your credentials."
            )
        elif " " in api_key or " " in api_secret:
            raise ValueError(
                "API key and secret cannot contain spaces, please double check your credentials."
            )
        elif len(api_key) != 24 or len(api_secret) != 44:
            raise ValueError(
                "API key and secret are not the correct length, please double check your credentials."
            )

        if port is None:
            if paper_trading:
                port = 5678
            else:
                port = 4567

        self.graphql_client = GraphQLClient(
            api_key=api_key, api_secret=api_secret, host=host, port=port, **kwargs
        )

        self.grpc_client = GRPCClient(self.graphql_client)

    async def who_am_i(self) -> tuple[str, str]:
        """
        Returns
        (userId, user_email)
        """
        user_id = await self.graphql_client.user_id_query()
        email = await self.graphql_client.user_email_query()

        return user_id.user_id, email.user_email

    async def search_symbols(
        self,
        search_string: Optional[str] = None,
        execution_venue: Optional[str] = None,
    ) -> List[TradableProduct]:
        """
        returns a list of TradableProduct objects
        """
        markets = (
            await self.graphql_client.search_symbols_query(
                search_string=search_string, execution_venue=execution_venue
            )
        ).search_symbols

        return markets

    async def get_product_info(self, symbol: str) -> Optional[ProductInfoFields]:
        # this reduces the indirection count
        info = await self.graphql_client.get_product_info_query(symbol)
        return info.product_info

    async def get_product_infos(
        self, symbols: list[str]
    ) -> Sequence[ProductInfoFields]:
        infos = await self.graphql_client.get_product_infos_query(symbols)
        return infos.product_infos

    async def get_cme_first_notice_date(self, symbol: str) -> Optional[date]:
        notice = await self.graphql_client.get_first_notice_date_query(symbol)
        if notice is None or notice.product_info is None:
            return None
        return notice.product_info.first_notice_date

    async def get_future_series(self, series_symbol: str) -> list[str]:
        futures_series = await self.graphql_client.get_future_series_query(
            series_symbol
        )
        return futures_series.futures_series

    async def get_execution_info(
        self, symbol: TradableProduct, execution_venue: str
    ) -> ExecutionInfoFields:
        execution_info = await self.graphql_client.get_execution_info_query(
            symbol, execution_venue
        )
        return execution_info.execution_info

    @staticmethod
    def get_expiration_from_CME_name(name: str) -> date:
        _, d, *_ = name.split(" ")
        return datetime.strptime(d, "%Y%m%d").date()

    async def get_cme_futures_series(self, series: str) -> list[tuple[date, str]]:
        markets = await self.get_future_series(
            series,
        )

        filtered_markets = [
            (self.get_expiration_from_CME_name(market), market) for market in markets
        ]

        filtered_markets.sort(key=lambda x: x[0])

        return filtered_markets

    async def get_cme_future_from_root_month_year(
        self, root: str, month: int, year: int
    ) -> str:
        [market] = [
            market
            for market in await self.search_symbols(
                f"{root} {year}{month:02d}",
            )
        ]

        return market

    async def list_accounts(self) -> Sequence[AccountWithPermissionsFields]:
        accounts = await self.graphql_client.list_accounts_query()
        return accounts.accounts

    async def get_account_summary(self, account: str) -> AccountSummaryFields:
        summary = await self.graphql_client.get_account_summary_query(account=account)
        return summary.account_summary

    async def get_account_summaries(
        self,
        accounts: Optional[list[str]] = None,
        trader: Optional[str] = None,
    ) -> Sequence[AccountSummaryFields]:
        summaries = await self.graphql_client.get_account_summaries_query(
            trader=trader, accounts=accounts
        )
        return summaries.account_summaries

    async def get_account_history(
        self,
        account: str,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
    ) -> Sequence[AccountSummaryFields]:
        history = await self.graphql_client.get_account_history_query(
            account=account, from_inclusive=from_inclusive, to_exclusive=to_exclusive
        )
        return history.account_history

    async def get_open_orders(
        self,
        order_ids: Optional[list[str]] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        symbol: Optional[str] = None,
        parent_order_id: Optional[str] = None,
    ) -> Sequence[OrderFields]:
        orders = await self.graphql_client.get_open_orders_query(
            venue=venue,
            account=account,
            trader=trader,
            symbol=symbol,
            parent_order_id=parent_order_id,
            order_ids=order_ids,
        )
        return orders.open_orders

    async def get_all_open_orders(self) -> Sequence[OrderFields]:
        orders = await self.graphql_client.get_open_orders_query()
        return orders.open_orders

    async def get_historical_orders(
        self,
        order_ids: Optional[list[str]] = None,
        from_inclusive: Optional[datetime] = None,
        to_exclusive: Optional[datetime] = None,
        venue: Optional[str] = None,
        account: Optional[str] = None,
        parent_order_id: Optional[str] = None,
    ) -> Sequence[OrderFields]:
        orders = await self.graphql_client.get_historical_orders_query(
            order_ids=order_ids,
            venue=venue,
            account=account,
            parent_order_id=parent_order_id,
            from_inclusive=from_inclusive,
            to_exclusive=to_exclusive,
        )
        return orders.historical_orders

    async def get_order(self, order_id: str) -> Optional[OrderFields]:
        open_orders = await self.graphql_client.get_open_orders_query(
            order_ids=[order_id]
        )

        for open_order in open_orders.open_orders:
            if open_order.id == order_id:
                return open_order

        historical_orders = await self.graphql_client.get_historical_orders_query(
            order_ids=[order_id]
        )

        if historical_orders.historical_orders:
            return historical_orders.historical_orders[0]

    async def get_orders(self, order_ids: list[str]) -> list[Optional[OrderFields]]:
        orders_dict: dict[str, Optional[OrderFields]] = {
            order_id: None for order_id in order_ids
        }

        open_orders = (
            await self.graphql_client.get_open_orders_query(order_ids=order_ids)
        ).open_orders
        for open_order in open_orders:
            orders_dict[open_order.id] = open_order

        not_open_order_ids = [
            order_id for order_id in order_ids if orders_dict[order_id] is None
        ]

        historical_orders = (
            await self.graphql_client.get_historical_orders_query(
                order_ids=not_open_order_ids
            )
        ).historical_orders
        for historical_order in historical_orders:
            orders_dict[historical_order.id] = historical_order

        return [orders_dict[order_id] for order_id in order_ids]

    async def get_fills(
        self,
        from_inclusive: Optional[datetime],
        to_exclusive: Optional[datetime],
        venue: Optional[str] = None,
        account: Optional[str] = None,
        order_id: Optional[str] = None,
    ) -> GetFillsQueryFolioHistoricalFills:
        fills = await self.graphql_client.get_fills_query(
            venue, account, order_id, from_inclusive, to_exclusive
        )
        return fills.historical_fills

    async def get_market_status(self, symbol: str, venue: str):
        market_status = await self.graphql_client.get_market_status_query(symbol, venue)
        return market_status.market_status

    async def get_market_snapshot(self, symbol: str, venue: str) -> MarketTickerFields:
        """this is an alias for l1_book_snapshot"""
        return await self.get_l1_book_snapshot(symbol=symbol, venue=venue)

    async def get_market_snapshots(
        self, symbols: list[str], venue: str
    ) -> Sequence[MarketTickerFields]:
        """this is an alias for l1_book_snapshots"""
        return await self.get_l1_book_snapshots(venue=venue, symbols=symbols)

    async def get_candles_snapshot(
        self,
        symbol: str,
        venue: str,
        candle_width: CandleWidth,
        start: datetime,
        end: Optional[datetime] = None,
    ) -> Sequence[CandleFields]:
        start.tzinfo
        if end is None:
            end = datetime.now(tz=start.tzinfo)
        candles = await self.graphql_client.get_candle_snapshot_query(
            venue=venue, symbol=symbol, candle_width=candle_width, start=start, end=end
        )
        return candles.historical_candles

    async def get_l1_book_snapshot(
        self,
        symbol: str,
        venue: str,
    ) -> MarketTickerFields:
        snapshot = await self.graphql_client.get_l_1_book_snapshot_query(
            symbol=symbol, venue=venue
        )
        return snapshot.ticker

    async def get_l1_book_snapshots(
        self, symbols: list[str], venue: str
    ) -> Sequence[MarketTickerFields]:
        snapshot = await self.graphql_client.get_l_1_book_snapshots_query(
            venue=venue, symbols=symbols
        )
        return snapshot.tickers

    async def get_l2_book_snapshot(self, symbol: str, venue: str) -> L2BookFields:
        l2_book = await self.graphql_client.get_l_2_book_snapshot_query(
            symbol=symbol, venue=venue
        )
        return l2_book.l_2_book_snapshot

    async def subscribe_l1_book(
        self, endpoint: str, symbols: list[str] | None = None
    ) -> AsyncIterator[L1BookSnapshot]:
        raise NotImplementedError

    async def subscribe_l2_book(
        self,
        endpoint: str,
        symbol: str,
        venue: Optional[str],
    ) -> AsyncIterator[L2BookSnapshot]:
        raise NotImplementedError

    async def subscribe_trades(self, symbol: str, venue: str) -> AsyncIterator[Trade]:
        raise NotImplementedError

    async def send_limit_order(
        self,
        *,
        symbol: str,
        odir: OrderDir,
        quantity: Decimal,
        limit_price: Decimal,
        execution_venue: Optional[str],
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TimeInForce = TimeInForce.DAY,
        good_til_date: Optional[datetime] = None,
        price_round_method: Optional[TickRoundMethod] = None,
        account: Optional[str] = None,
        trader: Optional[str] = None,
        post_only: bool = False,
        trigger_price: Optional[Decimal] = None,
    ) -> OrderFields:
        """
        if execution_venue is set to None, the OMS will send the order to the primary_exchange

        the primary_exchange can be deduced from `get_product_info`

        While technically optional, for most order types, the account is required
        """
        assert quantity > 0, "quantity must be positive"

        if price_round_method is not None:
            if execution_venue is None:
                product_info = await self.get_product_info(symbol)
                if product_info is None:
                    raise ValueError(
                        f"Could not find product information for {symbol} while trying to get execution venue for rounding price"
                    )
                execution_venue = product_info.primary_venue
                if execution_venue is None:
                    raise ValueError(
                        f"Could not find primary exchange for {symbol} while trying to get execution venue for rounding price"
                    )
            execution_info = await self.get_execution_info(
                TradableProduct(symbol), execution_venue
            )
            if (tick_size := execution_info.tick_size) is not None:
                if tick_size:
                    limit_price = nearest_tick(
                        limit_price, method=price_round_method, tick_size=tick_size
                    )
            else:
                raise ValueError(f"Could not find market information for {symbol}")

        if not isinstance(trigger_price, Decimal) and trigger_price is not None:
            trigger_price = Decimal(trigger_price)

        order: PlaceOrderMutationOms = await self.graphql_client.place_order_mutation(
            symbol,
            odir,
            quantity,
            order_type,
            time_in_force,
            None,
            trader,
            account,
            limit_price,
            post_only,
            trigger_price,
            good_til_date,
            execution_venue,
        )

        return order.place_order

    async def send_market_pro_order(
        self,
        *,
        symbol: TradableProduct,
        execution_venue: str,
        odir: OrderDir,
        quantity: Decimal,
        time_in_force: TimeInForce = TimeInForce.DAY,
        account: Optional[str] = None,
        fraction_through_market: Decimal = Decimal("0.001"),
    ) -> OrderFields:

        # Check for GQL failures
        bbo_snapshot = await self.get_market_snapshot(
            symbol=symbol, venue=execution_venue
        )
        if bbo_snapshot is None:
            raise ValueError(
                f"Failed to send market order with reason: no market snapshot for {symbol}"
            )

        price_band = price_band_pairs.get(symbol, None)

        if odir == OrderDir.BUY:
            if bbo_snapshot.ask_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no ask price for {symbol}"
                )
            limit_price = bbo_snapshot.ask_price * (1 + fraction_through_market)

            if price_band and bbo_snapshot.last_price:
                price_band_reference_price = bbo_snapshot.last_price + price_band
                limit_price = min(limit_price, price_band_reference_price)

        else:
            if bbo_snapshot.bid_price is None:
                raise ValueError(
                    f"Failed to send market order with reason: no bid price for {symbol}"
                )
            limit_price = bbo_snapshot.bid_price * (1 - fraction_through_market)
            if price_band and bbo_snapshot.last_price:
                price_band_reference_price = bbo_snapshot.last_price - price_band
                limit_price = min(limit_price, price_band_reference_price)

        # Conservatively round price to nearest tick
        tick_round_method = (
            TickRoundMethod.FLOOR if odir == OrderDir.BUY else TickRoundMethod.CEIL
        )

        execution_info = await self.get_execution_info(
            execution_venue=execution_venue, symbol=symbol
        )

        if (
            execution_info is not None
            and (tick_size := execution_info.tick_size) is not None
        ):
            limit_price = nearest_tick(
                Decimal(limit_price),
                tick_round_method,
                tick_size=tick_size,
            )

        return await self.send_limit_order(
            symbol=symbol,
            execution_venue=execution_venue,
            odir=odir,
            quantity=quantity,
            account=account,
            order_type=OrderType.LIMIT,
            limit_price=limit_price,
            time_in_force=time_in_force,
        )

    async def cancel_order(self, order_id: str) -> CancelFields:
        cancel = await self.graphql_client.cancel_order_mutation(order_id)
        return cancel.cancel_order

    async def cancel_all_orders(self) -> bool:
        b = await self.graphql_client.cancel_all_orders_mutation()
        return b.cancel_all_orders
