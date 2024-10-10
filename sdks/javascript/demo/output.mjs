/**
 * Temp file for iteratively building the JS SDK codegen
 */
import { client, graphql } from './client.mjs';


/**
 * @typedef {import('../src/graphql/graphql.ts').Scalars['AccountId']['output']} AccountId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Boolean']['output']} Boolean - The `Boolean` scalar type represents `true` or `false`.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['ComponentId']['output']} ComponentId - Components within an Architect installation are uniquely identified by a 16-bit integer
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Date']['output']} Date - Date in the proleptic Gregorian calendar (without time zone).
 * @typedef {import('../src/graphql/graphql.ts').Scalars['DateTime']['output']} DateTime - Combined date and time (with time zone) in [RFC 3339][0] format.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Decimal']['output']} Decimal - 128 bit representation of a fixed-precision decimal number.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Dir']['output']} Dir - An order side/direction or a trade execution side/direction.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['FillId']['output']} FillId - The ID of a fill
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Float']['output']} Float - The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Int']['output']} Int - The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['MarketId']['output']} MarketId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef {import('../src/graphql/graphql.ts').Scalars['OrderId']['output']} OrderId - System-unique, persistent order identifiers
 * @typedef {import('../src/graphql/graphql.ts').Scalars['ProductId']['output']} ProductId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef {import('../src/graphql/graphql.ts').Scalars['RouteId']['output']} RouteId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef {import('../src/graphql/graphql.ts').Scalars['Str']['output']} Str - A String type
 * @typedef {import('../src/graphql/graphql.ts').Scalars['String']['output']} String - The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
 * @typedef {import('../src/graphql/graphql.ts').Scalars['UserId']['output']} UserId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef {import('../src/graphql/graphql.ts').Scalars['VenueId']['output']} VenueId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * * @typedef {import('../src/graphql/graphql.ts').AberrantFill} AberrantFill - Fills which we received but couldn't parse fully, return details
 * @typedef {import('../src/graphql/graphql.ts').Account} Account
 * @typedef {import('../src/graphql/graphql.ts').AccountSummaries} AccountSummaries
 * @typedef {import('../src/graphql/graphql.ts').AccountSummary} AccountSummary
 * @typedef {import('../src/graphql/graphql.ts').Ack} Ack
 * @typedef {import('../src/graphql/graphql.ts').AlgoControlCommand} AlgoControlCommand
 * @typedef {import('../src/graphql/graphql.ts').AlgoKind} AlgoKind
 * @typedef {import('../src/graphql/graphql.ts').AlgoLog} AlgoLog
 * @typedef {import('../src/graphql/graphql.ts').AlgoOrder} AlgoOrder
 * @typedef {import('../src/graphql/graphql.ts').AlgoPreview} AlgoPreview
 * @typedef {import('../src/graphql/graphql.ts').AlgoRunningStatus} AlgoRunningStatus
 * @typedef {import('../src/graphql/graphql.ts').AlgoStatus} AlgoStatus
 * @typedef {import('../src/graphql/graphql.ts').ApiKey} ApiKey
 * @typedef {import('../src/graphql/graphql.ts').Balance} Balance
 * @typedef {import('../src/graphql/graphql.ts').Book} Book
 * @typedef {import('../src/graphql/graphql.ts').BookLevel} BookLevel
 * @typedef {import('../src/graphql/graphql.ts').Cancel} Cancel
 * @typedef {import('../src/graphql/graphql.ts').CancelAll} CancelAll
 * @typedef {import('../src/graphql/graphql.ts').CandleV1} CandleV1 - NB: buy_volume + sell_volume <> volume; volume may count trades
 * @typedef {import('../src/graphql/graphql.ts').CandleWidth} CandleWidth
 * @typedef {import('../src/graphql/graphql.ts').CmeProductGroupInfo} CmeProductGroupInfo
 * @typedef {import('../src/graphql/graphql.ts').CmeSecurityType} CmeSecurityType
 * @typedef {import('../src/graphql/graphql.ts').CoinInfo} CoinInfo
 * @typedef {import('../src/graphql/graphql.ts').CptyInfo} CptyInfo
 * @typedef {import('../src/graphql/graphql.ts').CreateMMAlgo} CreateMMAlgo
 * @typedef {import('../src/graphql/graphql.ts').CreateOrder} CreateOrder
 * @typedef {import('../src/graphql/graphql.ts').CreateOrderType} CreateOrderType
 * @typedef {import('../src/graphql/graphql.ts').CreatePovAlgo} CreatePovAlgo
 * @typedef {import('../src/graphql/graphql.ts').CreateSmartOrderRouterAlgo} CreateSmartOrderRouterAlgo
 * @typedef {import('../src/graphql/graphql.ts').CreateSpreadAlgo} CreateSpreadAlgo
 * @typedef {import('../src/graphql/graphql.ts').CreateSpreadAlgoHedgeMarket} CreateSpreadAlgoHedgeMarket
 * @typedef {import('../src/graphql/graphql.ts').CreateTimeInForce} CreateTimeInForce
 * @typedef {import('../src/graphql/graphql.ts').CreateTimeInForceInstruction} CreateTimeInForceInstruction
 * @typedef {import('../src/graphql/graphql.ts').CreateTwapAlgo} CreateTwapAlgo
 * @typedef {import('../src/graphql/graphql.ts').Environment} Environment
 * @typedef {import('../src/graphql/graphql.ts').EnvironmentKind} EnvironmentKind
 * @typedef {import('../src/graphql/graphql.ts').ExchangeMarketKind} ExchangeMarketKind
 * @typedef {import('../src/graphql/graphql.ts').ExchangeSpecificUpdate} ExchangeSpecificUpdate
 * @typedef {import('../src/graphql/graphql.ts').Fee} Fee
 * @typedef {import('../src/graphql/graphql.ts').Fill} Fill
 * @typedef {import('../src/graphql/graphql.ts').FillKind} FillKind
 * @typedef {import('../src/graphql/graphql.ts').Fills} Fills
 * @typedef {import('../src/graphql/graphql.ts').HedgeMarket} HedgeMarket
 * @typedef {import('../src/graphql/graphql.ts').License} License
 * @typedef {import('../src/graphql/graphql.ts').LicenseTier} LicenseTier
 * @typedef {import('../src/graphql/graphql.ts').LimitOrderType} LimitOrderType
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoDecision} MMAlgoDecision
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoDecisionCancel} MMAlgoDecisionCancel
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoDecisionDoNothing} MMAlgoDecisionDoNothing
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoDecisionSend} MMAlgoDecisionSend
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoKind} MMAlgoKind
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoOpenOrder} MMAlgoOpenOrder
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoOrder} MMAlgoOrder
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoSide} MMAlgoSide
 * @typedef {import('../src/graphql/graphql.ts').MMAlgoStatus} MMAlgoStatus
 * @typedef {import('../src/graphql/graphql.ts').Market} Market
 * @typedef {import('../src/graphql/graphql.ts').MarketFilter} MarketFilter
 * @typedef {import('../src/graphql/graphql.ts').MarketKind} MarketKind
 * @typedef {import('../src/graphql/graphql.ts').MarketSnapshot} MarketSnapshot
 * @typedef {import('../src/graphql/graphql.ts').Me} Me
 * @typedef {import('../src/graphql/graphql.ts').MinOrderQuantityUnit} MinOrderQuantityUnit
 * @typedef {import('../src/graphql/graphql.ts').MutationRoot} MutationRoot
 * @typedef {import('../src/graphql/graphql.ts').OmsOrderUpdate} OmsOrderUpdate
 * @typedef {import('../src/graphql/graphql.ts').OptionsMarketSnapshot} OptionsMarketSnapshot
 * @typedef {import('../src/graphql/graphql.ts').Order} Order
 * @typedef {import('../src/graphql/graphql.ts').OrderLog} OrderLog
 * @typedef {import('../src/graphql/graphql.ts').OrderSource} OrderSource
 * @typedef {import('../src/graphql/graphql.ts').OrderStateFlags} OrderStateFlags - The state of an order
 * @typedef {import('../src/graphql/graphql.ts').OrderType} OrderType
 * @typedef {import('../src/graphql/graphql.ts').Orderflow} Orderflow
 * @typedef {import('../src/graphql/graphql.ts').Out} Out
 * @typedef {import('../src/graphql/graphql.ts').PoolMarketKind} PoolMarketKind
 * @typedef {import('../src/graphql/graphql.ts').Position} Position
 * @typedef {import('../src/graphql/graphql.ts').PovAlgoOrder} PovAlgoOrder
 * @typedef {import('../src/graphql/graphql.ts').PovAlgoStatus} PovAlgoStatus
 * @typedef {import('../src/graphql/graphql.ts').Product} Product
 * @typedef {import('../src/graphql/graphql.ts').QueryRoot} QueryRoot
 * @typedef {import('../src/graphql/graphql.ts').Reason} Reason
 * @typedef {import('../src/graphql/graphql.ts').ReferencePrice} ReferencePrice
 * @typedef {import('../src/graphql/graphql.ts').Reject} Reject
 * @typedef {import('../src/graphql/graphql.ts').RfqResponse} RfqResponse
 * @typedef {import('../src/graphql/graphql.ts').RfqResponseSide} RfqResponseSide
 * @typedef {import('../src/graphql/graphql.ts').Route} Route
 * @typedef {import('../src/graphql/graphql.ts').SmartOrderRouterOrder} SmartOrderRouterOrder
 * @typedef {import('../src/graphql/graphql.ts').SmartOrderRouterStatus} SmartOrderRouterStatus
 * @typedef {import('../src/graphql/graphql.ts').StopLossLimitOrderType} StopLossLimitOrderType
 * @typedef {import('../src/graphql/graphql.ts').SubscriptionRoot} SubscriptionRoot
 * @typedef {import('../src/graphql/graphql.ts').TakeProfitLimitOrderType} TakeProfitLimitOrderType
 * @typedef {import('../src/graphql/graphql.ts').TcaBalancePnlV1} TcaBalancePnlV1
 * @typedef {import('../src/graphql/graphql.ts').TcaData} TcaData
 * @typedef {import('../src/graphql/graphql.ts').TcaMarksV1} TcaMarksV1
 * @typedef {import('../src/graphql/graphql.ts').TcaPnlV1} TcaPnlV1
 * @typedef {import('../src/graphql/graphql.ts').TcaSummaryV1} TcaSummaryV1
 * @typedef {import('../src/graphql/graphql.ts').TimeInForce} TimeInForce
 * @typedef {import('../src/graphql/graphql.ts').TradeV1} TradeV1
 * @typedef {import('../src/graphql/graphql.ts').TwapOrder} TwapOrder
 * @typedef {import('../src/graphql/graphql.ts').TwapStatus} TwapStatus
 * @typedef {import('../src/graphql/graphql.ts').UnknownMarketKind} UnknownMarketKind
 * @typedef {import('../src/graphql/graphql.ts').UpdateMarket} UpdateMarket
 * @typedef {import('../src/graphql/graphql.ts').Venue} Venue
 */

export function version() {
  return client.execute(
    graphql(`query Version {
  version 
}`,
    undefined)
  );
}
/**
 * Return the current user's authentication information.
 * **/
export function me() {
  return client.execute(
    graphql(`query Me {
  me { __typename }
}`,
    undefined)
  );
}
/**
 * List the API keys associated with the current user.
 * **/
export function listApiKeys() {
  return client.execute(
    graphql(`query ListApiKeys {
  listApiKeys { __typename }
}`,
    undefined)
  );
}

export function cptys() {
  return client.execute(
    graphql(`query Cptys {
  cptys { __typename }
}`,
    undefined)
  );
}
/**
 * List all known/mapped accounts relevant to the logged-in user.

Accounts are generally defined by exchange connectors or their respective exchange configs.
Refer to the User Guide for more information on how Architect names and manages accounts.
 * **/
export function accounts() {
  return client.execute(
    graphql(`query Accounts {
  accounts { __typename }
}`,
    undefined)
  );
}
/**
 * List all known routes in symbology.  Routes are uniquely identified by their names or IDs;
route IDs are fully determined by their string names as UUIDv5.
 * **/
export function routes() {
  return client.execute(
    graphql(`query Routes {
  routes { __typename }
}`,
    undefined)
  );
}
/**
 * Find a route by its ID.
 * @param {RouteId} id
 * **/
export function route(id) {
  return client.execute(
    graphql(`query Route($id: RouteId!) {
  route(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * List all known venues in symbology.  Venues are uniquely identified by their names or IDs;
venue IDs are fully determined by their string names as UUIDv5.
 * **/
export function venues() {
  return client.execute(
    graphql(`query Venues {
  venues { __typename }
}`,
    undefined)
  );
}
/**
 * Find a venue by its ID.
 * @param {VenueId} id
 * **/
export function venue(id) {
  return client.execute(
    graphql(`query Venue($id: VenueId!) {
  venue(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * Find products and their details by their IDs.  Products are uniquely identified by their
names or IDs; product IDs are fully determined by their string names as UUIDv5.
 * @param {ProductId[]} id
 * **/
export function products(id) {
  return client.execute(
    graphql(`query Products($id: ProductId[]!) {
  products(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * Find a product and its details by its ID.
 * @param {ProductId} id
 * **/
export function product(id) {
  return client.execute(
    graphql(`query Product($id: ProductId!) {
  product(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * Find markets and their details by their IDs.  Markets are uniquely identified by their
names or IDs; market IDs are fully determined by their string names as UUIDv5.
 * @param {MarketId[]} id
 * **/
export function markets(id) {
  return client.execute(
    graphql(`query Markets($id: MarketId[]!) {
  markets(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * Find a market and its details by its ID.
 * @param {MarketId} id
 * **/
export function market(id) {
  return client.execute(
    graphql(`query Market($id: MarketId!) {
  market(id: $id) { __typename }
}`,
    {id})
  );
}
/**
 * Find markets and their details by some filtering criteria.
 * @param {MarketFilter} filter
 * **/
export function filterMarkets(filter) {
  return client.execute(
    graphql(`query FilterMarkets($filter: MarketFilter!) {
  filterMarkets(filter: $filter) { __typename }
}`,
    {filter})
  );
}
/**
 * @param {MarketId} market
 * @param {Int} numLevels
 * @param {Decimal} [precision]
 * @param {Int} [retainSubscriptionForNSeconds]
 * @param {Boolean} [delayed]
 * **/
export function bookSnapshot(market, numLevels, precision, retainSubscriptionForNSeconds, delayed) {
  return client.execute(
    graphql(`query BookSnapshot($market: MarketId!, $numLevels: Int!, $precision: Decimal, $retainSubscriptionForNSeconds: Int, $delayed: Boolean) {
  bookSnapshot(market: $market, numLevels: $numLevels, precision: $precision, retainSubscriptionForNSeconds: $retainSubscriptionForNSeconds, delayed: $delayed) { __typename }
}`,
    {market, numLevels, precision, retainSubscriptionForNSeconds, delayed})
  );
}
/**
 * Get a snapshot of the marketdata for a given market, at a given time.  If no
latest_at_or_before is provided, the most recent snapshot is returned.
 * @param {MarketId} market
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function marketSnapshot(market, latestAtOrBefore) {
  return client.execute(
    graphql(`query MarketSnapshot($market: MarketId!, $latestAtOrBefore: DateTime) {
  marketSnapshot(market: $market, latestAtOrBefore: $latestAtOrBefore) { __typename }
}`,
    {market, latestAtOrBefore})
  );
}
/**
 * Get snapshots of all markets for the given time.  If no latest_at_or_before is provided,
the most recent snapshots are returned.
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function marketsSnapshots(latestAtOrBefore) {
  return client.execute(
    graphql(`query MarketsSnapshots($latestAtOrBefore: DateTime) {
  marketsSnapshots(latestAtOrBefore: $latestAtOrBefore) { __typename }
}`,
    {latestAtOrBefore})
  );
}
/**
 * Get a snapshot of the options data for a given underlying, at a given time.
 * @param {ProductId} underlying
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function optionsMarketSnapshots(underlying, latestAtOrBefore) {
  return client.execute(
    graphql(`query OptionsMarketSnapshots($underlying: ProductId!, $latestAtOrBefore: DateTime) {
  optionsMarketSnapshots(underlying: $underlying, latestAtOrBefore: $latestAtOrBefore) { __typename }
}`,
    {underlying, latestAtOrBefore})
  );
}
/**
 * Get the current known balances and positions for a given counterparty.
 * @param {VenueId} venue
 * @param {RouteId} route
 * **/
export function accountSummariesForCpty(venue, route) {
  return client.execute(
    graphql(`query AccountSummariesForCpty($venue: VenueId!, $route: RouteId!) {
  accountSummariesForCpty(venue: $venue, route: $route) { __typename }
}`,
    {venue, route})
  );
}
/**
 * Get all current known balances and positions for all counterparties.
 * **/
export function accountSummaries() {
  return client.execute(
    graphql(`query AccountSummaries {
  accountSummaries { __typename }
}`,
    undefined)
  );
}
/**
 * Get all fills for a given venue, route, base, and quote.
 * @param {VenueId} [venue]
 * @param {RouteId} [route]
 * @param {ProductId} [base]
 * @param {ProductId} [quote]
 * **/
export function fills(venue, route, base, quote) {
  return client.execute(
    graphql(`query Fills($venue: VenueId, $route: RouteId, $base: ProductId, $quote: ProductId) {
  fills(venue: $venue, route: $route, base: $base, quote: $quote) { __typename }
}`,
    {venue, route, base, quote})
  );
}
/**
 * Find order details by order ID from the OMS.
 * @param {OrderId} orderId
 * **/
export function order(orderId) {
  return client.execute(
    graphql(`query Order($orderId: OrderId!) {
  order(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * List all open orders known to the OMS.
 * **/
export function openOrders() {
  return client.execute(
    graphql(`query OpenOrders {
  openOrders { __typename }
}`,
    undefined)
  );
}
/**
 * List all recently outed orders known to the OMS.
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * **/
export function outedOrders(fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query OutedOrders($fromInclusive: DateTime, $toExclusive: DateTime) {
  outedOrders(fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename }
}`,
    {fromInclusive, toExclusive})
  );
}
/**
 * Query historical OHLCV candles for a given market, candle width, and time range.
 * @param {MarketId} id
 * @param {DateTime} start
 * @param {DateTime} end
 * @param {CandleWidth} width
 * **/
export function historicalCandles(id, start, end, width) {
  return client.execute(
    graphql(`query HistoricalCandles($id: MarketId!, $start: DateTime!, $end: DateTime!, $width: CandleWidth!) {
  historicalCandles(id: $id, start: $start, end: $end, width: $width) { __typename }
}`,
    {id, start, end, width})
  );
}
/**
 * Query TCA pnl / marks stats, id is an optional field but the dates are required
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
export function tcaMarks(id, fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query TcaMarks($id: MarketId, $fromInclusive: DateTime!, $toExclusive: DateTime!) {
  tcaMarks(id: $id, fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename }
}`,
    {id, fromInclusive, toExclusive})
  );
}
/**
 * Query TCA summary stats, id is an optional field but the dates are required
 * @param {String} [currency]
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
export function tcaSummary(currency, id, fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query TcaSummary($currency: String, $id: MarketId, $fromInclusive: DateTime!, $toExclusive: DateTime!) {
  tcaSummary(currency: $currency, id: $id, fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename }
}`,
    {currency, id, fromInclusive, toExclusive})
  );
}
/**
 * Query TCA balance pnl stats, the account_id is a required field.
The following filtering is allowed ..
If no venue is provided then all venues will be included
If use_purchasing_power is false or not provided then we will use
  the balance column in the table. If it's true then we will use
  the purchasing power column. This is needed for the rfb environment
 * @param {AccountId} accountId
 * @param {VenueId} [venueId]
 * @param {Boolean} [usePurchasingPower]
 * **/
export function tcaBalancePnl(accountId, venueId, usePurchasingPower) {
  return client.execute(
    graphql(`query TcaBalancePnl($accountId: AccountId!, $venueId: VenueId, $usePurchasingPower: Boolean) {
  tcaBalancePnl(accountId: $accountId, venueId: $venueId, usePurchasingPower: $usePurchasingPower) { __typename }
}`,
    {accountId, venueId, usePurchasingPower})
  );
}
/**
 * Query TCA balance pnl timeseries, the account_id and venue_id are
required fields. If both date ranges are not valid then we will return
the timeseries for the last rolling 24 hours. If they are both provided
then the timeseries will return hourly data points for the range provided
If use_purchasing_power is false or not provided then we will use
  the balance column in the table. If it's true then we will use
  the purchasing power column. This is needed for the rfb environment
 * @param {AccountId} accountId
 * @param {VenueId} venueId
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * @param {Boolean} [usePurchasingPower]
 * **/
export function tcaBalancePnlTimeseries(accountId, venueId, fromInclusive, toExclusive, usePurchasingPower) {
  return client.execute(
    graphql(`query TcaBalancePnlTimeseries($accountId: AccountId!, $venueId: VenueId!, $fromInclusive: DateTime, $toExclusive: DateTime, $usePurchasingPower: Boolean) {
  tcaBalancePnlTimeseries(accountId: $accountId, venueId: $venueId, fromInclusive: $fromInclusive, toExclusive: $toExclusive, usePurchasingPower: $usePurchasingPower) { __typename }
}`,
    {accountId, venueId, fromInclusive, toExclusive, usePurchasingPower})
  );
}
/**
 * Get a snapshot of token info, sourced from CoinGecko and CoinMarketCap.
 * **/
export function coinInfos() {
  return client.execute(
    graphql(`query CoinInfos {
  coinInfos { __typename }
}`,
    undefined)
  );
}
/**
 * Get token info for a given product.
 * @param {ProductId} product
 * **/
export function coinInfo(product) {
  return client.execute(
    graphql(`query CoinInfo($product: ProductId!) {
  coinInfo(product: $product) { __typename }
}`,
    {product})
  );
}
/**
 * Get CME product group info.
 * **/
export function cmeProductGroupInfos() {
  return client.execute(
    graphql(`query CmeProductGroupInfos {
  cmeProductGroupInfos { __typename }
}`,
    undefined)
  );
}
/**
 * Find a generic algo order and its details by parent order ID.
 * @param {OrderId} orderId
 * **/
export function algoOrder(orderId) {
  return client.execute(
    graphql(`query AlgoOrder($orderId: OrderId!) {
  algoOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return generic algo order status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function algoStatus(orderId) {
  return client.execute(
    graphql(`query AlgoStatus($orderId: OrderId) {
  algoStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return generic algo logs by parent order ID.
 * @param {OrderId} orderId
 * **/
export function algoLog(orderId) {
  return client.execute(
    graphql(`query AlgoLog($orderId: OrderId!) {
  algoLog(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return TWAP algo order details by parent order ID.
 * @param {OrderId} orderId
 * **/
export function twapOrder(orderId) {
  return client.execute(
    graphql(`query TwapOrder($orderId: OrderId!) {
  twapOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return TWAP algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function twapStatus(orderId) {
  return client.execute(
    graphql(`query TwapStatus($orderId: OrderId) {
  twapStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return POV order details by parent order ID.
 * @param {OrderId} orderId
 * **/
export function povOrder(orderId) {
  return client.execute(
    graphql(`query PovOrder($orderId: OrderId!) {
  povOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return POV algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function povStatus(orderId) {
  return client.execute(
    graphql(`query PovStatus($orderId: OrderId) {
  povStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return SOR order details by parent order ID.
 * @param {OrderId} orderId
 * **/
export function smartOrderRouterOrder(orderId) {
  return client.execute(
    graphql(`query SmartOrderRouterOrder($orderId: OrderId!) {
  smartOrderRouterOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return SOR algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function smartOrderRouterStatus(orderId) {
  return client.execute(
    graphql(`query SmartOrderRouterStatus($orderId: OrderId) {
  smartOrderRouterStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return MM algo order details by parent order ID.
 * @param {OrderId} orderId
 * **/
export function mmAlgoOrder(orderId) {
  return client.execute(
    graphql(`query MmAlgoOrder($orderId: OrderId!) {
  mmAlgoOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return spread algo status by parent order ID.
 * @param {OrderId} orderId
 * **/
export function spreadAlgoOrder(orderId) {
  return client.execute(
    graphql(`query SpreadAlgoOrder($orderId: OrderId!) {
  spreadAlgoOrder(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return MM algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function mmAlgoStatus(orderId) {
  return client.execute(
    graphql(`query MmAlgoStatus($orderId: OrderId) {
  mmAlgoStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}
/**
 * Find and return spread algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
export function spreadAlgoStatus(orderId) {
  return client.execute(
    graphql(`query SpreadAlgoStatus($orderId: OrderId) {
  spreadAlgoStatus(orderId: $orderId) { __typename }
}`,
    {orderId})
  );
}