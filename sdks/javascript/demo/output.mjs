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
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Me} fields
 * **/
export function me(fields, ) {
  return client.execute(
    graphql(`query Me {
  me { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * List the API keys associated with the current user.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').ApiKey} fields
 * **/
export function listApiKeys(fields, ) {
  return client.execute(
    graphql(`query ListApiKeys {
  listApiKeys { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').CptyInfo} fields
 * **/
export function cptys(fields, ) {
  return client.execute(
    graphql(`query Cptys {
  cptys { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * List all known/mapped accounts relevant to the logged-in user.

Accounts are generally defined by exchange connectors or their respective exchange configs.
Refer to the User Guide for more information on how Architect names and manages accounts.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Account} fields
 * **/
export function accounts(fields, ) {
  return client.execute(
    graphql(`query Accounts {
  accounts { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * List all known routes in symbology.  Routes are uniquely identified by their names or IDs;
route IDs are fully determined by their string names as UUIDv5.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Route} fields
 * **/
export function routes(fields, ) {
  return client.execute(
    graphql(`query Routes {
  routes { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * Find a route by its ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Route} fields
 * @param {RouteId} id
 * **/
export function route(fields, id) {
  return client.execute(
    graphql(`query Route($id: RouteId!) {
  route(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * List all known venues in symbology.  Venues are uniquely identified by their names or IDs;
venue IDs are fully determined by their string names as UUIDv5.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Venue} fields
 * **/
export function venues(fields, ) {
  return client.execute(
    graphql(`query Venues {
  venues { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * Find a venue by its ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Venue} fields
 * @param {VenueId} id
 * **/
export function venue(fields, id) {
  return client.execute(
    graphql(`query Venue($id: VenueId!) {
  venue(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * Find products and their details by their IDs.  Products are uniquely identified by their
names or IDs; product IDs are fully determined by their string names as UUIDv5.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Product} fields
 * @param {ProductId[]} id
 * **/
export function products(fields, id) {
  return client.execute(
    graphql(`query Products($id: ProductId[]!) {
  products(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * Find a product and its details by its ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Product} fields
 * @param {ProductId} id
 * **/
export function product(fields, id) {
  return client.execute(
    graphql(`query Product($id: ProductId!) {
  product(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * Find markets and their details by their IDs.  Markets are uniquely identified by their
names or IDs; market IDs are fully determined by their string names as UUIDv5.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Market} fields
 * @param {MarketId[]} id
 * **/
export function markets(fields, id) {
  return client.execute(
    graphql(`query Markets($id: MarketId[]!) {
  markets(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * Find a market and its details by its ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Market} fields
 * @param {MarketId} id
 * **/
export function market(fields, id) {
  return client.execute(
    graphql(`query Market($id: MarketId!) {
  market(id: $id) { __typename ${fields.join(' ')} }
}`,
    {id})
  );
}
/**
 * Find markets and their details by some filtering criteria.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Market} fields
 * @param {MarketFilter} filter
 * **/
export function filterMarkets(fields, filter) {
  return client.execute(
    graphql(`query FilterMarkets($filter: MarketFilter!) {
  filterMarkets(filter: $filter) { __typename ${fields.join(' ')} }
}`,
    {filter})
  );
}
/**
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Book} fields
 * @param {MarketId} market
 * @param {Int} numLevels
 * @param {Decimal} [precision]
 * @param {Int} [retainSubscriptionForNSeconds]
 * @param {Boolean} [delayed]
 * **/
export function bookSnapshot(fields, market, numLevels, precision, retainSubscriptionForNSeconds, delayed) {
  return client.execute(
    graphql(`query BookSnapshot($market: MarketId!, $numLevels: Int!, $precision: Decimal, $retainSubscriptionForNSeconds: Int, $delayed: Boolean) {
  bookSnapshot(market: $market, numLevels: $numLevels, precision: $precision, retainSubscriptionForNSeconds: $retainSubscriptionForNSeconds, delayed: $delayed) { __typename ${fields.join(' ')} }
}`,
    {market, numLevels, precision, retainSubscriptionForNSeconds, delayed})
  );
}
/**
 * Get a snapshot of the marketdata for a given market, at a given time.  If no
latest_at_or_before is provided, the most recent snapshot is returned.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MarketSnapshot} fields
 * @param {MarketId} market
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function marketSnapshot(fields, market, latestAtOrBefore) {
  return client.execute(
    graphql(`query MarketSnapshot($market: MarketId!, $latestAtOrBefore: DateTime) {
  marketSnapshot(market: $market, latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
}`,
    {market, latestAtOrBefore})
  );
}
/**
 * Get snapshots of all markets for the given time.  If no latest_at_or_before is provided,
the most recent snapshots are returned.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MarketSnapshot} fields
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function marketsSnapshots(fields, latestAtOrBefore) {
  return client.execute(
    graphql(`query MarketsSnapshots($latestAtOrBefore: DateTime) {
  marketsSnapshots(latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
}`,
    {latestAtOrBefore})
  );
}
/**
 * Get a snapshot of the options data for a given underlying, at a given time.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').OptionsMarketSnapshot} fields
 * @param {ProductId} underlying
 * @param {DateTime} [latestAtOrBefore]
 * **/
export function optionsMarketSnapshots(fields, underlying, latestAtOrBefore) {
  return client.execute(
    graphql(`query OptionsMarketSnapshots($underlying: ProductId!, $latestAtOrBefore: DateTime) {
  optionsMarketSnapshots(underlying: $underlying, latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
}`,
    {underlying, latestAtOrBefore})
  );
}
/**
 * Get the current known balances and positions for a given counterparty.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').AccountSummaries} fields
 * @param {VenueId} venue
 * @param {RouteId} route
 * **/
export function accountSummariesForCpty(fields, venue, route) {
  return client.execute(
    graphql(`query AccountSummariesForCpty($venue: VenueId!, $route: RouteId!) {
  accountSummariesForCpty(venue: $venue, route: $route) { __typename ${fields.join(' ')} }
}`,
    {venue, route})
  );
}
/**
 * Get all current known balances and positions for all counterparties.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').AccountSummaries} fields
 * **/
export function accountSummaries(fields, ) {
  return client.execute(
    graphql(`query AccountSummaries {
  accountSummaries { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * Get all fills for a given venue, route, base, and quote.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').Fills} fields
 * @param {VenueId} [venue]
 * @param {RouteId} [route]
 * @param {ProductId} [base]
 * @param {ProductId} [quote]
 * **/
export function fills(fields, venue, route, base, quote) {
  return client.execute(
    graphql(`query Fills($venue: VenueId, $route: RouteId, $base: ProductId, $quote: ProductId) {
  fills(venue: $venue, route: $route, base: $base, quote: $quote) { __typename ${fields.join(' ')} }
}`,
    {venue, route, base, quote})
  );
}
/**
 * Find order details by order ID from the OMS.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').OrderLog} fields
 * @param {OrderId} orderId
 * **/
export function order(fields, orderId) {
  return client.execute(
    graphql(`query Order($orderId: OrderId!) {
  order(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * List all open orders known to the OMS.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').OrderLog} fields
 * **/
export function openOrders(fields, ) {
  return client.execute(
    graphql(`query OpenOrders {
  openOrders { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * List all recently outed orders known to the OMS.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').OrderLog} fields
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * **/
export function outedOrders(fields, fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query OutedOrders($fromInclusive: DateTime, $toExclusive: DateTime) {
  outedOrders(fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename ${fields.join(' ')} }
}`,
    {fromInclusive, toExclusive})
  );
}
/**
 * Query historical OHLCV candles for a given market, candle width, and time range.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').CandleV1} fields
 * @param {MarketId} id
 * @param {DateTime} start
 * @param {DateTime} end
 * @param {CandleWidth} width
 * **/
export function historicalCandles(fields, id, start, end, width) {
  return client.execute(
    graphql(`query HistoricalCandles($id: MarketId!, $start: DateTime!, $end: DateTime!, $width: CandleWidth!) {
  historicalCandles(id: $id, start: $start, end: $end, width: $width) { __typename ${fields.join(' ')} }
}`,
    {id, start, end, width})
  );
}
/**
 * Query TCA pnl / marks stats, id is an optional field but the dates are required
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TcaMarksV1} fields
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
export function tcaMarks(fields, id, fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query TcaMarks($id: MarketId, $fromInclusive: DateTime!, $toExclusive: DateTime!) {
  tcaMarks(id: $id, fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename ${fields.join(' ')} }
}`,
    {id, fromInclusive, toExclusive})
  );
}
/**
 * Query TCA summary stats, id is an optional field but the dates are required
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TcaSummaryV1} fields
 * @param {String} [currency]
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
export function tcaSummary(fields, currency, id, fromInclusive, toExclusive) {
  return client.execute(
    graphql(`query TcaSummary($currency: String, $id: MarketId, $fromInclusive: DateTime!, $toExclusive: DateTime!) {
  tcaSummary(currency: $currency, id: $id, fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename ${fields.join(' ')} }
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
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TcaBalancePnlV1} fields
 * @param {AccountId} accountId
 * @param {VenueId} [venueId]
 * @param {Boolean} [usePurchasingPower]
 * **/
export function tcaBalancePnl(fields, accountId, venueId, usePurchasingPower) {
  return client.execute(
    graphql(`query TcaBalancePnl($accountId: AccountId!, $venueId: VenueId, $usePurchasingPower: Boolean) {
  tcaBalancePnl(accountId: $accountId, venueId: $venueId, usePurchasingPower: $usePurchasingPower) { __typename ${fields.join(' ')} }
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
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TcaPnlV1} fields
 * @param {AccountId} accountId
 * @param {VenueId} venueId
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * @param {Boolean} [usePurchasingPower]
 * **/
export function tcaBalancePnlTimeseries(fields, accountId, venueId, fromInclusive, toExclusive, usePurchasingPower) {
  return client.execute(
    graphql(`query TcaBalancePnlTimeseries($accountId: AccountId!, $venueId: VenueId!, $fromInclusive: DateTime, $toExclusive: DateTime, $usePurchasingPower: Boolean) {
  tcaBalancePnlTimeseries(accountId: $accountId, venueId: $venueId, fromInclusive: $fromInclusive, toExclusive: $toExclusive, usePurchasingPower: $usePurchasingPower) { __typename ${fields.join(' ')} }
}`,
    {accountId, venueId, fromInclusive, toExclusive, usePurchasingPower})
  );
}
/**
 * Get a snapshot of token info, sourced from CoinGecko and CoinMarketCap.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').CoinInfo} fields
 * **/
export function coinInfos(fields, ) {
  return client.execute(
    graphql(`query CoinInfos {
  coinInfos { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * Get token info for a given product.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').CoinInfo} fields
 * @param {ProductId} product
 * **/
export function coinInfo(fields, product) {
  return client.execute(
    graphql(`query CoinInfo($product: ProductId!) {
  coinInfo(product: $product) { __typename ${fields.join(' ')} }
}`,
    {product})
  );
}
/**
 * Get CME product group info.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').CmeProductGroupInfo} fields
 * **/
export function cmeProductGroupInfos(fields, ) {
  return client.execute(
    graphql(`query CmeProductGroupInfos {
  cmeProductGroupInfos { __typename ${fields.join(' ')} }
}`,
    undefined)
  );
}
/**
 * Find a generic algo order and its details by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').AlgoOrder} fields
 * @param {OrderId} orderId
 * **/
export function algoOrder(fields, orderId) {
  return client.execute(
    graphql(`query AlgoOrder($orderId: OrderId!) {
  algoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return generic algo order status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').AlgoStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function algoStatus(fields, orderId) {
  return client.execute(
    graphql(`query AlgoStatus($orderId: OrderId) {
  algoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return generic algo logs by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').AlgoLog} fields
 * @param {OrderId} orderId
 * **/
export function algoLog(fields, orderId) {
  return client.execute(
    graphql(`query AlgoLog($orderId: OrderId!) {
  algoLog(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return TWAP algo order details by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TwapOrder} fields
 * @param {OrderId} orderId
 * **/
export function twapOrder(fields, orderId) {
  return client.execute(
    graphql(`query TwapOrder($orderId: OrderId!) {
  twapOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return TWAP algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').TwapStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function twapStatus(fields, orderId) {
  return client.execute(
    graphql(`query TwapStatus($orderId: OrderId) {
  twapStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return POV order details by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').PovAlgoOrder} fields
 * @param {OrderId} orderId
 * **/
export function povOrder(fields, orderId) {
  return client.execute(
    graphql(`query PovOrder($orderId: OrderId!) {
  povOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return POV algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').PovAlgoStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function povStatus(fields, orderId) {
  return client.execute(
    graphql(`query PovStatus($orderId: OrderId) {
  povStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return SOR order details by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').SmartOrderRouterOrder} fields
 * @param {OrderId} orderId
 * **/
export function smartOrderRouterOrder(fields, orderId) {
  return client.execute(
    graphql(`query SmartOrderRouterOrder($orderId: OrderId!) {
  smartOrderRouterOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return SOR algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').SmartOrderRouterStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function smartOrderRouterStatus(fields, orderId) {
  return client.execute(
    graphql(`query SmartOrderRouterStatus($orderId: OrderId) {
  smartOrderRouterStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return MM algo order details by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MMAlgoOrder} fields
 * @param {OrderId} orderId
 * **/
export function mmAlgoOrder(fields, orderId) {
  return client.execute(
    graphql(`query MmAlgoOrder($orderId: OrderId!) {
  mmAlgoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return spread algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MMAlgoOrder} fields
 * @param {OrderId} orderId
 * **/
export function spreadAlgoOrder(fields, orderId) {
  return client.execute(
    graphql(`query SpreadAlgoOrder($orderId: OrderId!) {
  spreadAlgoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return MM algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MMAlgoStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function mmAlgoStatus(fields, orderId) {
  return client.execute(
    graphql(`query MmAlgoStatus($orderId: OrderId) {
  mmAlgoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}
/**
 * Find and return spread algo status by parent order ID.
 *  * @param {Array<keyof import('../src/graphql/graphql.ts').MMAlgoStatus} fields
 * @param {OrderId} [orderId]
 * **/
export function spreadAlgoStatus(fields, orderId) {
  return client.execute(
    graphql(`query SpreadAlgoStatus($orderId: OrderId) {
  spreadAlgoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
}`,
    {orderId})
  );
}