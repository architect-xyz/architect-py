/**
 * Temp file for iteratively building the JS SDK codegen
 */
import { client, graphql } from './client.mjs';




function version() {
  return client.execute(graphql('', {}));
}
/**
 * Return the current user's authentication information.
 * **/
function me() {
  return client.execute(graphql('', {}));
}
/**
 * List the API keys associated with the current user.
 * **/
function listApiKeys() {
  return client.execute(graphql('', {}));
}

function cptys() {
  return client.execute(graphql('', {}));
}
/**
 * List all known/mapped accounts relevant to the logged-in user.

Accounts are generally defined by exchange connectors or their respective exchange configs.
Refer to the User Guide for more information on how Architect names and manages accounts.
 * **/
function accounts() {
  return client.execute(graphql('', {}));
}
/**
 * List all known routes in symbology.  Routes are uniquely identified by their names or IDs;
route IDs are fully determined by their string names as UUIDv5.
 * **/
function routes() {
  return client.execute(graphql('', {}));
}
/**
 * Find a route by its ID.
 * @param {RouteId} id
 * **/
function route(id) {
  return client.execute(graphql('', {id}));
}
/**
 * List all known venues in symbology.  Venues are uniquely identified by their names or IDs;
venue IDs are fully determined by their string names as UUIDv5.
 * **/
function venues() {
  return client.execute(graphql('', {}));
}
/**
 * Find a venue by its ID.
 * @param {VenueId} id
 * **/
function venue(id) {
  return client.execute(graphql('', {id}));
}
/**
 * Find products and their details by their IDs.  Products are uniquely identified by their
names or IDs; product IDs are fully determined by their string names as UUIDv5.
 * @param {ProductId[]} id
 * **/
function products(id) {
  return client.execute(graphql('', {id}));
}
/**
 * Find a product and its details by its ID.
 * @param {ProductId} id
 * **/
function product(id) {
  return client.execute(graphql('', {id}));
}
/**
 * Find markets and their details by their IDs.  Markets are uniquely identified by their
names or IDs; market IDs are fully determined by their string names as UUIDv5.
 * @param {MarketId[]} id
 * **/
function markets(id) {
  return client.execute(graphql('', {id}));
}
/**
 * Find a market and its details by its ID.
 * @param {MarketId} id
 * **/
function market(id) {
  return client.execute(graphql('', {id}));
}
/**
 * Find markets and their details by some filtering criteria.
 * @param {MarketFilter} filter
 * **/
function filterMarkets(filter) {
  return client.execute(graphql('', {filter}));
}
/**
 * @param {MarketId} market
 * @param {Int} numLevels
 * @param {Decimal} [precision]
 * @param {Int} [retainSubscriptionForNSeconds]
 * @param {Boolean} [delayed]
 * **/
function bookSnapshot(market, numLevels, precision, retainSubscriptionForNSeconds, delayed) {
  return client.execute(graphql('', {market, numLevels, precision, retainSubscriptionForNSeconds, delayed}));
}
/**
 * Get a snapshot of the marketdata for a given market, at a given time.  If no
latest_at_or_before is provided, the most recent snapshot is returned.
 * @param {MarketId} market
 * @param {DateTime} [latestAtOrBefore]
 * **/
function marketSnapshot(market, latestAtOrBefore) {
  return client.execute(graphql('', {market, latestAtOrBefore}));
}
/**
 * Get snapshots of all markets for the given time.  If no latest_at_or_before is provided,
the most recent snapshots are returned.
 * @param {DateTime} [latestAtOrBefore]
 * **/
function marketsSnapshots(latestAtOrBefore) {
  return client.execute(graphql('', {latestAtOrBefore}));
}
/**
 * Get a snapshot of the options data for a given underlying, at a given time.
 * @param {ProductId} underlying
 * @param {DateTime} [latestAtOrBefore]
 * **/
function optionsMarketSnapshots(underlying, latestAtOrBefore) {
  return client.execute(graphql('', {underlying, latestAtOrBefore}));
}
/**
 * Get the current known balances and positions for a given counterparty.
 * @param {VenueId} venue
 * @param {RouteId} route
 * **/
function accountSummariesForCpty(venue, route) {
  return client.execute(graphql('', {venue, route}));
}
/**
 * Get all current known balances and positions for all counterparties.
 * **/
function accountSummaries() {
  return client.execute(graphql('', {}));
}
/**
 * Get all fills for a given venue, route, base, and quote.
 * @param {VenueId} [venue]
 * @param {RouteId} [route]
 * @param {ProductId} [base]
 * @param {ProductId} [quote]
 * **/
function fills(venue, route, base, quote) {
  return client.execute(graphql('', {venue, route, base, quote}));
}
/**
 * Find order details by order ID from the OMS.
 * @param {OrderId} orderId
 * **/
function order(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * List all open orders known to the OMS.
 * **/
function openOrders() {
  return client.execute(graphql('', {}));
}
/**
 * List all recently outed orders known to the OMS.
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * **/
function outedOrders(fromInclusive, toExclusive) {
  return client.execute(graphql('', {fromInclusive, toExclusive}));
}
/**
 * Query historical OHLCV candles for a given market, candle width, and time range.
 * @param {MarketId} id
 * @param {DateTime} start
 * @param {DateTime} end
 * @param {CandleWidth} width
 * **/
function historicalCandles(id, start, end, width) {
  return client.execute(graphql('', {id, start, end, width}));
}
/**
 * Query TCA pnl / marks stats, id is an optional field but the dates are required
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
function tcaMarks(id, fromInclusive, toExclusive) {
  return client.execute(graphql('', {id, fromInclusive, toExclusive}));
}
/**
 * Query TCA summary stats, id is an optional field but the dates are required
 * @param {String} [currency]
 * @param {MarketId} [id]
 * @param {DateTime} fromInclusive
 * @param {DateTime} toExclusive
 * **/
function tcaSummary(currency, id, fromInclusive, toExclusive) {
  return client.execute(graphql('', {currency, id, fromInclusive, toExclusive}));
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
function tcaBalancePnl(accountId, venueId, usePurchasingPower) {
  return client.execute(graphql('', {accountId, venueId, usePurchasingPower}));
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
function tcaBalancePnlTimeseries(accountId, venueId, fromInclusive, toExclusive, usePurchasingPower) {
  return client.execute(graphql('', {accountId, venueId, fromInclusive, toExclusive, usePurchasingPower}));
}
/**
 * Get a snapshot of token info, sourced from CoinGecko and CoinMarketCap.
 * **/
function coinInfos() {
  return client.execute(graphql('', {}));
}
/**
 * Get token info for a given product.
 * @param {ProductId} product
 * **/
function coinInfo(product) {
  return client.execute(graphql('', {product}));
}
/**
 * Get CME product group info.
 * **/
function cmeProductGroupInfos() {
  return client.execute(graphql('', {}));
}
/**
 * Find a generic algo order and its details by parent order ID.
 * @param {OrderId} orderId
 * **/
function algoOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return generic algo order status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function algoStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return generic algo logs by parent order ID.
 * @param {OrderId} orderId
 * **/
function algoLog(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return TWAP algo order details by parent order ID.
 * @param {OrderId} orderId
 * **/
function twapOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return TWAP algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function twapStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return POV order details by parent order ID.
 * @param {OrderId} orderId
 * **/
function povOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return POV algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function povStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return SOR order details by parent order ID.
 * @param {OrderId} orderId
 * **/
function smartOrderRouterOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return SOR algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function smartOrderRouterStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return MM algo order details by parent order ID.
 * @param {OrderId} orderId
 * **/
function mmAlgoOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return spread algo status by parent order ID.
 * @param {OrderId} orderId
 * **/
function spreadAlgoOrder(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return MM algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function mmAlgoStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}
/**
 * Find and return spread algo status by parent order ID.
 * @param {OrderId} [orderId]
 * **/
function spreadAlgoStatus(orderId) {
  return client.execute(graphql('', {orderId}));
}