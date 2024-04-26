# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, AsyncIterator, Dict, List, Optional, Union

from .base_model import UNSET, UnsetType
from .cancel_order import CancelOrder
from .enums import CandleWidth
from .fills_subscription import FillsSubscription
from .get_all_market_snapshots import GetAllMarketSnapshots
from .get_balances_for_cpty import GetBalancesForCpty
from .get_fills import GetFills
from .get_filtered_markets import GetFilteredMarkets
from .get_market import GetMarket
from .get_market_snapshot import GetMarketSnapshot
from .get_markets import GetMarkets
from .get_open_orders import GetOpenOrders
from .get_order import GetOrder
from .get_out_orders import GetOutOrders
from .input_types import CreateOrder
from .juniper_async_base_client import JuniperAsyncBaseClient
from .send_order import SendOrder
from .subscribe_book import SubscribeBook
from .subscribe_candles import SubscribeCandles
from .subscribe_exchange_specific import SubscribeExchangeSpecific
from .subscribe_trades import SubscribeTrades


def gql(q: str) -> str:
    return q


class GraphQLClient(JuniperAsyncBaseClient):
    async def get_market(self, id: Any, **kwargs: Any) -> GetMarket:
        query = gql(
            """
            query GetMarket($id: MarketId!) {
              market(id: $id) {
                ...MarketFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="GetMarket", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetMarket.model_validate(data)

    async def get_markets(self, ids: List[Any], **kwargs: Any) -> GetMarkets:
        query = gql(
            """
            query GetMarkets($ids: [MarketId!]!) {
              markets(id: $ids) {
                ...MarketFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {"ids": ids}
        response = await self.execute(
            query=query, operation_name="GetMarkets", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetMarkets.model_validate(data)

    async def get_filtered_markets(
        self,
        venue: Union[Optional[Any], UnsetType] = UNSET,
        base: Union[Optional[Any], UnsetType] = UNSET,
        quote: Union[Optional[Any], UnsetType] = UNSET,
        underlying: Union[Optional[Any], UnsetType] = UNSET,
        max_results: Union[Optional[int], UnsetType] = UNSET,
        results_offset: Union[Optional[int], UnsetType] = UNSET,
        search_string: Union[Optional[Any], UnsetType] = UNSET,
        only_favorites: Union[Optional[bool], UnsetType] = UNSET,
        sort_by_volume_desc: Union[Optional[bool], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetFilteredMarkets:
        query = gql(
            """
            query GetFilteredMarkets($venue: Str, $base: Str, $quote: Str, $underlying: Str, $maxResults: Int, $resultsOffset: Int, $searchString: Str, $onlyFavorites: Boolean, $sortByVolumeDesc: Boolean) {
              filterMarkets(
                filter: {venue: $venue, base: $base, quote: $quote, underlying: $underlying, maxResults: $maxResults, resultsOffset: $resultsOffset, searchString: $searchString, onlyFavorites: $onlyFavorites, sortByVolumeDesc: $sortByVolumeDesc}
              ) {
                ...MarketFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "base": base,
            "quote": quote,
            "underlying": underlying,
            "maxResults": max_results,
            "resultsOffset": results_offset,
            "searchString": search_string,
            "onlyFavorites": only_favorites,
            "sortByVolumeDesc": sort_by_volume_desc,
        }
        response = await self.execute(
            query=query,
            operation_name="GetFilteredMarkets",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetFilteredMarkets.model_validate(data)

    async def get_market_snapshot(self, id: Any, **kwargs: Any) -> GetMarketSnapshot:
        query = gql(
            """
            query GetMarketSnapshot($id: MarketId!) {
              marketSnapshot(market: $id) {
                ...MarketSnapshotFields
              }
            }

            fragment MarketSnapshotFields on MarketSnapshot {
              __typename
              marketId
              market {
                name
              }
              high24h
              lastPrice
              low24h
              volume24h
              open24h
              bidPrice
              askPrice
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query,
            operation_name="GetMarketSnapshot",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetMarketSnapshot.model_validate(data)

    async def get_all_market_snapshots(self, **kwargs: Any) -> GetAllMarketSnapshots:
        query = gql(
            """
            query GetAllMarketSnapshots {
              marketsSnapshots {
                ...MarketSnapshotFields
              }
            }

            fragment MarketSnapshotFields on MarketSnapshot {
              __typename
              marketId
              market {
                name
              }
              high24h
              lastPrice
              low24h
              volume24h
              open24h
              bidPrice
              askPrice
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAllMarketSnapshots",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAllMarketSnapshots.model_validate(data)

    async def get_balances_for_cpty(
        self, venue: Any, route: Any, **kwargs: Any
    ) -> GetBalancesForCpty:
        query = gql(
            """
            query GetBalancesForCpty($venue: VenueId!, $route: RouteId!) {
              balancesForCpty(venue: $venue, route: $route) {
                snapshotTs
                product {
                  ...ProductFields
                }
                amount
              }
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {"venue": venue, "route": route}
        response = await self.execute(
            query=query,
            operation_name="GetBalancesForCpty",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetBalancesForCpty.model_validate(data)

    async def get_open_orders(self, **kwargs: Any) -> GetOpenOrders:
        query = gql(
            """
            query GetOpenOrders {
              openOrders {
                ...OrderLogFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment OrderLogFields on OrderLog {
              __typename
              timestamp
              order {
                id
                market {
                  ...MarketFields
                }
                dir
                quantity
              }
              orderState
              filledQty
              avgFillPrice
              rejectReason
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="GetOpenOrders", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetOpenOrders.model_validate(data)

    async def get_out_orders(
        self, from_inclusive: Any, to_exclusive: Any, **kwargs: Any
    ) -> GetOutOrders:
        query = gql(
            """
            query GetOutOrders($fromInclusive: DateTime!, $toExclusive: DateTime!) {
              outedOrders(fromInclusive: $fromInclusive, toExclusive: $toExclusive) {
                ...OrderLogFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment OrderLogFields on OrderLog {
              __typename
              timestamp
              order {
                id
                market {
                  ...MarketFields
                }
                dir
                quantity
              }
              orderState
              filledQty
              avgFillPrice
              rejectReason
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {
            "fromInclusive": from_inclusive,
            "toExclusive": to_exclusive,
        }
        response = await self.execute(
            query=query, operation_name="GetOutOrders", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetOutOrders.model_validate(data)

    async def get_order(self, order_id: Any, **kwargs: Any) -> GetOrder:
        query = gql(
            """
            query GetOrder($orderId: OrderId!) {
              order(orderId: $orderId) {
                ...OrderLogFields
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment OrderLogFields on OrderLog {
              __typename
              timestamp
              order {
                id
                market {
                  ...MarketFields
                }
                dir
                quantity
              }
              orderState
              filledQty
              avgFillPrice
              rejectReason
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {"orderId": order_id}
        response = await self.execute(
            query=query, operation_name="GetOrder", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetOrder.model_validate(data)

    async def get_fills(
        self,
        venue: Union[Optional[Any], UnsetType] = UNSET,
        route: Union[Optional[Any], UnsetType] = UNSET,
        base: Union[Optional[Any], UnsetType] = UNSET,
        quote: Union[Optional[Any], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetFills:
        query = gql(
            """
            query GetFills($venue: VenueId, $route: RouteId, $base: ProductId, $quote: ProductId) {
              fills(venue: $venue, route: $route, base: $base, quote: $quote) {
                normal {
                  kind
                  fillId
                  orderId
                  market {
                    ...MarketFields
                  }
                  dir
                  price
                  quantity
                  recvTime
                  tradeTime
                }
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {
            "venue": venue,
            "route": route,
            "base": base,
            "quote": quote,
        }
        response = await self.execute(
            query=query, operation_name="GetFills", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetFills.model_validate(data)

    async def subscribe_trades(
        self, market: Any, **kwargs: Any
    ) -> AsyncIterator[SubscribeTrades]:
        query = gql(
            """
            subscription SubscribeTrades($market: MarketId!) {
              trades(market: $market) {
                time
                price
                size
                direction
              }
            }
            """
        )
        variables: Dict[str, object] = {"market": market}
        async for data in self.execute_ws(
            query=query, operation_name="SubscribeTrades", variables=variables, **kwargs
        ):
            yield SubscribeTrades.model_validate(data)

    async def subscribe_candles(
        self, id: Any, width: CandleWidth, **kwargs: Any
    ) -> AsyncIterator[SubscribeCandles]:
        query = gql(
            """
            subscription SubscribeCandles($id: MarketId!, $width: CandleWidth!) {
              candles(market: $id, candleWidth: $width) {
                ...CandleFields
              }
            }

            fragment CandleFields on CandleV1 {
              time
              open
              high
              low
              close
              volume
            }
            """
        )
        variables: Dict[str, object] = {"id": id, "width": width}
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeCandles",
            variables=variables,
            **kwargs
        ):
            yield SubscribeCandles.model_validate(data)

    async def fills_subscription(
        self, **kwargs: Any
    ) -> AsyncIterator[FillsSubscription]:
        query = gql(
            """
            subscription FillsSubscription {
              fills {
                dir
                fillId
                kind
                marketId
                orderId
                price
                quantity
                recvTime
                tradeTime
                market {
                  ...MarketFields
                }
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=query,
            operation_name="FillsSubscription",
            variables=variables,
            **kwargs
        ):
            yield FillsSubscription.model_validate(data)

    async def subscribe_book(
        self, id: Any, precision: Union[Optional[Any], UnsetType] = UNSET, **kwargs: Any
    ) -> AsyncIterator[SubscribeBook]:
        query = gql(
            """
            subscription SubscribeBook($id: MarketId!, $precision: Decimal) {
              book(market: $id, precision: $precision) {
                bids {
                  price
                  amount
                  total
                }
                asks {
                  price
                  amount
                  total
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id, "precision": precision}
        async for data in self.execute_ws(
            query=query, operation_name="SubscribeBook", variables=variables, **kwargs
        ):
            yield SubscribeBook.model_validate(data)

    async def subscribe_exchange_specific(
        self, markets: List[Any], fields: List[str], **kwargs: Any
    ) -> AsyncIterator[SubscribeExchangeSpecific]:
        query = gql(
            """
            subscription SubscribeExchangeSpecific($markets: [MarketId!]!, $fields: [String!]!) {
              exchangeSpecific(markets: $markets, fields: $fields) {
                market {
                  ...MarketFields
                }
                field
                value
              }
            }

            fragment MarketFields on Market {
              __typename
              venue {
                id
                name
              }
              exchangeSymbol
              id
              kind {
                ... on ExchangeMarketKind {
                  __typename
                  base {
                    ...ProductFields
                  }
                  quote {
                    ...ProductFields
                  }
                }
                ... on PoolMarketKind {
                  __typename
                  products {
                    ...ProductFields
                  }
                }
              }
              name
              tickSize
              stepSize
              route {
                id
                name
              }
              isFavorite
            }

            fragment ProductFields on Product {
              __typename
              id
              name
              kind
              markUsd
            }
            """
        )
        variables: Dict[str, object] = {"markets": markets, "fields": fields}
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeExchangeSpecific",
            variables=variables,
            **kwargs
        ):
            yield SubscribeExchangeSpecific.model_validate(data)

    async def send_order(self, order: CreateOrder, **kwargs: Any) -> SendOrder:
        query = gql(
            """
            mutation SendOrder($order: CreateOrder!) {
              createOrder(order: $order)
            }
            """
        )
        variables: Dict[str, object] = {"order": order}
        response = await self.execute(
            query=query, operation_name="SendOrder", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return SendOrder.model_validate(data)

    async def cancel_order(self, order_id: Any, **kwargs: Any) -> CancelOrder:
        query = gql(
            """
            mutation CancelOrder($orderId: OrderId!) {
              cancelOrder(orderId: $orderId)
            }
            """
        )
        variables: Dict[str, object] = {"orderId": order_id}
        response = await self.execute(
            query=query, operation_name="CancelOrder", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CancelOrder.model_validate(data)
