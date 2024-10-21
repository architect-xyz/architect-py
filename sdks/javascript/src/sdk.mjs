/**
 * Copyright (c) Architect Financial Technologies, Inc. and affiliates.
 *
 * This source code is licensed under the Apache 2.0 license found in the
 *
 * LICENSE file in the root directory of this source tree.
 */
import { print } from 'graphql';
import { graphql } from './client.mjs';

/**
 * @typedef { import('./graphql/graphql.ts').Scalars['AccountId']['output'] } AccountId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef { import('./graphql/graphql.ts').Scalars['Boolean']['output'] } Boolean - The `Boolean` scalar type represents `true` or `false`.
 * @typedef { import('./graphql/graphql.ts').Scalars['ComponentId']['output'] } ComponentId - Components within an Architect installation are uniquely identified by a 16-bit integer
 * @typedef { import('./graphql/graphql.ts').Scalars['Date']['output'] } Date - Date in the proleptic Gregorian calendar (without time zone).
 * @typedef { import('./graphql/graphql.ts').Scalars['DateTime']['output'] } DateTime - Combined date and time (with time zone) in [RFC 3339][0] format.
 * @typedef { import('./graphql/graphql.ts').Scalars['Decimal']['output'] } Decimal - 128 bit representation of a fixed-precision decimal number.
 * @typedef { import('./graphql/graphql.ts').Scalars['Dir']['output'] } Dir - An order side/direction or a trade execution side/direction.
 * @typedef { import('./graphql/graphql.ts').Scalars['FillId']['output'] } FillId - The ID of a fill
 * @typedef { import('./graphql/graphql.ts').Scalars['Float']['output'] } Float - The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
 * @typedef { import('./graphql/graphql.ts').Scalars['Int']['output'] } Int - The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.
 * @typedef { import('./graphql/graphql.ts').Scalars['MarketId']['output'] } MarketId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef { import('./graphql/graphql.ts').Scalars['OrderId']['output'] } OrderId - System-unique, persistent order identifiers
 * @typedef { import('./graphql/graphql.ts').Scalars['ProductId']['output'] } ProductId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef { import('./graphql/graphql.ts').Scalars['RouteId']['output'] } RouteId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef { import('./graphql/graphql.ts').Scalars['Str']['output'] } Str - A String type
 * @typedef { import('./graphql/graphql.ts').Scalars['String']['output'] } String - The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.
 * @typedef { import('./graphql/graphql.ts').Scalars['UserId']['output'] } UserId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 * @typedef { import('./graphql/graphql.ts').Scalars['VenueId']['output'] } VenueId - Wrapper type around a UUIDv5 for a given namespace.  These types are
 *
 * @typedef { import('./graphql/graphql.ts').AberrantFill } AberrantFill - Fills which we received but couldn't parse fully, return details
 * @typedef { import('./graphql/graphql.ts').Account } Account
 * @typedef { import('./graphql/graphql.ts').AccountSummaries } AccountSummaries
 * @typedef { import('./graphql/graphql.ts').AccountSummary } AccountSummary
 * @typedef { import('./graphql/graphql.ts').Ack } Ack
 * @typedef { import('./graphql/graphql.ts').AlgoControlCommand } AlgoControlCommand
 * @typedef { import('./graphql/graphql.ts').AlgoKind } AlgoKind
 * @typedef { import('./graphql/graphql.ts').AlgoLog } AlgoLog
 * @typedef { import('./graphql/graphql.ts').AlgoOrder } AlgoOrder
 * @typedef { import('./graphql/graphql.ts').AlgoPreview } AlgoPreview
 * @typedef { import('./graphql/graphql.ts').AlgoRunningStatus } AlgoRunningStatus
 * @typedef { import('./graphql/graphql.ts').AlgoStatus } AlgoStatus
 * @typedef { import('./graphql/graphql.ts').ApiKey } ApiKey
 * @typedef { import('./graphql/graphql.ts').Balance } Balance
 * @typedef { import('./graphql/graphql.ts').Book } Book
 * @typedef { import('./graphql/graphql.ts').BookLevel } BookLevel
 * @typedef { import('./graphql/graphql.ts').Cancel } Cancel
 * @typedef { import('./graphql/graphql.ts').CancelAll } CancelAll
 * @typedef { import('./graphql/graphql.ts').CandleV1 } CandleV1 - NB: buy_volume + sell_volume <> volume; volume may count trades
 * @typedef { import('./graphql/graphql.ts').CandleWidth } CandleWidth
 * @typedef { import('./graphql/graphql.ts').CmeProductGroupInfo } CmeProductGroupInfo
 * @typedef { import('./graphql/graphql.ts').CmeSecurityType } CmeSecurityType
 * @typedef { import('./graphql/graphql.ts').CoinInfo } CoinInfo
 * @typedef { import('./graphql/graphql.ts').CptyInfo } CptyInfo
 * @typedef { import('./graphql/graphql.ts').CreateMmAlgo } CreateMmAlgo
 * @typedef { import('./graphql/graphql.ts').CreateOrder } CreateOrder
 * @typedef { import('./graphql/graphql.ts').CreateOrderType } CreateOrderType
 * @typedef { import('./graphql/graphql.ts').CreatePovAlgo } CreatePovAlgo
 * @typedef { import('./graphql/graphql.ts').CreateSmartOrderRouterAlgo } CreateSmartOrderRouterAlgo
 * @typedef { import('./graphql/graphql.ts').CreateSpreadAlgo } CreateSpreadAlgo
 * @typedef { import('./graphql/graphql.ts').CreateSpreadAlgoHedgeMarket } CreateSpreadAlgoHedgeMarket
 * @typedef { import('./graphql/graphql.ts').CreateTimeInForce } CreateTimeInForce
 * @typedef { import('./graphql/graphql.ts').CreateTimeInForceInstruction } CreateTimeInForceInstruction
 * @typedef { import('./graphql/graphql.ts').CreateTwapAlgo } CreateTwapAlgo
 * @typedef { import('./graphql/graphql.ts').Environment } Environment
 * @typedef { import('./graphql/graphql.ts').EnvironmentKind } EnvironmentKind
 * @typedef { import('./graphql/graphql.ts').ExchangeMarketKind } ExchangeMarketKind
 * @typedef { import('./graphql/graphql.ts').ExchangeSpecificUpdate } ExchangeSpecificUpdate
 * @typedef { import('./graphql/graphql.ts').Fee } Fee
 * @typedef { import('./graphql/graphql.ts').Fill } Fill
 * @typedef { import('./graphql/graphql.ts').FillKind } FillKind
 * @typedef { import('./graphql/graphql.ts').Fills } Fills
 * @typedef { import('./graphql/graphql.ts').HedgeMarket } HedgeMarket
 * @typedef { import('./graphql/graphql.ts').License } License
 * @typedef { import('./graphql/graphql.ts').LicenseTier } LicenseTier
 * @typedef { import('./graphql/graphql.ts').LimitOrderType } LimitOrderType
 * @typedef { import('./graphql/graphql.ts').MmAlgoDecision } MmAlgoDecision
 * @typedef { import('./graphql/graphql.ts').MmAlgoDecisionCancel } MmAlgoDecisionCancel
 * @typedef { import('./graphql/graphql.ts').MmAlgoDecisionDoNothing } MmAlgoDecisionDoNothing
 * @typedef { import('./graphql/graphql.ts').MmAlgoDecisionSend } MmAlgoDecisionSend
 * @typedef { import('./graphql/graphql.ts').MmAlgoKind } MmAlgoKind
 * @typedef { import('./graphql/graphql.ts').MmAlgoOpenOrder } MmAlgoOpenOrder
 * @typedef { import('./graphql/graphql.ts').MmAlgoOrder } MmAlgoOrder
 * @typedef { import('./graphql/graphql.ts').MmAlgoSide } MmAlgoSide
 * @typedef { import('./graphql/graphql.ts').MmAlgoStatus } MmAlgoStatus
 * @typedef { import('./graphql/graphql.ts').Market } Market
 * @typedef { import('./graphql/graphql.ts').MarketFilter } MarketFilter
 * @typedef { import('./graphql/graphql.ts').MarketKind } MarketKind
 * @typedef { import('./graphql/graphql.ts').MarketSnapshot } MarketSnapshot
 * @typedef { import('./graphql/graphql.ts').Me } Me
 * @typedef { import('./graphql/graphql.ts').MinOrderQuantityUnit } MinOrderQuantityUnit
 * @typedef { import('./graphql/graphql.ts').MutationRoot } MutationRoot
 * @typedef { import('./graphql/graphql.ts').OmsOrderUpdate } OmsOrderUpdate
 * @typedef { import('./graphql/graphql.ts').OptionsMarketSnapshot } OptionsMarketSnapshot
 * @typedef { import('./graphql/graphql.ts').Order } Order
 * @typedef { import('./graphql/graphql.ts').OrderLog } OrderLog
 * @typedef { import('./graphql/graphql.ts').OrderSource } OrderSource
 * @typedef { import('./graphql/graphql.ts').OrderStateFlags } OrderStateFlags - The state of an order
 * @typedef { import('./graphql/graphql.ts').OrderType } OrderType
 * @typedef { import('./graphql/graphql.ts').Orderflow } Orderflow
 * @typedef { import('./graphql/graphql.ts').Out } Out
 * @typedef { import('./graphql/graphql.ts').PoolMarketKind } PoolMarketKind
 * @typedef { import('./graphql/graphql.ts').Position } Position
 * @typedef { import('./graphql/graphql.ts').PovAlgoOrder } PovAlgoOrder
 * @typedef { import('./graphql/graphql.ts').PovAlgoStatus } PovAlgoStatus
 * @typedef { import('./graphql/graphql.ts').Product } Product
 * @typedef { import('./graphql/graphql.ts').QueryRoot } QueryRoot
 * @typedef { import('./graphql/graphql.ts').Reason } Reason
 * @typedef { import('./graphql/graphql.ts').ReferencePrice } ReferencePrice
 * @typedef { import('./graphql/graphql.ts').Reject } Reject
 * @typedef { import('./graphql/graphql.ts').RfqResponse } RfqResponse
 * @typedef { import('./graphql/graphql.ts').RfqResponseSide } RfqResponseSide
 * @typedef { import('./graphql/graphql.ts').Route } Route
 * @typedef { import('./graphql/graphql.ts').SmartOrderRouterOrder } SmartOrderRouterOrder
 * @typedef { import('./graphql/graphql.ts').SmartOrderRouterStatus } SmartOrderRouterStatus
 * @typedef { import('./graphql/graphql.ts').StopLossLimitOrderType } StopLossLimitOrderType
 * @typedef { import('./graphql/graphql.ts').SubscriptionRoot } SubscriptionRoot
 * @typedef { import('./graphql/graphql.ts').TakeProfitLimitOrderType } TakeProfitLimitOrderType
 * @typedef { import('./graphql/graphql.ts').TcaBalancePnlV1 } TcaBalancePnlV1
 * @typedef { import('./graphql/graphql.ts').TcaData } TcaData
 * @typedef { import('./graphql/graphql.ts').TcaMarksV1 } TcaMarksV1
 * @typedef { import('./graphql/graphql.ts').TcaPnlV1 } TcaPnlV1
 * @typedef { import('./graphql/graphql.ts').TcaSummaryV1 } TcaSummaryV1
 * @typedef { import('./graphql/graphql.ts').TimeInForce } TimeInForce
 * @typedef { import('./graphql/graphql.ts').TradeV1 } TradeV1
 * @typedef { import('./graphql/graphql.ts').TwapOrder } TwapOrder
 * @typedef { import('./graphql/graphql.ts').TwapStatus } TwapStatus
 * @typedef { import('./graphql/graphql.ts').UnknownMarketKind } UnknownMarketKind
 * @typedef { import('./graphql/graphql.ts').UpdateMarket } UpdateMarket
 * @typedef { import('./graphql/graphql.ts').Venue } Venue
 */

/**
 * @typedef {Object} Config API client config
 * @property {string} host API Host
 * @property {string} apiKey API Key
 * @property {string} apiSecret API Secret
 */

export class Client {
  /**
   * Architect Client SDK class
   *
   * @param {Config} config API client config
   * @param {import('graphql-http')['createClient']} createGraphqlClient
   */
  constructor(config, createGraphqlClient) {
    // Resolve host to the graphql endpoint
    const host = config.host.includes('4567')
      ? config.host
      : config.host.replace(/\/$/, ':4567/');

    /**
     * GraphQL client that can execute queries against the GraphQL Server
     * @type {import('graphql-http').Client} client
     * @public
     */
    this.client = createGraphqlClient({
      url: `${host}graphql`,
      headers: {
        Authorization: `Basic ${config.apiKey} ${config.apiSecret}`,
      },
    });
  }

  /**
   * Typed GraphQL query parser
   *
   * @param {Parameters<typeof graphql>[0]} query GraphQL document string
   * @returns {ReturnType<typeof graphql>}
   */
  parse(query) {
    return graphql(query);
  }

  /**
   * Execute a GraphQL query with typed response
   *
   * @template Result [Result=any]
   * @template Variables [Variables=any]
   *
   * @param {import('gql.tada').TadaDocumentNode<Result, Variables>} query GraphQL document string
   * @param {Variables} [variables] query variables
   * @returns {Promise<Result>}
   */
  async execute(query, variables) {
    let cancel = () => {};
    return new Promise((resolve, reject) => {
      /**
       * @type {Result}
       */
      let result;
      cancel = this.client.subscribe(
        {
          query: print(query),
          // @ts-expect-error Variables type is not quite the same
          variables,
        },
        {
          next: (resp) => {
            // @ts-expect-error resp.data may not be provided in error cases
            result = resp.data;
          },
          error: (err) => reject(err),
          complete: () => resolve(result),
        },
      );
    });
  }

  /**
   * @returns {Promise<String>}
   **/
  async version() {
    return this.execute(
      graphql(`query Version {
        version
      }`),
    ).then((results) => results['version']);
  }

  /**
   * Return the current user's authentication information.
   * @template {keyof Me} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<Me, Fields | '__typename'>>}
   **/
  async me(fields) {
    return this.execute(
      graphql(`query Me {
        me { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['me']);
  }

  /**
   * List the API keys associated with the current user.
   * @template {keyof ApiKey} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<ApiKey, Fields | '__typename'>[]>}
   **/
  async listApiKeys(fields) {
    return this.execute(
      graphql(`query ListApiKeys {
        listApiKeys { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['listApiKeys']);
  }

  /**
   * @template {keyof CptyInfo} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<CptyInfo, Fields | '__typename'>[]>}
   **/
  async cptys(fields) {
    return this.execute(
      graphql(`query Cptys {
        cptys { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['cptys']);
  }

  /**
 * List all known/mapped accounts relevant to the logged-in user.

Accounts are generally defined by exchange connectors or their respective exchange configs.
Refer to the User Guide for more information on how Architect names and manages accounts.
 * @template {keyof Account} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @returns {Promise<Pick<Account, Fields | '__typename'>[]>}
 **/
  async accounts(fields) {
    return this.execute(
      graphql(`query Accounts {
        accounts { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['accounts']);
  }

  /**
 * List all known routes in symbology.  Routes are uniquely identified by their names or IDs;
route IDs are fully determined by their string names as UUIDv5.
 * @template {keyof Route} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @returns {Promise<Pick<Route, Fields | '__typename'>[]>}
 **/
  async routes(fields) {
    return this.execute(
      graphql(`query Routes {
        routes { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['routes']);
  }

  /**
   * Find a route by its ID.
   * @template {keyof Route} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {RouteId} id
   * @returns {Promise<Pick<Route, Fields | '__typename'> | null>}
   **/
  async route(fields, id) {
    return this.execute(
      graphql(`query Route($id: RouteId!) {
        route(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['route']);
  }

  /**
 * List all known venues in symbology.  Venues are uniquely identified by their names or IDs;
venue IDs are fully determined by their string names as UUIDv5.
 * @template {keyof Venue} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @returns {Promise<Pick<Venue, Fields | '__typename'>[]>}
 **/
  async venues(fields) {
    return this.execute(
      graphql(`query Venues {
        venues { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['venues']);
  }

  /**
   * Find a venue by its ID.
   * @template {keyof Venue} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {VenueId} id
   * @returns {Promise<Pick<Venue, Fields | '__typename'> | null>}
   **/
  async venue(fields, id) {
    return this.execute(
      graphql(`query Venue($id: VenueId!) {
        venue(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['venue']);
  }

  /**
 * Find products and their details by their IDs.  Products are uniquely identified by their
names or IDs; product IDs are fully determined by their string names as UUIDv5.
 * @template {keyof Product} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {ProductId[]} id
 * @returns {Promise<Pick<Product, Fields | '__typename'>[]>}
 **/
  async products(fields, id) {
    return this.execute(
      graphql(`query Products($id: [ProductId!]!) {
        products(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['products']);
  }

  /**
   * Find a product and its details by its ID.
   * @template {keyof Product} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {ProductId} id
   * @returns {Promise<Pick<Product, Fields | '__typename'> | null>}
   **/
  async product(fields, id) {
    return this.execute(
      graphql(`query Product($id: ProductId!) {
        product(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['product']);
  }

  /**
 * Find markets and their details by their IDs.  Markets are uniquely identified by their
names or IDs; market IDs are fully determined by their string names as UUIDv5.
 * @template {keyof Market} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {MarketId[]} id
 * @returns {Promise<Pick<Market, Fields | '__typename'>[]>}
 **/
  async markets(fields, id) {
    return this.execute(
      graphql(`query Markets($id: [MarketId!]!) {
        markets(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['markets']);
  }

  /**
   * Find a market and its details by its ID.
   * @template {keyof Market} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {MarketId} id
   * @returns {Promise<Pick<Market, Fields | '__typename'> | null>}
   **/
  async market(fields, id) {
    return this.execute(
      graphql(`query Market($id: MarketId!) {
        market(id: $id) { __typename ${fields.join(' ')} }
      }`),
      { id },
    ).then((results) => results['market']);
  }

  /**
   * Find markets and their details by some filtering criteria.
   * @template {keyof Market} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {MarketFilter} filter
   * @returns {Promise<Pick<Market, Fields | '__typename'>[]>}
   **/
  async filterMarkets(fields, filter) {
    return this.execute(
      graphql(`query FilterMarkets($filter: MarketFilter!) {
        filterMarkets(filter: $filter) { __typename ${fields.join(' ')} }
      }`),
      { filter },
    ).then((results) => results['filterMarkets']);
  }

  /**
   * @template {keyof Book} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {Int} numLevels
   * @param {MarketId} market
   * @param {Decimal} [precision]
   * @param {Int} [retainSubscriptionForNSeconds]
   * @param {Boolean} [delayed]
   * @returns {Promise<Pick<Book, Fields | '__typename'>>}
   **/
  async bookSnapshot(
    fields,
    numLevels,
    market,
    precision,
    retainSubscriptionForNSeconds,
    delayed,
  ) {
    return this.execute(
      graphql(`query BookSnapshot($numLevels: Int!, $market: MarketId!, $precision: Decimal, $retainSubscriptionForNSeconds: Int, $delayed: Boolean) {
        bookSnapshot(numLevels: $numLevels, market: $market, precision: $precision, retainSubscriptionForNSeconds: $retainSubscriptionForNSeconds, delayed: $delayed) { __typename ${fields.join(' ')} }
      }`),
      { numLevels, market, precision, retainSubscriptionForNSeconds, delayed },
    ).then((results) => results['bookSnapshot']);
  }

  /**
 * Get a snapshot of the marketdata for a given market, at a given time.  If no
latest_at_or_before is provided, the most recent snapshot is returned.
 * @template {keyof MarketSnapshot} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {MarketId} market
 * @param {DateTime} [latestAtOrBefore]
 * @returns {Promise<Pick<MarketSnapshot, Fields | '__typename'> | null>}
 **/
  async marketSnapshot(fields, market, latestAtOrBefore) {
    return this.execute(
      graphql(`query MarketSnapshot($market: MarketId!, $latestAtOrBefore: DateTime) {
        marketSnapshot(market: $market, latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
      }`),
      { market, latestAtOrBefore },
    ).then((results) => results['marketSnapshot']);
  }

  /**
 * Get snapshots of all markets for the given time.  If no latest_at_or_before is provided,
the most recent snapshots are returned.
 * @template {keyof MarketSnapshot} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {DateTime} [latestAtOrBefore]
 * @returns {Promise<Pick<MarketSnapshot, Fields | '__typename'>[]>}
 **/
  async marketsSnapshots(fields, latestAtOrBefore) {
    return this.execute(
      graphql(`query MarketsSnapshots($latestAtOrBefore: DateTime) {
        marketsSnapshots(latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
      }`),
      { latestAtOrBefore },
    ).then((results) => results['marketsSnapshots']);
  }

  /**
   * Get a snapshot of the options data for a given underlying, at a given time.
   * @template {keyof OptionsMarketSnapshot} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {ProductId} underlying
   * @param {DateTime} [latestAtOrBefore]
   * @returns {Promise<Pick<OptionsMarketSnapshot, Fields | '__typename'>[]>}
   **/
  async optionsMarketSnapshots(fields, underlying, latestAtOrBefore) {
    return this.execute(
      graphql(`query OptionsMarketSnapshots($underlying: ProductId!, $latestAtOrBefore: DateTime) {
        optionsMarketSnapshots(underlying: $underlying, latestAtOrBefore: $latestAtOrBefore) { __typename ${fields.join(' ')} }
      }`),
      { underlying, latestAtOrBefore },
    ).then((results) => results['optionsMarketSnapshots']);
  }

  /**
   * Get the current known balances and positions for a given counterparty.
   * @template {keyof AccountSummaries} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {RouteId} route
   * @param {VenueId} venue
   * @returns {Promise<Pick<AccountSummaries, Fields | '__typename'>>}
   **/
  async accountSummariesForCpty(fields, route, venue) {
    return this.execute(
      graphql(`query AccountSummariesForCpty($route: RouteId!, $venue: VenueId!) {
        accountSummariesForCpty(route: $route, venue: $venue) { __typename ${fields.join(' ')} }
      }`),
      { route, venue },
    ).then((results) => results['accountSummariesForCpty']);
  }

  /**
   * Get all current known balances and positions for all counterparties.
   * @template {keyof AccountSummaries} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<AccountSummaries, Fields | '__typename'>[]>}
   **/
  async accountSummaries(fields) {
    return this.execute(
      graphql(`query AccountSummaries {
        accountSummaries { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['accountSummaries']);
  }

  /**
   * Get all fills for a given venue, route, base, and quote.
   * @template {keyof Fills} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {VenueId} [venue]
   * @param {RouteId} [route]
   * @param {ProductId} [base]
   * @param {ProductId} [quote]
   * @returns {Promise<Pick<Fills, Fields | '__typename'>>}
   **/
  async fills(fields, venue, route, base, quote) {
    return this.execute(
      graphql(`query Fills($venue: VenueId, $route: RouteId, $base: ProductId, $quote: ProductId) {
        fills(venue: $venue, route: $route, base: $base, quote: $quote) { __typename ${fields.join(' ')} }
      }`),
      { venue, route, base, quote },
    ).then((results) => results['fills']);
  }

  /**
   * Find order details by order ID from the OMS.
   * @template {keyof OrderLog} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<OrderLog, Fields | '__typename'> | null>}
   **/
  async order(fields, orderId) {
    return this.execute(
      graphql(`query Order($orderId: OrderId!) {
        order(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['order']);
  }

  /**
   * List all open orders known to the OMS.
   * @template {keyof OrderLog} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<OrderLog, Fields | '__typename'>[]>}
   **/
  async openOrders(fields) {
    return this.execute(
      graphql(`query OpenOrders {
        openOrders { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['openOrders']);
  }

  /**
   * List all recently outed orders known to the OMS.
   * @template {keyof OrderLog} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {DateTime} [fromInclusive]
   * @param {DateTime} [toExclusive]
   * @returns {Promise<Pick<OrderLog, Fields | '__typename'>[]>}
   **/
  async outedOrders(fields, fromInclusive, toExclusive) {
    return this.execute(
      graphql(`query OutedOrders($fromInclusive: DateTime, $toExclusive: DateTime) {
        outedOrders(fromInclusive: $fromInclusive, toExclusive: $toExclusive) { __typename ${fields.join(' ')} }
      }`),
      { fromInclusive, toExclusive },
    ).then((results) => results['outedOrders']);
  }

  /**
   * Query historical OHLCV candles for a given market, candle width, and time range.
   * @template {keyof CandleV1} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {CandleWidth} width
   * @param {DateTime} end
   * @param {DateTime} start
   * @param {MarketId} id
   * @returns {Promise<Pick<CandleV1, Fields | '__typename'>[]>}
   **/
  async historicalCandles(fields, width, end, start, id) {
    return this.execute(
      graphql(`query HistoricalCandles($width: CandleWidth!, $end: DateTime!, $start: DateTime!, $id: MarketId!) {
        historicalCandles(width: $width, end: $end, start: $start, id: $id) { __typename ${fields.join(' ')} }
      }`),
      { width, end, start, id },
    ).then((results) => results['historicalCandles']);
  }

  /**
   * Query TCA pnl / marks stats, id is an optional field but the dates are required
   * @template {keyof TcaMarksV1} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {DateTime} toExclusive
   * @param {DateTime} fromInclusive
   * @param {MarketId} [id]
   * @returns {Promise<Pick<TcaMarksV1, Fields | '__typename'>[]>}
   **/
  async tcaMarks(fields, toExclusive, fromInclusive, id) {
    return this.execute(
      graphql(`query TcaMarks($toExclusive: DateTime!, $fromInclusive: DateTime!, $id: MarketId) {
        tcaMarks(toExclusive: $toExclusive, fromInclusive: $fromInclusive, id: $id) { __typename ${fields.join(' ')} }
      }`),
      { toExclusive, fromInclusive, id },
    ).then((results) => results['tcaMarks']);
  }

  /**
   * Query TCA summary stats, id is an optional field but the dates are required
   * @template {keyof TcaSummaryV1} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {DateTime} toExclusive
   * @param {DateTime} fromInclusive
   * @param {String} [currency]
   * @param {MarketId} [id]
   * @returns {Promise<Pick<TcaSummaryV1, Fields | '__typename'>[]>}
   **/
  async tcaSummary(fields, toExclusive, fromInclusive, currency, id) {
    return this.execute(
      graphql(`query TcaSummary($toExclusive: DateTime!, $fromInclusive: DateTime!, $currency: String, $id: MarketId) {
        tcaSummary(toExclusive: $toExclusive, fromInclusive: $fromInclusive, currency: $currency, id: $id) { __typename ${fields.join(' ')} }
      }`),
      { toExclusive, fromInclusive, currency, id },
    ).then((results) => results['tcaSummary']);
  }

  /**
 * Query TCA balance pnl stats, the account_id is a required field.
The following filtering is allowed ..
If no venue is provided then all venues will be included
If use_purchasing_power is false or not provided then we will use
  the balance column in the table. If it's true then we will use
  the purchasing power column. This is needed for the rfb environment
 * @template {keyof TcaBalancePnlV1} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {AccountId} accountId
 * @param {VenueId} [venueId]
 * @param {Boolean} [usePurchasingPower]
 * @returns {Promise<Pick<TcaBalancePnlV1, Fields | '__typename'>[]>}
 **/
  async tcaBalancePnl(fields, accountId, venueId, usePurchasingPower) {
    return this.execute(
      graphql(`query TcaBalancePnl($accountId: AccountId!, $venueId: VenueId, $usePurchasingPower: Boolean) {
        tcaBalancePnl(accountId: $accountId, venueId: $venueId, usePurchasingPower: $usePurchasingPower) { __typename ${fields.join(' ')} }
      }`),
      { accountId, venueId, usePurchasingPower },
    ).then((results) => results['tcaBalancePnl']);
  }

  /**
 * Query TCA balance pnl timeseries, the account_id and venue_id are
required fields. If both date ranges are not valid then we will return
the timeseries for the last rolling 24 hours. If they are both provided
then the timeseries will return hourly data points for the range provided
If use_purchasing_power is false or not provided then we will use
  the balance column in the table. If it's true then we will use
  the purchasing power column. This is needed for the rfb environment
 * @template {keyof TcaPnlV1} Fields
 * @param {Array<Fields>} fields Fields to select in response type
 * @param {VenueId} venueId
 * @param {AccountId} accountId
 * @param {DateTime} [fromInclusive]
 * @param {DateTime} [toExclusive]
 * @param {Boolean} [usePurchasingPower]
 * @returns {Promise<Pick<TcaPnlV1, Fields | '__typename'>[]>}
 **/
  async tcaBalancePnlTimeseries(
    fields,
    venueId,
    accountId,
    fromInclusive,
    toExclusive,
    usePurchasingPower,
  ) {
    return this.execute(
      graphql(`query TcaBalancePnlTimeseries($venueId: VenueId!, $accountId: AccountId!, $fromInclusive: DateTime, $toExclusive: DateTime, $usePurchasingPower: Boolean) {
        tcaBalancePnlTimeseries(venueId: $venueId, accountId: $accountId, fromInclusive: $fromInclusive, toExclusive: $toExclusive, usePurchasingPower: $usePurchasingPower) { __typename ${fields.join(' ')} }
      }`),
      { venueId, accountId, fromInclusive, toExclusive, usePurchasingPower },
    ).then((results) => results['tcaBalancePnlTimeseries']);
  }

  /**
   * Get a snapshot of token info, sourced from CoinGecko and CoinMarketCap.
   * @template {keyof CoinInfo} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<CoinInfo, Fields | '__typename'>[]>}
   **/
  async coinInfos(fields) {
    return this.execute(
      graphql(`query CoinInfos {
        coinInfos { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['coinInfos']);
  }

  /**
   * Get token info for a given product.
   * @template {keyof CoinInfo} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {ProductId} product
   * @returns {Promise<Pick<CoinInfo, Fields | '__typename'> | null>}
   **/
  async coinInfo(fields, product) {
    return this.execute(
      graphql(`query CoinInfo($product: ProductId!) {
        coinInfo(product: $product) { __typename ${fields.join(' ')} }
      }`),
      { product },
    ).then((results) => results['coinInfo']);
  }

  /**
   * Get CME product group info.
   * @template {keyof CmeProductGroupInfo} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<CmeProductGroupInfo, Fields | '__typename'>[]>}
   **/
  async cmeProductGroupInfos(fields) {
    return this.execute(
      graphql(`query CmeProductGroupInfos {
        cmeProductGroupInfos { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['cmeProductGroupInfos']);
  }

  /**
   * Find a generic algo order and its details by parent order ID.
   * @template {keyof AlgoOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<AlgoOrder, Fields | '__typename'> | null>}
   **/
  async algoOrder(fields, orderId) {
    return this.execute(
      graphql(`query AlgoOrder($orderId: OrderId!) {
        algoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['algoOrder']);
  }

  /**
   * Find and return generic algo order status by parent order ID.
   * @template {keyof AlgoStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<AlgoStatus, Fields | '__typename'>[]>}
   **/
  async algoStatus(fields, orderId) {
    return this.execute(
      graphql(`query AlgoStatus($orderId: OrderId) {
        algoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['algoStatus']);
  }

  /**
   * Find and return generic algo logs by parent order ID.
   * @template {keyof AlgoLog} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<AlgoLog, Fields | '__typename'> | null>}
   **/
  async algoLog(fields, orderId) {
    return this.execute(
      graphql(`query AlgoLog($orderId: OrderId!) {
        algoLog(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['algoLog']);
  }

  /**
   * Find and return TWAP algo order details by parent order ID.
   * @template {keyof TwapOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<TwapOrder, Fields | '__typename'> | null>}
   **/
  async twapOrder(fields, orderId) {
    return this.execute(
      graphql(`query TwapOrder($orderId: OrderId!) {
        twapOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['twapOrder']);
  }

  /**
   * Find and return TWAP algo status by parent order ID.
   * @template {keyof TwapStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<TwapStatus, Fields | '__typename'>[]>}
   **/
  async twapStatus(fields, orderId) {
    return this.execute(
      graphql(`query TwapStatus($orderId: OrderId) {
        twapStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['twapStatus']);
  }

  /**
   * Find and return POV order details by parent order ID.
   * @template {keyof PovAlgoOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<PovAlgoOrder, Fields | '__typename'> | null>}
   **/
  async povOrder(fields, orderId) {
    return this.execute(
      graphql(`query PovOrder($orderId: OrderId!) {
        povOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['povOrder']);
  }

  /**
   * Find and return POV algo status by parent order ID.
   * @template {keyof PovAlgoStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<PovAlgoStatus, Fields | '__typename'>[]>}
   **/
  async povStatus(fields, orderId) {
    return this.execute(
      graphql(`query PovStatus($orderId: OrderId) {
        povStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['povStatus']);
  }

  /**
   * Find and return SOR order details by parent order ID.
   * @template {keyof SmartOrderRouterOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<SmartOrderRouterOrder, Fields | '__typename'> | null>}
   **/
  async smartOrderRouterOrder(fields, orderId) {
    return this.execute(
      graphql(`query SmartOrderRouterOrder($orderId: OrderId!) {
        smartOrderRouterOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['smartOrderRouterOrder']);
  }

  /**
   * Find and return SOR algo status by parent order ID.
   * @template {keyof SmartOrderRouterStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<SmartOrderRouterStatus, Fields | '__typename'>[]>}
   **/
  async smartOrderRouterStatus(fields, orderId) {
    return this.execute(
      graphql(`query SmartOrderRouterStatus($orderId: OrderId) {
        smartOrderRouterStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['smartOrderRouterStatus']);
  }

  /**
   * Find and return MM algo order details by parent order ID.
   * @template {keyof MmAlgoOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<MmAlgoOrder, Fields | '__typename'> | null>}
   **/
  async mmAlgoOrder(fields, orderId) {
    return this.execute(
      graphql(`query MmAlgoOrder($orderId: OrderId!) {
        mmAlgoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['mmAlgoOrder']);
  }

  /**
   * Find and return spread algo status by parent order ID.
   * @template {keyof MmAlgoOrder} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} orderId
   * @returns {Promise<Pick<MmAlgoOrder, Fields | '__typename'> | null>}
   **/
  async spreadAlgoOrder(fields, orderId) {
    return this.execute(
      graphql(`query SpreadAlgoOrder($orderId: OrderId!) {
        spreadAlgoOrder(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['spreadAlgoOrder']);
  }

  /**
   * Find and return MM algo status by parent order ID.
   * @template {keyof MmAlgoStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<MmAlgoStatus, Fields | '__typename'>[]>}
   **/
  async mmAlgoStatus(fields, orderId) {
    return this.execute(
      graphql(`query MmAlgoStatus($orderId: OrderId) {
        mmAlgoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['mmAlgoStatus']);
  }

  /**
   * Find and return spread algo status by parent order ID.
   * @template {keyof MmAlgoStatus} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {OrderId} [orderId]
   * @returns {Promise<Pick<MmAlgoStatus, Fields | '__typename'>[]>}
   **/
  async spreadAlgoStatus(fields, orderId) {
    return this.execute(
      graphql(`query SpreadAlgoStatus($orderId: OrderId) {
        spreadAlgoStatus(orderId: $orderId) { __typename ${fields.join(' ')} }
      }`),
      { orderId },
    ).then((results) => results['spreadAlgoStatus']);
  }

  /**
   * Create a new API key
   * @template {keyof ApiKey} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @returns {Promise<Pick<ApiKey, Fields | '__typename'>>}
   **/
  async createApiKey(fields) {
    return this.execute(
      graphql(`mutation CreateApiKey {
        createApiKey { __typename ${fields.join(' ')} }
      }`),
    ).then((results) => results['createApiKey']);
  }

  /**
   * Create a new API key for Telegram
   * @template {keyof ApiKey} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {String} telegramId
   * @returns {Promise<Pick<ApiKey, Fields | '__typename'>>}
   **/
  async createTelegramApiKey(fields, telegramId) {
    return this.execute(
      graphql(`mutation CreateTelegramApiKey($telegramId: String!) {
        createTelegramApiKey(telegramId: $telegramId) { __typename ${fields.join(' ')} }
      }`),
      { telegramId },
    ).then((results) => results['createTelegramApiKey']);
  }

  /**
   * Remove all Telegram API keys
   * @returns {Promise<Boolean>}
   **/
  async removeTelegramApiKeys() {
    return this.execute(
      graphql(`mutation RemoveTelegramApiKeys {
        removeTelegramApiKeys
      }`),
    ).then((results) => results['removeTelegramApiKeys']);
  }

  /**
   * Remove an API key
   * @param {String} apiKey
   * @returns {Promise<Boolean>}
   **/
  async removeApiKey(apiKey) {
    return this.execute(
      graphql(`mutation RemoveApiKey($apiKey: String!) {
        removeApiKey(apiKey: $apiKey)
      }`),
      { apiKey },
    ).then((results) => results['removeApiKey']);
  }

  /**
   * Set credentials for a given component id.
   * @param {String} credentials
   * @param {ComponentId} componentId
   * @returns {Promise<Boolean>}
   **/
  async setCredentials(credentials, componentId) {
    return this.execute(
      graphql(`mutation SetCredentials($credentials: String!, $componentId: ComponentId!) {
        setCredentials(credentials: $credentials, componentId: $componentId)
      }`),
      { credentials, componentId },
    ).then((results) => results['setCredentials']);
  }

  /**
   * Set/unset market favorited by current user.
   * @template {keyof Market} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {UpdateMarket} payload
   * @returns {Promise<Pick<Market, Fields | '__typename'> | null>}
   **/
  async updateMarket(fields, payload) {
    return this.execute(
      graphql(`mutation UpdateMarket($payload: UpdateMarket!) {
        updateMarket(payload: $payload) { __typename ${fields.join(' ')} }
      }`),
      { payload },
    ).then((results) => results['updateMarket']);
  }

  /**
   * Send an order to Architect.
   * @param {CreateOrder} order
   * @returns {Promise<OrderId>}
   **/
  async createOrder(order) {
    return this.execute(
      graphql(`mutation CreateOrder($order: CreateOrder!) {
        createOrder(order: $order)
      }`),
      { order },
    ).then((results) => results['createOrder']);
  }

  /**
   * Send multiple orders to Architect.
   * @param {CreateOrder[]} orders
   * @returns {Promise<OrderId[]>}
   **/
  async createOrders(orders) {
    return this.execute(
      graphql(`mutation CreateOrders($orders: [CreateOrder!]!) {
        createOrders(orders: $orders)
      }`),
      { orders },
    ).then((results) => results['createOrders']);
  }

  /**
   * Cancel an Architect order.
   * @param {OrderId} orderId
   * @returns {Promise<OrderId>}
   **/
  async cancelOrder(orderId) {
    return this.execute(
      graphql(`mutation CancelOrder($orderId: OrderId!) {
        cancelOrder(orderId: $orderId)
      }`),
      { orderId },
    ).then((results) => results['cancelOrder']);
  }

  /**
   * Cancel multiple Architect orders.
   * @param {OrderId[]} orderIds
   * @returns {Promise<OrderId[]>}
   **/
  async cancelOrders(orderIds) {
    return this.execute(
      graphql(`mutation CancelOrders($orderIds: [OrderId!]!) {
        cancelOrders(orderIds: $orderIds)
      }`),
      { orderIds },
    ).then((results) => results['cancelOrders']);
  }

  /**
 * Cancel all orders on component, regardless of architect order state
If venue is specified it will act as filter if the component manages multiple counterparties (oms for example)
 * @param {VenueId} [venueId]
 * @returns {Promise<VenueId | null>}
 **/
  async cancelAllOrders(venueId) {
    return this.execute(
      graphql(`mutation CancelAllOrders($venueId: VenueId) {
        cancelAllOrders(venueId: $venueId)
      }`),
      { venueId },
    ).then((results) => results['cancelAllOrders']);
  }

  /**
   * @param {AlgoControlCommand} command
   * @param {OrderId} orderId
   * @returns {Promise<OrderId>}
   **/
  async sendAlgoControlCommand(command, orderId) {
    return this.execute(
      graphql(`mutation SendAlgoControlCommand($command: AlgoControlCommand!, $orderId: OrderId!) {
        sendAlgoControlCommand(command: $command, orderId: $orderId)
      }`),
      { command, orderId },
    ).then((results) => results['sendAlgoControlCommand']);
  }

  /**
   * Create a new TWAP algo order.
   * @param {CreateTwapAlgo} twapAlgo
   * @returns {Promise<OrderId>}
   **/
  async createTwapAlgo(twapAlgo) {
    return this.execute(
      graphql(`mutation CreateTwapAlgo($twapAlgo: CreateTwapAlgo!) {
        createTwapAlgo(twapAlgo: $twapAlgo)
      }`),
      { twapAlgo },
    ).then((results) => results['createTwapAlgo']);
  }

  /**
   * Create a new POV algo order.
   * @param {CreatePovAlgo} povAlgo
   * @returns {Promise<OrderId>}
   **/
  async createPovAlgo(povAlgo) {
    return this.execute(
      graphql(`mutation CreatePovAlgo($povAlgo: CreatePovAlgo!) {
        createPovAlgo(povAlgo: $povAlgo)
      }`),
      { povAlgo },
    ).then((results) => results['createPovAlgo']);
  }

  /**
   * Preview the execution of an SOR algo.
   * @template {keyof AlgoPreview} Fields
   * @param {Array<Fields>} fields Fields to select in response type
   * @param {CreateSmartOrderRouterAlgo} algo
   * @returns {Promise<Pick<AlgoPreview, Fields | '__typename'> | null>}
   **/
  async previewSmartOrderRouterAlgo(fields, algo) {
    return this.execute(
      graphql(`mutation PreviewSmartOrderRouterAlgo($algo: CreateSmartOrderRouterAlgo!) {
        previewSmartOrderRouterAlgo(algo: $algo) { __typename ${fields.join(' ')} }
      }`),
      { algo },
    ).then((results) => results['previewSmartOrderRouterAlgo']);
  }

  /**
   * Create a new SOR algo order.
   * @param {CreateSmartOrderRouterAlgo} algo
   * @returns {Promise<OrderId>}
   **/
  async createSmartOrderRouterAlgo(algo) {
    return this.execute(
      graphql(`mutation CreateSmartOrderRouterAlgo($algo: CreateSmartOrderRouterAlgo!) {
        createSmartOrderRouterAlgo(algo: $algo)
      }`),
      { algo },
    ).then((results) => results['createSmartOrderRouterAlgo']);
  }

  /**
   * Create a new MM algo order.
   * @param {CreateMmAlgo} mmAlgo
   * @returns {Promise<OrderId>}
   **/
  async createMmAlgo(mmAlgo) {
    return this.execute(
      graphql(`mutation CreateMmAlgo($mmAlgo: CreateMMAlgo!) {
        createMmAlgo(mmAlgo: $mmAlgo)
      }`),
      { mmAlgo },
    ).then((results) => results['createMmAlgo']);
  }

  /**
   * Create a new Spread algo order.
   * @param {CreateSpreadAlgo} spreadAlgo
   * @returns {Promise<OrderId>}
   **/
  async createSpreadAlgo(spreadAlgo) {
    return this.execute(
      graphql(`mutation CreateSpreadAlgo($spreadAlgo: CreateSpreadAlgo!) {
        createSpreadAlgo(spreadAlgo: $spreadAlgo)
      }`),
      { spreadAlgo },
    ).then((results) => results['createSpreadAlgo']);
  }
}
