# Generated by ariadne-codegen
# Source: queries.graphql

from datetime import datetime
from decimal import Decimal
from typing import Any, AsyncIterator, Dict, List, Optional, Union

from architect_py.scalars import OrderDir, convert_datetime_to_utc_str, serialize

from .base_model import UNSET, UnsetType
from .cancel_all_orders_mutation import (
    CancelAllOrdersMutation,
    CancelAllOrdersMutationOms,
)
from .cancel_order_mutation import CancelOrderMutation, CancelOrderMutationOms
from .create_jwt import CreateJwt, CreateJwtUser
from .enums import CandleWidth, OrderType, TimeInForce
from .get_account_summaries_query import (
    GetAccountSummariesQuery,
    GetAccountSummariesQueryFolio,
)
from .get_account_summary_query import (
    GetAccountSummaryQuery,
    GetAccountSummaryQueryFolio,
)
from .get_all_open_orders_query import GetAllOpenOrdersQuery, GetAllOpenOrdersQueryOms
from .get_execution_info_query import (
    GetExecutionInfoQuery,
    GetExecutionInfoQuerySymbology,
)
from .get_fills_query import GetFillsQuery, GetFillsQueryFolio
from .get_first_notice_date_query import (
    GetFirstNoticeDateQuery,
    GetFirstNoticeDateQuerySymbology,
)
from .get_future_series_query import GetFutureSeriesQuery, GetFutureSeriesQuerySymbology
from .get_historical_orders_query import (
    GetHistoricalOrdersQuery,
    GetHistoricalOrdersQueryFolio,
)
from .get_l_2_book_snapshot_query import (
    GetL2BookSnapshotQuery,
    GetL2BookSnapshotQueryMarketdata,
)
from .get_market_snapshot_query import (
    GetMarketSnapshotQuery,
    GetMarketSnapshotQueryMarketdata,
)
from .get_market_snapshots_query import (
    GetMarketSnapshotsQuery,
    GetMarketSnapshotsQueryMarketdata,
)
from .get_market_status_query import (
    GetMarketStatusQuery,
    GetMarketStatusQueryMarketdata,
)
from .get_open_orders_query import GetOpenOrdersQuery, GetOpenOrdersQueryOms
from .get_product_info_query import GetProductInfoQuery, GetProductInfoQuerySymbology
from .get_product_infos_query import GetProductInfosQuery, GetProductInfosQuerySymbology
from .juniper_base_client import JuniperBaseClient
from .list_accounts_query import ListAccountsQuery, ListAccountsQueryUser
from .place_order_mutation import PlaceOrderMutation, PlaceOrderMutationOms
from .search_symbols_query import SearchSymbolsQuery, SearchSymbolsQuerySymbology
from .subscribe_candles import SubscribeCandles, SubscribeCandlesCandles
from .subscribe_orderflow import (
    SubscribeOrderflow,
    SubscribeOrderflowOrderflowAberrantFill,
    SubscribeOrderflowOrderflowCancel,
    SubscribeOrderflowOrderflowCancelReject,
    SubscribeOrderflowOrderflowFill,
    SubscribeOrderflowOrderflowGqlOrderReject,
    SubscribeOrderflowOrderflowOrder,
    SubscribeOrderflowOrderflowOrderAck,
    SubscribeOrderflowOrderflowOrderCanceled,
    SubscribeOrderflowOrderflowOrderCanceling,
    SubscribeOrderflowOrderflowOrderOut,
    SubscribeOrderflowOrderflowOrderStale,
)
from .subscribe_trades import SubscribeTrades, SubscribeTradesTrades


def gql(q: str) -> str:
    return q


class GraphQLClient(JuniperBaseClient):
    async def search_symbols_query(
        self,
        search_string: Union[Optional[str], UnsetType] = UNSET,
        execution_venue: Union[Optional[str], UnsetType] = UNSET,
        **kwargs: Any
    ) -> SearchSymbolsQuerySymbology:
        query = gql(
            """
            query SearchSymbolsQuery($searchString: String, $executionVenue: ExecutionVenue) {
              symbology {
                searchSymbols(searchString: $searchString, executionVenue: $executionVenue)
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "searchString": search_string,
            "executionVenue": execution_venue,
        }
        response = await self.execute(
            query=query,
            operation_name="SearchSymbolsQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return SearchSymbolsQuery.model_validate(data).symbology

    async def get_product_info_query(
        self, symbol: str, **kwargs: Any
    ) -> GetProductInfoQuerySymbology:
        query = gql(
            """
            query GetProductInfoQuery($symbol: String!) {
              symbology {
                productInfo(symbol: $symbol) {
                  ...ProductInfoFields
                }
              }
            }

            fragment ProductInfoFields on ProductInfo {
              __typename
              symbol
              productType
              underlying
              multiplier
              derivativeKind
              firstNoticeDate
              primaryVenue
            }
            """
        )
        variables: Dict[str, object] = {"symbol": symbol}
        response = await self.execute(
            query=query,
            operation_name="GetProductInfoQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetProductInfoQuery.model_validate(data).symbology

    async def get_product_infos_query(
        self, symbols: List[str], **kwargs: Any
    ) -> GetProductInfosQuerySymbology:
        query = gql(
            """
            query GetProductInfosQuery($symbols: [String!]!) {
              symbology {
                productInfos(symbols: $symbols) {
                  ...ProductInfoFields
                }
              }
            }

            fragment ProductInfoFields on ProductInfo {
              __typename
              symbol
              productType
              underlying
              multiplier
              derivativeKind
              firstNoticeDate
              primaryVenue
            }
            """
        )
        variables: Dict[str, object] = {"symbols": symbols}
        response = await self.execute(
            query=query,
            operation_name="GetProductInfosQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetProductInfosQuery.model_validate(data).symbology

    async def get_first_notice_date_query(
        self, symbol: str, **kwargs: Any
    ) -> GetFirstNoticeDateQuerySymbology:
        query = gql(
            """
            query GetFirstNoticeDateQuery($symbol: String!) {
              symbology {
                productInfo(symbol: $symbol) {
                  firstNoticeDate
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"symbol": symbol}
        response = await self.execute(
            query=query,
            operation_name="GetFirstNoticeDateQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetFirstNoticeDateQuery.model_validate(data).symbology

    async def get_future_series_query(
        self, series_symbol: str, **kwargs: Any
    ) -> GetFutureSeriesQuerySymbology:
        query = gql(
            """
            query GetFutureSeriesQuery($seriesSymbol: String!) {
              symbology {
                futuresSeries(seriesSymbol: $seriesSymbol)
              }
            }
            """
        )
        variables: Dict[str, object] = {"seriesSymbol": series_symbol}
        response = await self.execute(
            query=query,
            operation_name="GetFutureSeriesQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetFutureSeriesQuery.model_validate(data).symbology

    async def get_execution_info_query(
        self, symbol: str, execution_venue: str, **kwargs: Any
    ) -> GetExecutionInfoQuerySymbology:
        query = gql(
            """
            query GetExecutionInfoQuery($symbol: String!, $executionVenue: ExecutionVenue!) {
              symbology {
                executionInfo(symbol: $symbol, executionVenue: $executionVenue) {
                  ...ExecutionInfoFields
                }
              }
            }

            fragment ExecutionInfoFields on ExecutionInfo {
              symbol
              executionVenue
              tickSize
              stepSize
              minOrderQuantity
              minOrderQuantityUnit
              isDelisted
            }
            """
        )
        variables: Dict[str, object] = {
            "symbol": symbol,
            "executionVenue": execution_venue,
        }
        response = await self.execute(
            query=query,
            operation_name="GetExecutionInfoQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetExecutionInfoQuery.model_validate(data).symbology

    async def get_market_snapshot_query(
        self, symbol: str, venue: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> GetMarketSnapshotQueryMarketdata:
        query = gql(
            """
            query GetMarketSnapshotQuery($venue: MarketdataVenue, $symbol: String!) {
              marketdata {
                ticker(venue: $venue, symbol: $symbol) {
                  ...MarketTickerFields
                }
              }
            }

            fragment MarketTickerFields on Ticker {
              symbol
              timestamp
              bidPrice
              bidSize
              askPrice
              askSize
              lastPrice
              lastSize
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "symbol": symbol}
        response = await self.execute(
            query=query,
            operation_name="GetMarketSnapshotQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetMarketSnapshotQuery.model_validate(data).marketdata

    async def get_market_snapshots_query(
        self,
        venue: str,
        symbols: Union[Optional[List[str]], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetMarketSnapshotsQueryMarketdata:
        query = gql(
            """
            query GetMarketSnapshotsQuery($venue: MarketdataVenue!, $symbols: [String!]) {
              marketdata {
                tickers(venue: $venue, symbols: $symbols) {
                  ...MarketTickerFields
                }
              }
            }

            fragment MarketTickerFields on Ticker {
              symbol
              timestamp
              bidPrice
              bidSize
              askPrice
              askSize
              lastPrice
              lastSize
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "symbols": symbols}
        response = await self.execute(
            query=query,
            operation_name="GetMarketSnapshotsQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetMarketSnapshotsQuery.model_validate(data).marketdata

    async def get_market_status_query(
        self, symbol: str, venue: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> GetMarketStatusQueryMarketdata:
        query = gql(
            """
            query GetMarketStatusQuery($venue: MarketdataVenue, $symbol: String!) {
              marketdata {
                marketStatus(venue: $venue, symbol: $symbol) {
                  ...MarketStatusFields
                }
              }
            }

            fragment MarketStatusFields on MarketStatus {
              symbol
              isTrading
              isQuoting
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "symbol": symbol}
        response = await self.execute(
            query=query,
            operation_name="GetMarketStatusQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetMarketStatusQuery.model_validate(data).marketdata

    async def list_accounts_query(self, **kwargs: Any) -> ListAccountsQueryUser:
        query = gql(
            """
            query ListAccountsQuery {
              user {
                accounts {
                  ...AccountWithPermissionsFields
                }
              }
            }

            fragment AccountWithPermissionsFields on AccountWithPermissions {
              account {
                id
                name
              }
              trader
              permissions {
                list
                view
                trade
                reduceOrClose
                setLimits
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="ListAccountsQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return ListAccountsQuery.model_validate(data).user

    async def get_account_summary_query(
        self,
        account: str,
        venue: Union[Optional[str], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetAccountSummaryQueryFolio:
        query = gql(
            """
            query GetAccountSummaryQuery($venue: ExecutionVenue, $account: String!) {
              folio {
                accountSummary(venue: $venue, account: $account) {
                  ...AccountSummaryFields
                }
              }
            }

            fragment AccountSummaryFields on AccountSummary {
              account
              timestamp
              balances {
                product
                balance
              }
              positions {
                symbol
                quantity
                tradeTime
                costBasis
                breakEvenPrice
                liquidationPrice
              }
              unrealizedPnl
              realizedPnl
              equity
              yesterdayEquity
              cashExcess
              purchasingPower
              totalMargin
              positionMargin
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "account": account}
        response = await self.execute(
            query=query,
            operation_name="GetAccountSummaryQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAccountSummaryQuery.model_validate(data).folio

    async def get_account_summaries_query(
        self,
        venue: Union[Optional[str], UnsetType] = UNSET,
        trader: Union[Optional[str], UnsetType] = UNSET,
        accounts: Union[Optional[List[str]], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetAccountSummariesQueryFolio:
        query = gql(
            """
            query GetAccountSummariesQuery($venue: ExecutionVenue, $trader: String, $accounts: [String!]) {
              folio {
                accountSummaries(venue: $venue, trader: $trader, accounts: $accounts) {
                  ...AccountSummaryFields
                }
              }
            }

            fragment AccountSummaryFields on AccountSummary {
              account
              timestamp
              balances {
                product
                balance
              }
              positions {
                symbol
                quantity
                tradeTime
                costBasis
                breakEvenPrice
                liquidationPrice
              }
              unrealizedPnl
              realizedPnl
              equity
              yesterdayEquity
              cashExcess
              purchasingPower
              totalMargin
              positionMargin
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "trader": trader,
            "accounts": accounts,
        }
        response = await self.execute(
            query=query,
            operation_name="GetAccountSummariesQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAccountSummariesQuery.model_validate(data).folio

    async def get_open_orders_query(
        self,
        venue: Union[Optional[str], UnsetType] = UNSET,
        account: Union[Optional[str], UnsetType] = UNSET,
        trader: Union[Optional[str], UnsetType] = UNSET,
        symbol: Union[Optional[str], UnsetType] = UNSET,
        parent_order_id: Union[Optional[str], UnsetType] = UNSET,
        order_ids: Union[Optional[List[str]], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetOpenOrdersQueryOms:
        query = gql(
            """
            query GetOpenOrdersQuery($venue: ExecutionVenue, $account: String, $trader: String, $symbol: String, $parentOrderId: OrderId, $orderIds: [OrderId!]) {
              oms {
                openOrders(
                  venue: $venue
                  account: $account
                  trader: $trader
                  symbol: $symbol
                  parentOrderId: $parentOrderId
                  orderIds: $orderIds
                ) {
                  ...OrderFields
                }
              }
            }

            fragment OrderFields on Order {
              id
              parentId
              recvTime
              status
              rejectReason
              rejectMessage
              symbol
              trader
              account
              dir
              quantity
              filledQuantity
              averageFillPrice
              orderType
              limitPrice
              postOnly
              triggerPrice
              timeInForce
              goodTilDate
              source
              executionVenue
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "account": account,
            "trader": trader,
            "symbol": symbol,
            "parentOrderId": parent_order_id,
            "orderIds": order_ids,
        }
        response = await self.execute(
            query=query,
            operation_name="GetOpenOrdersQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetOpenOrdersQuery.model_validate(data).oms

    async def get_all_open_orders_query(
        self, **kwargs: Any
    ) -> GetAllOpenOrdersQueryOms:
        query = gql(
            """
            query GetAllOpenOrdersQuery {
              oms {
                openOrders {
                  ...OrderFields
                }
              }
            }

            fragment OrderFields on Order {
              id
              parentId
              recvTime
              status
              rejectReason
              rejectMessage
              symbol
              trader
              account
              dir
              quantity
              filledQuantity
              averageFillPrice
              orderType
              limitPrice
              postOnly
              triggerPrice
              timeInForce
              goodTilDate
              source
              executionVenue
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAllOpenOrdersQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAllOpenOrdersQuery.model_validate(data).oms

    async def get_historical_orders_query(
        self,
        from_inclusive: datetime,
        to_exclusive: datetime,
        venue: Union[Optional[str], UnsetType] = UNSET,
        account: Union[Optional[str], UnsetType] = UNSET,
        parent_order_id: Union[Optional[str], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetHistoricalOrdersQueryFolio:
        query = gql(
            """
            query GetHistoricalOrdersQuery($venue: ExecutionVenue, $account: String, $parentOrderId: OrderId, $fromInclusive: DateTime!, $toExclusive: DateTime!) {
              folio {
                historicalOrders(
                  venue: $venue
                  account: $account
                  parentOrderId: $parentOrderId
                  fromInclusive: $fromInclusive
                  toExclusive: $toExclusive
                ) {
                  ...OrderFields
                }
              }
            }

            fragment OrderFields on Order {
              id
              parentId
              recvTime
              status
              rejectReason
              rejectMessage
              symbol
              trader
              account
              dir
              quantity
              filledQuantity
              averageFillPrice
              orderType
              limitPrice
              postOnly
              triggerPrice
              timeInForce
              goodTilDate
              source
              executionVenue
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "account": account,
            "parentOrderId": parent_order_id,
            "fromInclusive": convert_datetime_to_utc_str(from_inclusive),
            "toExclusive": convert_datetime_to_utc_str(to_exclusive),
        }
        response = await self.execute(
            query=query,
            operation_name="GetHistoricalOrdersQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetHistoricalOrdersQuery.model_validate(data).folio

    async def get_fills_query(
        self,
        venue: Union[Optional[str], UnsetType] = UNSET,
        account: Union[Optional[str], UnsetType] = UNSET,
        order_id: Union[Optional[str], UnsetType] = UNSET,
        from_inclusive: Union[Optional[datetime], UnsetType] = UNSET,
        to_exclusive: Union[Optional[datetime], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetFillsQueryFolio:
        query = gql(
            """
            query GetFillsQuery($venue: ExecutionVenue, $account: String, $orderId: OrderId, $fromInclusive: DateTime, $toExclusive: DateTime) {
              folio {
                historicalFills(
                  venue: $venue
                  account: $account
                  orderId: $orderId
                  fromInclusive: $fromInclusive
                  toExclusive: $toExclusive
                ) {
                  fills {
                    fillId
                    fillKind
                    executionVenue
                    exchangeFillId
                    orderId
                    trader
                    account
                    symbol
                    dir
                    quantity
                    price
                    recvTime
                    tradeTime
                  }
                  aberrantFills {
                    fillId
                    fillKind
                    executionVenue
                    exchangeFillId
                    orderId
                    trader
                    account
                    symbol
                    dir
                    quantity
                    price
                    recvTime
                    tradeTime
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "account": account,
            "orderId": order_id,
            "fromInclusive": convert_datetime_to_utc_str(from_inclusive),
            "toExclusive": convert_datetime_to_utc_str(to_exclusive),
        }
        response = await self.execute(
            query=query, operation_name="GetFillsQuery", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetFillsQuery.model_validate(data).folio

    async def get_l_2_book_snapshot_query(
        self, symbol: str, venue: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> GetL2BookSnapshotQueryMarketdata:
        query = gql(
            """
            query GetL2BookSnapshotQuery($venue: MarketdataVenue, $symbol: String!) {
              marketdata {
                l2BookSnapshot(venue: $venue, symbol: $symbol) {
                  ...L2BookFields
                }
              }
            }

            fragment L2BookFields on L2Book {
              timestamp
              bids {
                ...L2BookLevelFields
              }
              asks {
                ...L2BookLevelFields
              }
            }

            fragment L2BookLevelFields on L2BookLevel {
              price
              size
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "symbol": symbol}
        response = await self.execute(
            query=query,
            operation_name="GetL2BookSnapshotQuery",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetL2BookSnapshotQuery.model_validate(data).marketdata

    async def subscribe_trades(
        self, venue: str, symbol: str, **kwargs: Any
    ) -> AsyncIterator[SubscribeTradesTrades]:
        query = gql(
            """
            subscription SubscribeTrades($venue: MarketdataVenue!, $symbol: String!) {
              trades(venue: $venue, symbol: $symbol) {
                timestamp
                direction
                price
                size
              }
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "symbol": symbol}
        async for data in self.execute_ws(
            query=query, operation_name="SubscribeTrades", variables=variables, **kwargs
        ):
            yield SubscribeTrades.model_validate(data).trades

    async def subscribe_candles(
        self,
        venue: str,
        symbol: str,
        widths: Union[Optional[List[CandleWidth]], UnsetType] = UNSET,
        **kwargs: Any
    ) -> AsyncIterator[SubscribeCandlesCandles]:
        query = gql(
            """
            subscription SubscribeCandles($venue: MarketdataVenue!, $symbol: String!, $widths: [CandleWidth!]) {
              candles(venue: $venue, symbol: $symbol, candleWidths: $widths) {
                ...CandleFields
              }
            }

            fragment CandleFields on Candle {
              timestamp
              width
              open
              high
              low
              close
              volume
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "symbol": symbol,
            "widths": widths,
        }
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeCandles",
            variables=variables,
            **kwargs
        ):
            yield SubscribeCandles.model_validate(data).candles

    async def cancel_order_mutation(
        self, order_id: str, **kwargs: Any
    ) -> CancelOrderMutationOms:
        query = gql(
            """
            mutation CancelOrderMutation($orderId: OrderId!) {
              oms {
                cancelOrder(orderId: $orderId) {
                  ...CancelFields
                }
              }
            }

            fragment CancelFields on Cancel {
              cancelId
              orderId
              recvTime
              status
              rejectReason
            }
            """
        )
        variables: Dict[str, object] = {"orderId": order_id}
        response = await self.execute(
            query=query,
            operation_name="CancelOrderMutation",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CancelOrderMutation.model_validate(data).oms

    async def cancel_all_orders_mutation(
        self, **kwargs: Any
    ) -> CancelAllOrdersMutationOms:
        query = gql(
            """
            mutation CancelAllOrdersMutation {
              oms {
                cancelAllOrders
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="CancelAllOrdersMutation",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CancelAllOrdersMutation.model_validate(data).oms

    async def place_order_mutation(
        self,
        symbol: str,
        dir: OrderDir,
        quantity: Decimal,
        order_type: OrderType,
        time_in_force: TimeInForce,
        id: Union[Optional[str], UnsetType] = UNSET,
        trader: Union[Optional[str], UnsetType] = UNSET,
        account: Union[Optional[str], UnsetType] = UNSET,
        limit_price: Union[Optional[Decimal], UnsetType] = UNSET,
        post_only: Union[Optional[bool], UnsetType] = UNSET,
        trigger_price: Union[Optional[Decimal], UnsetType] = UNSET,
        good_til_date: Union[Optional[datetime], UnsetType] = UNSET,
        execution_venue: Union[Optional[str], UnsetType] = UNSET,
        **kwargs: Any
    ) -> PlaceOrderMutationOms:
        query = gql(
            """
            mutation PlaceOrderMutation($id: OrderId, $symbol: String!, $dir: Dir!, $quantity: Decimal!, $trader: String, $account: String, $orderType: OrderType!, $limitPrice: Decimal, $postOnly: Boolean, $triggerPrice: Decimal, $timeInForce: TimeInForce!, $goodTilDate: DateTime, $executionVenue: ExecutionVenue) {
              oms {
                placeOrder(
                  id: $id
                  symbol: $symbol
                  dir: $dir
                  quantity: $quantity
                  trader: $trader
                  account: $account
                  orderType: $orderType
                  limitPrice: $limitPrice
                  postOnly: $postOnly
                  triggerPrice: $triggerPrice
                  timeInForce: $timeInForce
                  goodTilDate: $goodTilDate
                  executionVenue: $executionVenue
                ) {
                  ...OrderFields
                }
              }
            }

            fragment OrderFields on Order {
              id
              parentId
              recvTime
              status
              rejectReason
              rejectMessage
              symbol
              trader
              account
              dir
              quantity
              filledQuantity
              averageFillPrice
              orderType
              limitPrice
              postOnly
              triggerPrice
              timeInForce
              goodTilDate
              source
              executionVenue
            }
            """
        )
        variables: Dict[str, object] = {
            "id": id,
            "symbol": symbol,
            "dir": serialize(dir),
            "quantity": quantity,
            "trader": trader,
            "account": account,
            "orderType": order_type,
            "limitPrice": limit_price,
            "postOnly": post_only,
            "triggerPrice": trigger_price,
            "timeInForce": time_in_force,
            "goodTilDate": convert_datetime_to_utc_str(good_til_date),
            "executionVenue": execution_venue,
        }
        response = await self.execute(
            query=query,
            operation_name="PlaceOrderMutation",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return PlaceOrderMutation.model_validate(data).oms

    async def subscribe_orderflow(self, **kwargs: Any) -> AsyncIterator[
        Union[
            SubscribeOrderflowOrderflowOrder,
            SubscribeOrderflowOrderflowOrderAck,
            SubscribeOrderflowOrderflowGqlOrderReject,
            SubscribeOrderflowOrderflowOrderOut,
            SubscribeOrderflowOrderflowOrderStale,
            SubscribeOrderflowOrderflowCancel,
            SubscribeOrderflowOrderflowCancelReject,
            SubscribeOrderflowOrderflowOrderCanceling,
            SubscribeOrderflowOrderflowOrderCanceled,
            SubscribeOrderflowOrderflowFill,
            SubscribeOrderflowOrderflowAberrantFill,
        ]
    ]:
        query = gql(
            """
            subscription SubscribeOrderflow {
              orderflow {
                __typename
                ... on Order {
                  ...OrderFields
                }
                ... on OrderAck {
                  orderId
                }
                ... on OrderCanceled {
                  orderId
                  cancelId
                }
                ... on GqlOrderReject {
                  orderId
                  reason
                  message
                }
                ... on CancelReject {
                  orderId
                  message
                }
                ... on Fill {
                  fillOrderId: orderId
                  fillId
                  fillKind
                  executionVenue
                  exchangeFillId
                  symbol
                  dir
                  quantity
                  price
                  recvTime
                  tradeTime
                }
                ... on OrderOut {
                  orderId
                }
                ... on OrderStale {
                  orderId
                }
              }
            }

            fragment OrderFields on Order {
              id
              parentId
              recvTime
              status
              rejectReason
              rejectMessage
              symbol
              trader
              account
              dir
              quantity
              filledQuantity
              averageFillPrice
              orderType
              limitPrice
              postOnly
              triggerPrice
              timeInForce
              goodTilDate
              source
              executionVenue
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeOrderflow",
            variables=variables,
            **kwargs
        ):
            yield SubscribeOrderflow.model_validate(data).orderflow

    async def create_jwt(self, **kwargs: Any) -> CreateJwtUser:
        query = gql(
            """
            mutation CreateJwt {
              user {
                createJwt
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="CreateJwt", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CreateJwt.model_validate(data).user
