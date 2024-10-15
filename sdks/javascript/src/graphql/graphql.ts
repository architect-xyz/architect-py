/* eslint-disable */
import { DocumentTypeDecoration } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = {
  [K in keyof T]: T[K];
};
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]?: Maybe<T[SubKey]>;
};
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]: Maybe<T[SubKey]>;
};
export type MakeEmpty<
  T extends { [key: string]: unknown },
  K extends keyof T,
> = { [_ in K]?: never };
export type Incremental<T> =
  | T
  | {
      [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never;
    };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string };
  String: { input: string; output: string };
  Boolean: { input: boolean; output: boolean };
  Int: { input: number; output: number };
  Float: { input: number; output: number };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  AccountId: { input: string; output: string };
  /**
   * Components within an Architect installation are uniquely identified by a 16-bit integer
   * in the range `1..<0xFFFF`.
   *
   * The integers 0 and 0xFFFF are reserved as special values and MUST NOT be used as component IDs.
   *
   * Canonical meanings of special values:
   *
   * * `0x0` -- None/executor/broadcast
   * * `0xFFFF` -- Self/loopback
   */
  ComponentId: { input: string; output: string };
  /**
   * Date in the proleptic Gregorian calendar (without time zone).
   *
   * Represents a description of the date (as used for birthdays, for example).
   * It cannot represent an instant on the time-line.
   *
   * [`Date` scalar][1] compliant.
   *
   * See also [`chrono::NaiveDate`][2] for details.
   *
   * [1]: https://graphql-scalars.dev/docs/scalars/date
   * [2]: https://docs.rs/chrono/latest/chrono/naive/struct.NaiveDate.html
   */
  Date: { input: string; output: string };
  /**
   * Combined date and time (with time zone) in [RFC 3339][0] format.
   *
   * Represents a description of an exact instant on the time-line (such as the
   * instant that a user account was created).
   *
   * [`DateTime` scalar][1] compliant.
   *
   * See also [`chrono::DateTime`][2] for details.
   *
   * [0]: https://datatracker.ietf.org/doc/html/rfc3339#section-5
   * [1]: https://graphql-scalars.dev/docs/scalars/date-time
   * [2]: https://docs.rs/chrono/latest/chrono/struct.DateTime.html
   */
  DateTime: { input: string; output: string };
  /**
   * 128 bit representation of a fixed-precision decimal number.
   *
   * The finite set of values of `Decimal` scalar are of the form
   * m / 10<sup>e</sup>, where m is an integer such that
   * -2<sup>96</sup> < m < 2<sup>96</sup>, and e is an integer between 0 and 28
   * inclusive.
   *
   * Always serializes as `String`. But may be deserialized from `Int` and
   * `Float` values too. It's not recommended to deserialize from a `Float`
   * directly, as the floating point representation may be unexpected.
   *
   * See also [`rust_decimal`] crate for details.
   *
   * [`rust_decimal`]: https://docs.rs/rust_decimal
   */
  Decimal: { input: string; output: string };
  /**
   * An order side/direction or a trade execution side/direction.
   * In GraphQL these are serialized as "buy" or "sell".
   */
  Dir: { input: 'buy' | 'sell'; output: 'buy' | 'sell' };
  /** The ID of a fill */
  FillId: { input: string; output: string };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  MarketId: { input: string; output: string };
  /** System-unique, persistent order identifiers */
  OrderId: { input: string; output: string };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  ProductId: { input: string; output: string };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  RouteId: { input: string; output: string };
  /** A String type */
  Str: { input: string; output: string };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  UserId: { input: string; output: string };
  /**
   * Wrapper type around a UUIDv5 for a given namespace.  These types are
   * parseable from either the UUIDv5 string representation, or from the
   * name itself, as they are 1-1.
   */
  VenueId: { input: string; output: string };
};

/**
 * Fills which we received but couldn't parse fully, return details
 * best effort
 */
export type AberrantFill = {
  __typename?: 'AberrantFill';
  accountId?: Maybe<Scalars['AccountId']['output']>;
  dir?: Maybe<Scalars['Dir']['output']>;
  fee?: Maybe<Fee>;
  fillId: Scalars['FillId']['output'];
  isMaker?: Maybe<Scalars['Boolean']['output']>;
  kind?: Maybe<FillKind>;
  market?: Maybe<Scalars['MarketId']['output']>;
  orderId?: Maybe<Scalars['OrderId']['output']>;
  price?: Maybe<Scalars['Decimal']['output']>;
  quantity?: Maybe<Scalars['Decimal']['output']>;
  recvTime?: Maybe<Scalars['DateTime']['output']>;
  tradeTime?: Maybe<Scalars['DateTime']['output']>;
  trader?: Maybe<Scalars['UserId']['output']>;
};

export type Account = {
  __typename?: 'Account';
  id: Scalars['AccountId']['output'];
  name: Scalars['String']['output'];
  venue?: Maybe<Venue>;
  venueId: Scalars['VenueId']['output'];
};

export type AccountSummaries = {
  __typename?: 'AccountSummaries';
  byAccount: Array<AccountSummary>;
  snapshotTs: Scalars['DateTime']['output'];
};

export type AccountSummary = {
  __typename?: 'AccountSummary';
  account?: Maybe<Account>;
  accountId: Scalars['AccountId']['output'];
  balances: Array<Balance>;
  positions: Array<Position>;
  profitLoss?: Maybe<Scalars['Decimal']['output']>;
  venue?: Maybe<Venue>;
  venueId: Scalars['VenueId']['output'];
};

export type Ack = {
  __typename?: 'Ack';
  order?: Maybe<Order>;
  orderId: Scalars['OrderId']['output'];
};

export enum AlgoControlCommand {
  Pause = 'PAUSE',
  Start = 'START',
  Stop = 'STOP',
}

export enum AlgoKind {
  Chaser = 'CHASER',
  MarketMaker = 'MARKET_MAKER',
  Pov = 'POV',
  SmartOrderRouter = 'SMART_ORDER_ROUTER',
  Spread = 'SPREAD',
  Twap = 'TWAP',
}

export type AlgoLog = {
  __typename?: 'AlgoLog';
  aberrantFills: Array<AberrantFill>;
  fills: Array<Fill>;
  orderId: Scalars['OrderId']['output'];
  rejects: Array<Reject>;
};

export type AlgoOrder = {
  __typename?: 'AlgoOrder';
  account?: Maybe<Scalars['AccountId']['output']>;
  algo: AlgoKind;
  markets: Array<Scalars['MarketId']['output']>;
  orderId: Scalars['OrderId']['output'];
  parentOrderId?: Maybe<Scalars['OrderId']['output']>;
  trader: Scalars['UserId']['output'];
};

export type AlgoPreview = {
  __typename?: 'AlgoPreview';
  orders: Array<Order>;
};

export enum AlgoRunningStatus {
  Done = 'DONE',
  Paused = 'PAUSED',
  Running = 'RUNNING',
}

export type AlgoStatus = {
  __typename?: 'AlgoStatus';
  creationTime: Scalars['DateTime']['output'];
  fractionComplete?: Maybe<Scalars['Float']['output']>;
  lastStatusChange: Scalars['DateTime']['output'];
  order?: Maybe<AlgoOrder>;
  orderId: Scalars['OrderId']['output'];
  status: AlgoRunningStatus;
};

export type ApiKey = {
  __typename?: 'ApiKey';
  apiKey: Scalars['String']['output'];
  apiSecret: Scalars['String']['output'];
  created: Scalars['DateTime']['output'];
  subject: Scalars['String']['output'];
};

export type Balance = {
  __typename?: 'Balance';
  account?: Maybe<Account>;
  accountId: Scalars['AccountId']['output'];
  amount?: Maybe<Scalars['Decimal']['output']>;
  cashExcess?: Maybe<Scalars['Decimal']['output']>;
  marginExcess?: Maybe<Scalars['Decimal']['output']>;
  positionMargin?: Maybe<Scalars['Decimal']['output']>;
  product?: Maybe<Product>;
  productId: Scalars['ProductId']['output'];
  purchasingPower?: Maybe<Scalars['Decimal']['output']>;
  totalMargin?: Maybe<Scalars['Decimal']['output']>;
  venue?: Maybe<Venue>;
  venueId: Scalars['VenueId']['output'];
  yesterdayBalance?: Maybe<Scalars['Decimal']['output']>;
};

export type Book = {
  __typename?: 'Book';
  asks: Array<BookLevel>;
  bids: Array<BookLevel>;
  market: Scalars['MarketId']['output'];
  timestamp: Scalars['DateTime']['output'];
};

export type BookLevel = {
  __typename?: 'BookLevel';
  amount: Scalars['Decimal']['output'];
  price: Scalars['Decimal']['output'];
  total: Scalars['Decimal']['output'];
};

export type Cancel = {
  __typename?: 'Cancel';
  order?: Maybe<Order>;
  orderId: Scalars['OrderId']['output'];
};

export type CancelAll = {
  __typename?: 'CancelAll';
  venueId?: Maybe<Scalars['VenueId']['output']>;
};

/**
 * NB: buy_volume + sell_volume <> volume; volume may count trades
 * that don't have a discernible direction.
 */
export type CandleV1 = {
  __typename?: 'CandleV1';
  buyVolume: Scalars['Decimal']['output'];
  close: Scalars['Decimal']['output'];
  high: Scalars['Decimal']['output'];
  low: Scalars['Decimal']['output'];
  open: Scalars['Decimal']['output'];
  sellVolume: Scalars['Decimal']['output'];
  time: Scalars['DateTime']['output'];
  volume: Scalars['Decimal']['output'];
};

export enum CandleWidth {
  FifteenMinute = 'FIFTEEN_MINUTE',
  FiveSecond = 'FIVE_SECOND',
  OneDay = 'ONE_DAY',
  OneHour = 'ONE_HOUR',
  OneMinute = 'ONE_MINUTE',
  OneSecond = 'ONE_SECOND',
}

export type CmeProductGroupInfo = {
  __typename?: 'CmeProductGroupInfo';
  altGlobexMinTick?: Maybe<Scalars['String']['output']>;
  altGlobexTickConstraint?: Maybe<Scalars['String']['output']>;
  altMinQuoteLife?: Maybe<Scalars['String']['output']>;
  assetClass?: Maybe<Scalars['String']['output']>;
  assetSubClass?: Maybe<Scalars['String']['output']>;
  assignmentMethod?: Maybe<Scalars['String']['output']>;
  blockTradeEligible?: Maybe<Scalars['String']['output']>;
  calendarTickRules?: Maybe<Scalars['String']['output']>;
  category?: Maybe<Scalars['String']['output']>;
  clearingCabPx?: Maybe<Scalars['String']['output']>;
  clearingOrgId?: Maybe<Scalars['String']['output']>;
  clearingSymbol?: Maybe<Scalars['String']['output']>;
  clearportEligible?: Maybe<Scalars['String']['output']>;
  clearportSchedule?: Maybe<Scalars['String']['output']>;
  commodityStandards?: Maybe<Scalars['String']['output']>;
  contractNotionalAmount?: Maybe<Scalars['Decimal']['output']>;
  contraryInstructionsAllowed?: Maybe<Scalars['String']['output']>;
  dailyFlag?: Maybe<Scalars['String']['output']>;
  daysOrHours?: Maybe<Scalars['String']['output']>;
  defaultListingRules?: Maybe<Scalars['String']['output']>;
  defaultMinTick?: Maybe<Scalars['String']['output']>;
  dirtyPriceRounding?: Maybe<Scalars['String']['output']>;
  dirtyPriceTick?: Maybe<Scalars['String']['output']>;
  ebfEligible?: Maybe<Scalars['String']['output']>;
  efpEligible?: Maybe<Scalars['String']['output']>;
  efrEligible?: Maybe<Scalars['String']['output']>;
  exchangeClearing?: Maybe<Scalars['String']['output']>;
  exchangeGlobex?: Maybe<Scalars['String']['output']>;
  exerciseStyle?: Maybe<Scalars['String']['output']>;
  exerciseStyleAmericanEuropean?: Maybe<Scalars['String']['output']>;
  fixedPayout?: Maybe<Scalars['Float']['output']>;
  fixingSource?: Maybe<Scalars['String']['output']>;
  fixingTimeZone?: Maybe<Scalars['String']['output']>;
  flexEligible?: Maybe<Scalars['String']['output']>;
  floorCallSymbol?: Maybe<Scalars['String']['output']>;
  floorEligible?: Maybe<Scalars['String']['output']>;
  floorListingRules?: Maybe<Scalars['String']['output']>;
  floorPutSymbol?: Maybe<Scalars['String']['output']>;
  floorSchedule?: Maybe<Scalars['String']['output']>;
  fractional?: Maybe<Scalars['String']['output']>;
  gcBasketIdentifier?: Maybe<Scalars['String']['output']>;
  globexCabPx?: Maybe<Scalars['String']['output']>;
  globexDisplayFactor?: Maybe<Scalars['String']['output']>;
  globexEligible?: Maybe<Scalars['String']['output']>;
  globexGroupCode?: Maybe<Scalars['String']['output']>;
  globexGroupDescr?: Maybe<Scalars['String']['output']>;
  globexGtEligible?: Maybe<Scalars['String']['output']>;
  globexListingRules?: Maybe<Scalars['String']['output']>;
  globexMatchAlgo?: Maybe<Scalars['String']['output']>;
  globexMinTick?: Maybe<Scalars['String']['output']>;
  globexProductCode?: Maybe<Scalars['String']['output']>;
  globexSchedule?: Maybe<Scalars['String']['output']>;
  goodForSession?: Maybe<Scalars['String']['output']>;
  ilinkEligible?: Maybe<Scalars['String']['output']>;
  isBticProduct?: Maybe<Scalars['String']['output']>;
  isDerivedBlockEligible?: Maybe<Scalars['String']['output']>;
  isEfixProduct?: Maybe<Scalars['String']['output']>;
  isPmEligible?: Maybe<Scalars['String']['output']>;
  isSyntheticProduct?: Maybe<Scalars['String']['output']>;
  isTacoProduct?: Maybe<Scalars['String']['output']>;
  isTamProduct?: Maybe<Scalars['String']['output']>;
  isTasProduct?: Maybe<Scalars['String']['output']>;
  isTmacProduct?: Maybe<Scalars['String']['output']>;
  itcCode?: Maybe<Scalars['String']['output']>;
  itmOtm?: Maybe<Scalars['String']['output']>;
  lastDeliveryRules?: Maybe<Scalars['String']['output']>;
  lastUpdated?: Maybe<Scalars['String']['output']>;
  limitRules?: Maybe<Scalars['String']['output']>;
  mainFraction?: Maybe<Scalars['Int']['output']>;
  markerStlmtRules?: Maybe<Scalars['String']['output']>;
  marketData?: Maybe<Scalars['String']['output']>;
  marketSegmentId?: Maybe<Scalars['Int']['output']>;
  massQuoteEligible?: Maybe<Scalars['String']['output']>;
  masterSymbol?: Maybe<Scalars['String']['output']>;
  maxBidAskConstraint?: Maybe<Scalars['String']['output']>;
  maxGlobexOrdQty?: Maybe<Scalars['String']['output']>;
  mdp3Channel?: Maybe<Scalars['String']['output']>;
  midcurveOptionsRules?: Maybe<Scalars['String']['output']>;
  midcurveTickRules?: Maybe<Scalars['String']['output']>;
  minCabinetTickRules?: Maybe<Scalars['String']['output']>;
  minClearportFloorTick?: Maybe<Scalars['String']['output']>;
  minClearportTick?: Maybe<Scalars['String']['output']>;
  minDaysToMat?: Maybe<Scalars['String']['output']>;
  minGlobexOrdQty?: Maybe<Scalars['String']['output']>;
  minIncrementalOrder?: Maybe<Scalars['String']['output']>;
  minOutrightTick?: Maybe<Scalars['String']['output']>;
  minQtrlySerialTick?: Maybe<Scalars['String']['output']>;
  minimumHalfTick?: Maybe<Scalars['String']['output']>;
  minimumTickNote?: Maybe<Scalars['String']['output']>;
  negativePxEligible?: Maybe<Scalars['String']['output']>;
  negativeStrikeEligible?: Maybe<Scalars['String']['output']>;
  onMtf?: Maybe<Scalars['String']['output']>;
  onSef?: Maybe<Scalars['String']['output']>;
  optStyle?: Maybe<Scalars['String']['output']>;
  otcEligible?: Maybe<Scalars['String']['output']>;
  parOrMoney?: Maybe<Scalars['String']['output']>;
  priceBand?: Maybe<Scalars['String']['output']>;
  priceMultiplier?: Maybe<Scalars['Decimal']['output']>;
  pricePrecision?: Maybe<Scalars['String']['output']>;
  priceQuotation?: Maybe<Scalars['String']['output']>;
  productGuid?: Maybe<Scalars['String']['output']>;
  productName?: Maybe<Scalars['String']['output']>;
  pxQuoteMethod?: Maybe<Scalars['String']['output']>;
  pxUnitOfMeasure?: Maybe<Scalars['String']['output']>;
  pxUnitOfMeasureQty?: Maybe<Scalars['Int']['output']>;
  quarterlyListingRules?: Maybe<Scalars['String']['output']>;
  rbtEligibleInd?: Maybe<Scalars['String']['output']>;
  reducedTickNotes?: Maybe<Scalars['String']['output']>;
  regularListingRules?: Maybe<Scalars['String']['output']>;
  repoYearDays?: Maybe<Scalars['String']['output']>;
  reportablePositions?: Maybe<Scalars['String']['output']>;
  rfqCrossEligible?: Maybe<Scalars['String']['output']>;
  sector?: Maybe<Scalars['String']['output']>;
  securityType: CmeSecurityType;
  serialListingRules?: Maybe<Scalars['String']['output']>;
  settlCcy?: Maybe<Scalars['String']['output']>;
  settleMethod?: Maybe<Scalars['String']['output']>;
  settlePxCcy?: Maybe<Scalars['String']['output']>;
  settleUsingFixingPx?: Maybe<Scalars['String']['output']>;
  settlementAtExpiration?: Maybe<Scalars['String']['output']>;
  settlementLocale?: Maybe<Scalars['String']['output']>;
  settlementProcedure?: Maybe<Scalars['String']['output']>;
  settlementType?: Maybe<Scalars['String']['output']>;
  sizePriorityQty?: Maybe<Scalars['String']['output']>;
  spreadPricingConvention?: Maybe<Scalars['String']['output']>;
  stdTradingHours?: Maybe<Scalars['String']['output']>;
  strategyType?: Maybe<Scalars['String']['output']>;
  strikePriceInterval?: Maybe<Scalars['String']['output']>;
  subCategory?: Maybe<Scalars['String']['output']>;
  subSector?: Maybe<Scalars['String']['output']>;
  subfraction?: Maybe<Scalars['String']['output']>;
  subtype?: Maybe<Scalars['String']['output']>;
  topEligible?: Maybe<Scalars['String']['output']>;
  totClearport?: Maybe<Scalars['String']['output']>;
  totDefault?: Maybe<Scalars['String']['output']>;
  totFloor?: Maybe<Scalars['String']['output']>;
  totGlobex?: Maybe<Scalars['String']['output']>;
  totLtd?: Maybe<Scalars['String']['output']>;
  totMidcurve?: Maybe<Scalars['String']['output']>;
  totQuarterly?: Maybe<Scalars['String']['output']>;
  totSerial?: Maybe<Scalars['String']['output']>;
  tradeCloseOffSet?: Maybe<Scalars['String']['output']>;
  tradePxCcy?: Maybe<Scalars['String']['output']>;
  tradingCutOffTime?: Maybe<Scalars['String']['output']>;
  unitOfMeasure?: Maybe<Scalars['String']['output']>;
  unitOfMeasureQty?: Maybe<Scalars['Decimal']['output']>;
  url?: Maybe<Scalars['String']['output']>;
  valuationMethod?: Maybe<Scalars['String']['output']>;
  varCabPxHigh?: Maybe<Scalars['String']['output']>;
  varCabPxLow?: Maybe<Scalars['String']['output']>;
  variableQtyFlag?: Maybe<Scalars['String']['output']>;
};

export enum CmeSecurityType {
  Cash = 'CASH',
  Combo = 'COMBO',
  Fra = 'FRA',
  Fut = 'FUT',
  Fwd = 'FWD',
  Idx = 'IDX',
  Index = 'INDEX',
  Irs = 'IRS',
  Ooc = 'OOC',
  Oof = 'OOF',
}

export type CoinInfo = {
  __typename?: 'CoinInfo';
  circulatingSupply?: Maybe<Scalars['Decimal']['output']>;
  fullyDilutedMarketCap?: Maybe<Scalars['Decimal']['output']>;
  infiniteSupply: Scalars['Boolean']['output'];
  marketCap?: Maybe<Scalars['Decimal']['output']>;
  maxSupply?: Maybe<Scalars['Decimal']['output']>;
  name: Scalars['String']['output'];
  percentChange1h?: Maybe<Scalars['Decimal']['output']>;
  percentChange7d?: Maybe<Scalars['Decimal']['output']>;
  percentChange24h?: Maybe<Scalars['Decimal']['output']>;
  percentChange30d?: Maybe<Scalars['Decimal']['output']>;
  percentChange60d?: Maybe<Scalars['Decimal']['output']>;
  percentChange90d?: Maybe<Scalars['Decimal']['output']>;
  price?: Maybe<Scalars['Decimal']['output']>;
  symbol: Scalars['String']['output'];
  tags: Array<Scalars['String']['output']>;
  totalSupply?: Maybe<Scalars['Decimal']['output']>;
  volume24h?: Maybe<Scalars['Decimal']['output']>;
  volumeChange24h?: Maybe<Scalars['Decimal']['output']>;
};

export type CptyInfo = {
  __typename?: 'CptyInfo';
  canSetCredentials: Scalars['Boolean']['output'];
  componentId: Scalars['ComponentId']['output'];
  route: Route;
  venue: Venue;
};

export type CreateMmAlgo = {
  account?: InputMaybe<Scalars['AccountId']['input']>;
  buyQuantity: Scalars['Decimal']['input'];
  fillLockoutMs: Scalars['Int']['input'];
  market: Scalars['MarketId']['input'];
  maxImproveBbo: Scalars['Decimal']['input'];
  maxPosition: Scalars['Decimal']['input'];
  minPosition: Scalars['Decimal']['input'];
  name: Scalars['Str']['input'];
  orderLockoutMs: Scalars['Int']['input'];
  positionTilt: Scalars['Decimal']['input'];
  refDistFrac: Scalars['Decimal']['input'];
  referencePrice: ReferencePrice;
  rejectLockoutMs: Scalars['Int']['input'];
  sellQuantity: Scalars['Decimal']['input'];
  toleranceFrac: Scalars['Decimal']['input'];
};

export type CreateOrder = {
  account?: InputMaybe<Scalars['AccountId']['input']>;
  dir: Scalars['Dir']['input'];
  limitPrice?: InputMaybe<Scalars['Decimal']['input']>;
  market: Scalars['MarketId']['input'];
  orderType: CreateOrderType;
  postOnly?: InputMaybe<Scalars['Boolean']['input']>;
  quantity: Scalars['Decimal']['input'];
  quoteId?: InputMaybe<Scalars['Str']['input']>;
  source?: InputMaybe<OrderSource>;
  timeInForce: CreateTimeInForce;
  triggerPrice?: InputMaybe<Scalars['Decimal']['input']>;
};

export enum CreateOrderType {
  Limit = 'LIMIT',
  StopLossLimit = 'STOP_LOSS_LIMIT',
  TakeProfitLimit = 'TAKE_PROFIT_LIMIT',
}

export type CreatePovAlgo = {
  account?: InputMaybe<Scalars['AccountId']['input']>;
  dir: Scalars['Dir']['input'];
  endTime: Scalars['DateTime']['input'];
  market: Scalars['MarketId']['input'];
  maxQuantity: Scalars['Decimal']['input'];
  minOrderQuantity: Scalars['Decimal']['input'];
  name: Scalars['Str']['input'];
  orderLockoutMs: Scalars['Int']['input'];
  takeThroughFrac?: InputMaybe<Scalars['Decimal']['input']>;
  targetVolumeFrac: Scalars['Decimal']['input'];
};

export type CreateSmartOrderRouterAlgo = {
  base: Scalars['ProductId']['input'];
  dir: Scalars['Dir']['input'];
  executionTimeLimitMs: Scalars['Int']['input'];
  limitPrice: Scalars['Decimal']['input'];
  markets: Array<Scalars['MarketId']['input']>;
  quote: Scalars['ProductId']['input'];
  targetSize: Scalars['Decimal']['input'];
};

export type CreateSpreadAlgo = {
  account?: InputMaybe<Scalars['AccountId']['input']>;
  buyQuantity: Scalars['Decimal']['input'];
  fillLockoutMs: Scalars['Int']['input'];
  hedgeMarket: CreateSpreadAlgoHedgeMarket;
  market: Scalars['MarketId']['input'];
  maxImproveBbo: Scalars['Decimal']['input'];
  maxPosition: Scalars['Decimal']['input'];
  minPosition: Scalars['Decimal']['input'];
  name: Scalars['Str']['input'];
  orderLockoutMs: Scalars['Int']['input'];
  positionTilt: Scalars['Decimal']['input'];
  refDistFrac: Scalars['Decimal']['input'];
  referencePrice: ReferencePrice;
  rejectLockoutMs: Scalars['Int']['input'];
  sellQuantity: Scalars['Decimal']['input'];
  toleranceFrac: Scalars['Decimal']['input'];
};

export type CreateSpreadAlgoHedgeMarket = {
  conversionRatio: Scalars['Decimal']['input'];
  hedgeFrac: Scalars['Decimal']['input'];
  market: Scalars['MarketId']['input'];
  premium: Scalars['Decimal']['input'];
};

export type CreateTimeInForce = {
  goodTilDate?: InputMaybe<Scalars['DateTime']['input']>;
  instruction: CreateTimeInForceInstruction;
};

export enum CreateTimeInForceInstruction {
  Gtc = 'GTC',
  Gtd = 'GTD',
  Ioc = 'IOC',
}

export type CreateTwapAlgo = {
  account?: InputMaybe<Scalars['AccountId']['input']>;
  dir: Scalars['Dir']['input'];
  endTime: Scalars['DateTime']['input'];
  intervalMs: Scalars['Int']['input'];
  market: Scalars['MarketId']['input'];
  name: Scalars['Str']['input'];
  quantity: Scalars['Decimal']['input'];
  rejectLockoutMs: Scalars['Int']['input'];
  takeThroughFrac?: InputMaybe<Scalars['Decimal']['input']>;
};

export type Environment = {
  __typename?: 'Environment';
  id: Scalars['String']['output'];
  kind: EnvironmentKind;
};

export enum EnvironmentKind {
  Brokerage = 'BROKERAGE',
  Platform = 'PLATFORM',
}

export type ExchangeMarketKind = {
  __typename?: 'ExchangeMarketKind';
  base: Product;
  quote: Product;
};

export type ExchangeSpecificUpdate = {
  __typename?: 'ExchangeSpecificUpdate';
  field: Scalars['String']['output'];
  market: Market;
  value?: Maybe<Scalars['Decimal']['output']>;
};

export type Fee = {
  __typename?: 'Fee';
  amount: Scalars['Decimal']['output'];
  feeCurrency: Scalars['ProductId']['output'];
};

export type Fill = {
  __typename?: 'Fill';
  dir: Scalars['Dir']['output'];
  fillId: Scalars['FillId']['output'];
  kind: FillKind;
  market: Market;
  marketId: Scalars['MarketId']['output'];
  orderId?: Maybe<Scalars['OrderId']['output']>;
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Decimal']['output'];
  recvTime?: Maybe<Scalars['DateTime']['output']>;
  tradeTime: Scalars['DateTime']['output'];
};

export enum FillKind {
  Correction = 'CORRECTION',
  Normal = 'NORMAL',
  Reversal = 'REVERSAL',
}

export type Fills = {
  __typename?: 'Fills';
  aberrant: Array<AberrantFill>;
  normal: Array<Fill>;
};

export type HedgeMarket = {
  __typename?: 'HedgeMarket';
  conversionRatio: Scalars['Decimal']['output'];
  hedgeFrac: Scalars['Decimal']['output'];
  market: Scalars['MarketId']['output'];
  premium: Scalars['Decimal']['output'];
};

export type License = {
  __typename?: 'License';
  expiry?: Maybe<Scalars['DateTime']['output']>;
  tier?: Maybe<LicenseTier>;
  user: Scalars['UserId']['output'];
};

export enum LicenseTier {
  Basic = 'BASIC',
  Professional = 'PROFESSIONAL',
}

export type LimitOrderType = {
  __typename?: 'LimitOrderType';
  limitPrice: Scalars['Decimal']['output'];
  postOnly: Scalars['Boolean']['output'];
};

export type MmAlgoDecision =
  | MmAlgoDecisionCancel
  | MmAlgoDecisionDoNothing
  | MmAlgoDecisionSend;

export type MmAlgoDecisionCancel = {
  __typename?: 'MMAlgoDecisionCancel';
  orderId: Scalars['OrderId']['output'];
  reasons: Array<Reason>;
};

export type MmAlgoDecisionDoNothing = {
  __typename?: 'MMAlgoDecisionDoNothing';
  reasons: Array<Reason>;
};

export type MmAlgoDecisionSend = {
  __typename?: 'MMAlgoDecisionSend';
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Decimal']['output'];
};

export enum MmAlgoKind {
  Mm = 'MM',
  Spread = 'SPREAD',
}

export type MmAlgoOpenOrder = {
  __typename?: 'MMAlgoOpenOrder';
  cancelPending: Scalars['Boolean']['output'];
  orderId: Scalars['OrderId']['output'];
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Decimal']['output'];
};

export type MmAlgoOrder = {
  __typename?: 'MMAlgoOrder';
  account?: Maybe<Scalars['AccountId']['output']>;
  hedgeMarket?: Maybe<HedgeMarket>;
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  maxImproveBbo: Scalars['Decimal']['output'];
  maxPosition: Scalars['Decimal']['output'];
  minPosition: Scalars['Decimal']['output'];
  name: Scalars['String']['output'];
  orderId: Scalars['OrderId']['output'];
  positionTilt: Scalars['Decimal']['output'];
  quantityBuy: Scalars['Decimal']['output'];
  quantitySell: Scalars['Decimal']['output'];
  refDistFrac: Scalars['Decimal']['output'];
  referencePrice: ReferencePrice;
  toleranceFrac: Scalars['Decimal']['output'];
};

export type MmAlgoSide = {
  __typename?: 'MMAlgoSide';
  lastDecision: MmAlgoDecision;
  lastFillTime: Scalars['DateTime']['output'];
  lastOrderTime: Scalars['DateTime']['output'];
  lastRejectTime: Scalars['DateTime']['output'];
  openOrder?: Maybe<MmAlgoOpenOrder>;
  referencePrice?: Maybe<Scalars['Decimal']['output']>;
};

export type MmAlgoStatus = {
  __typename?: 'MMAlgoStatus';
  buyStatus: MmAlgoSide;
  creationTime: Scalars['DateTime']['output'];
  effectiveSpread?: Maybe<Scalars['Decimal']['output']>;
  hedgePosition: Scalars['Decimal']['output'];
  kind: MmAlgoKind;
  missRatio: Scalars['Decimal']['output'];
  order?: Maybe<MmAlgoOrder>;
  orderId: Scalars['OrderId']['output'];
  position: Scalars['Decimal']['output'];
  sellStatus: MmAlgoSide;
  status: AlgoRunningStatus;
};

export type Market = {
  __typename?: 'Market';
  cmeProductGroupInfo?: Maybe<CmeProductGroupInfo>;
  exchangeSymbol: Scalars['String']['output'];
  firstNoticeDate?: Maybe<Scalars['DateTime']['output']>;
  id: Scalars['MarketId']['output'];
  initialMargin?: Maybe<Scalars['Decimal']['output']>;
  isDelisted: Scalars['Boolean']['output'];
  isFavorite: Scalars['Boolean']['output'];
  kind: MarketKind;
  lastTradingDate?: Maybe<Scalars['DateTime']['output']>;
  maintenanceMargin?: Maybe<Scalars['Decimal']['output']>;
  minOrderQuantity: Scalars['Decimal']['output'];
  minOrderQuantityUnit: MinOrderQuantityUnit;
  name: Scalars['String']['output'];
  route: Route;
  stepSize: Scalars['Decimal']['output'];
  tickSize: Scalars['Decimal']['output'];
  venue: Venue;
};

export type MarketFilter = {
  base?: InputMaybe<Scalars['Str']['input']>;
  includeDelisted?: InputMaybe<Scalars['Boolean']['input']>;
  maxResults?: InputMaybe<Scalars['Int']['input']>;
  onlyFavorites?: InputMaybe<Scalars['Boolean']['input']>;
  quote?: InputMaybe<Scalars['Str']['input']>;
  resultsOffset?: InputMaybe<Scalars['Int']['input']>;
  route?: InputMaybe<Scalars['Str']['input']>;
  searchString?: InputMaybe<Scalars['Str']['input']>;
  sortByVolumeDesc?: InputMaybe<Scalars['Boolean']['input']>;
  underlying?: InputMaybe<Scalars['Str']['input']>;
  venue?: InputMaybe<Scalars['Str']['input']>;
};

export type MarketKind =
  | ExchangeMarketKind
  | PoolMarketKind
  | UnknownMarketKind;

export type MarketSnapshot = {
  __typename?: 'MarketSnapshot';
  askPrice?: Maybe<Scalars['Decimal']['output']>;
  bidPrice?: Maybe<Scalars['Decimal']['output']>;
  high24h?: Maybe<Scalars['Decimal']['output']>;
  lastPrice?: Maybe<Scalars['Decimal']['output']>;
  low24h?: Maybe<Scalars['Decimal']['output']>;
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  open24h?: Maybe<Scalars['Decimal']['output']>;
  volume24h?: Maybe<Scalars['Decimal']['output']>;
};

export type Me = {
  __typename?: 'Me';
  email: Scalars['String']['output'];
  environment: Environment;
  isStaff: Scalars['Boolean']['output'];
  license?: Maybe<License>;
  userId: Scalars['UserId']['output'];
};

export enum MinOrderQuantityUnit {
  Base = 'BASE',
  Quote = 'QUOTE',
}

export type MutationRoot = {
  __typename?: 'MutationRoot';
  /**
   * Cancel all orders on component, regardless of architect order state
   * If venue is specified it will act as filter if the component manages multiple counterparties (oms for example)
   */
  cancelAllOrders?: Maybe<Scalars['VenueId']['output']>;
  /** Cancel an Architect order. */
  cancelOrder: Scalars['OrderId']['output'];
  /** Cancel multiple Architect orders. */
  cancelOrders: Array<Scalars['OrderId']['output']>;
  /** Create a new API key */
  createApiKey: ApiKey;
  /** Create a new MM algo order. */
  createMmAlgo: Scalars['OrderId']['output'];
  /** Send an order to Architect. */
  createOrder: Scalars['OrderId']['output'];
  /** Send multiple orders to Architect. */
  createOrders: Array<Scalars['OrderId']['output']>;
  /** Create a new POV algo order. */
  createPovAlgo: Scalars['OrderId']['output'];
  /** Create a new SOR algo order. */
  createSmartOrderRouterAlgo: Scalars['OrderId']['output'];
  /** Create a new Spread algo order. */
  createSpreadAlgo: Scalars['OrderId']['output'];
  /** Create a new API key for Telegram */
  createTelegramApiKey: ApiKey;
  /** Create a new TWAP algo order. */
  createTwapAlgo: Scalars['OrderId']['output'];
  /** Preview the execution of an SOR algo. */
  previewSmartOrderRouterAlgo?: Maybe<AlgoPreview>;
  /** Remove an API key */
  removeApiKey: Scalars['Boolean']['output'];
  /** Remove all Telegram API keys */
  removeTelegramApiKeys: Scalars['Boolean']['output'];
  sendAlgoControlCommand: Scalars['OrderId']['output'];
  /** Set credentials for a given component id. */
  setCredentials: Scalars['Boolean']['output'];
  /** Set/unset market favorited by current user. */
  updateMarket?: Maybe<Market>;
};

export type MutationRootCancelAllOrdersArgs = {
  venueId?: InputMaybe<Scalars['VenueId']['input']>;
};

export type MutationRootCancelOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type MutationRootCancelOrdersArgs = {
  orderIds: Array<Scalars['OrderId']['input']>;
};

export type MutationRootCreateMmAlgoArgs = {
  mmAlgo: CreateMmAlgo;
};

export type MutationRootCreateOrderArgs = {
  order: CreateOrder;
};

export type MutationRootCreateOrdersArgs = {
  orders: Array<CreateOrder>;
};

export type MutationRootCreatePovAlgoArgs = {
  povAlgo: CreatePovAlgo;
};

export type MutationRootCreateSmartOrderRouterAlgoArgs = {
  algo: CreateSmartOrderRouterAlgo;
};

export type MutationRootCreateSpreadAlgoArgs = {
  spreadAlgo: CreateSpreadAlgo;
};

export type MutationRootCreateTelegramApiKeyArgs = {
  telegramId: Scalars['String']['input'];
};

export type MutationRootCreateTwapAlgoArgs = {
  twapAlgo: CreateTwapAlgo;
};

export type MutationRootPreviewSmartOrderRouterAlgoArgs = {
  algo: CreateSmartOrderRouterAlgo;
};

export type MutationRootRemoveApiKeyArgs = {
  apiKey: Scalars['String']['input'];
};

export type MutationRootSendAlgoControlCommandArgs = {
  command: AlgoControlCommand;
  orderId: Scalars['OrderId']['input'];
};

export type MutationRootSetCredentialsArgs = {
  componentId: Scalars['ComponentId']['input'];
  credentials: Scalars['String']['input'];
};

export type MutationRootUpdateMarketArgs = {
  payload: UpdateMarket;
};

export type OmsOrderUpdate = {
  __typename?: 'OmsOrderUpdate';
  avgFillPrice?: Maybe<Scalars['Decimal']['output']>;
  filledQty: Scalars['Decimal']['output'];
  orderId: Scalars['OrderId']['output'];
  state: Array<OrderStateFlags>;
};

export type OptionsMarketSnapshot = {
  __typename?: 'OptionsMarketSnapshot';
  askIv?: Maybe<Scalars['Decimal']['output']>;
  bidIv?: Maybe<Scalars['Decimal']['output']>;
  delta?: Maybe<Scalars['Decimal']['output']>;
  gamma?: Maybe<Scalars['Decimal']['output']>;
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  openInterest?: Maybe<Scalars['Decimal']['output']>;
  rho?: Maybe<Scalars['Decimal']['output']>;
  theta?: Maybe<Scalars['Decimal']['output']>;
  undPrice?: Maybe<Scalars['Decimal']['output']>;
  underlying?: Maybe<Product>;
  underlyingId: Scalars['ProductId']['output'];
  vega?: Maybe<Scalars['Decimal']['output']>;
};

export type Order = {
  __typename?: 'Order';
  accountId?: Maybe<Scalars['AccountId']['output']>;
  dir: Scalars['Dir']['output'];
  id: Scalars['OrderId']['output'];
  market: Market;
  marketId: Scalars['MarketId']['output'];
  orderType: OrderType;
  quantity: Scalars['Decimal']['output'];
  quoteId?: Maybe<Scalars['Str']['output']>;
  source: OrderSource;
  timeInForce: TimeInForce;
};

export type OrderLog = {
  __typename?: 'OrderLog';
  avgFillPrice?: Maybe<Scalars['Decimal']['output']>;
  filledQty: Scalars['Decimal']['output'];
  order: Order;
  orderState: Array<OrderStateFlags>;
  rejectReason?: Maybe<Scalars['String']['output']>;
  timestamp: Scalars['DateTime']['output'];
};

export enum OrderSource {
  Algo = 'ALGO',
  Api = 'API',
  Cli = 'CLI',
  External = 'EXTERNAL',
  Gui = 'GUI',
  Other = 'OTHER',
  Telegram = 'TELEGRAM',
}

/** The state of an order */
export enum OrderStateFlags {
  Acked = 'ACKED',
  Canceled = 'CANCELED',
  Canceling = 'CANCELING',
  Filled = 'FILLED',
  Open = 'OPEN',
  Out = 'OUT',
  Rejected = 'REJECTED',
  Stale = 'STALE',
}

export type OrderType =
  | LimitOrderType
  | StopLossLimitOrderType
  | TakeProfitLimitOrderType;

export type Orderflow =
  | AberrantFill
  | Ack
  | Cancel
  | CancelAll
  | Fill
  | OmsOrderUpdate
  | Order
  | Out
  | Reject;

export type Out = {
  __typename?: 'Out';
  order?: Maybe<Order>;
  orderId: Scalars['OrderId']['output'];
};

export type PoolMarketKind = {
  __typename?: 'PoolMarketKind';
  products: Array<Product>;
};

export type Position = {
  __typename?: 'Position';
  account?: Maybe<Account>;
  accountId: Scalars['AccountId']['output'];
  averagePrice?: Maybe<Scalars['Decimal']['output']>;
  breakEvenPrice?: Maybe<Scalars['Decimal']['output']>;
  dir: Scalars['Dir']['output'];
  liquidationPrice?: Maybe<Scalars['Decimal']['output']>;
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  quantity?: Maybe<Scalars['Decimal']['output']>;
  tradeDate?: Maybe<Scalars['Date']['output']>;
  tradeTime?: Maybe<Scalars['DateTime']['output']>;
  venue?: Maybe<Venue>;
  venueId: Scalars['VenueId']['output'];
};

export type PovAlgoOrder = {
  __typename?: 'PovAlgoOrder';
  accountId?: Maybe<Scalars['AccountId']['output']>;
  dir: Scalars['Dir']['output'];
  endTime: Scalars['DateTime']['output'];
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  maxQuantity: Scalars['Decimal']['output'];
  minOrderQuantity: Scalars['Decimal']['output'];
  name: Scalars['String']['output'];
  orderId: Scalars['OrderId']['output'];
  takeThroughFrac?: Maybe<Scalars['Decimal']['output']>;
  targetVolumeFrac: Scalars['Decimal']['output'];
};

export type PovAlgoStatus = {
  __typename?: 'PovAlgoStatus';
  creationTime: Scalars['DateTime']['output'];
  fractionComplete?: Maybe<Scalars['Float']['output']>;
  marketVolume: Scalars['Decimal']['output'];
  order?: Maybe<PovAlgoOrder>;
  orderId: Scalars['OrderId']['output'];
  quantityFilled: Scalars['Decimal']['output'];
  realizedVolumeFrac?: Maybe<Scalars['Decimal']['output']>;
  status: AlgoRunningStatus;
};

export type Product = {
  __typename?: 'Product';
  expiration?: Maybe<Scalars['DateTime']['output']>;
  id: Scalars['ProductId']['output'];
  kind: Scalars['String']['output'];
  markUsd?: Maybe<Scalars['Decimal']['output']>;
  multiplier: Scalars['Decimal']['output'];
  name: Scalars['String']['output'];
  optionType?: Maybe<Scalars['String']['output']>;
  strike?: Maybe<Scalars['String']['output']>;
  underlying?: Maybe<Product>;
};

export type QueryRoot = {
  __typename?: 'QueryRoot';
  /** Get all current known balances and positions for all counterparties. */
  accountSummaries: Array<AccountSummaries>;
  /** Get the current known balances and positions for a given counterparty. */
  accountSummariesForCpty: AccountSummaries;
  /**
   * List all known/mapped accounts relevant to the logged-in user.
   *
   * Accounts are generally defined by exchange connectors or their respective exchange configs.
   * Refer to the User Guide for more information on how Architect names and manages accounts.
   */
  accounts: Array<Account>;
  /** Find and return generic algo logs by parent order ID. */
  algoLog?: Maybe<AlgoLog>;
  /** Find a generic algo order and its details by parent order ID. */
  algoOrder?: Maybe<AlgoOrder>;
  /** Find and return generic algo order status by parent order ID. */
  algoStatus: Array<AlgoStatus>;
  bookSnapshot: Book;
  /** Get CME product group info. */
  cmeProductGroupInfos: Array<CmeProductGroupInfo>;
  /** Get token info for a given product. */
  coinInfo?: Maybe<CoinInfo>;
  /** Get a snapshot of token info, sourced from CoinGecko and CoinMarketCap. */
  coinInfos: Array<CoinInfo>;
  cptys: Array<CptyInfo>;
  /** Get all fills for a given venue, route, base, and quote. */
  fills: Fills;
  /** Find markets and their details by some filtering criteria. */
  filterMarkets: Array<Market>;
  /** Query historical OHLCV candles for a given market, candle width, and time range. */
  historicalCandles: Array<CandleV1>;
  /** List the API keys associated with the current user. */
  listApiKeys: Array<ApiKey>;
  /** Find a market and its details by its ID. */
  market?: Maybe<Market>;
  /**
   * Get a snapshot of the marketdata for a given market, at a given time.  If no
   * latest_at_or_before is provided, the most recent snapshot is returned.
   */
  marketSnapshot?: Maybe<MarketSnapshot>;
  /**
   * Find markets and their details by their IDs.  Markets are uniquely identified by their
   * names or IDs; market IDs are fully determined by their string names as UUIDv5.
   */
  markets: Array<Maybe<Market>>;
  /**
   * Get snapshots of all markets for the given time.  If no latest_at_or_before is provided,
   * the most recent snapshots are returned.
   */
  marketsSnapshots: Array<MarketSnapshot>;
  /** Return the current user's authentication information. */
  me: Me;
  /** Find and return MM algo order details by parent order ID. */
  mmAlgoOrder?: Maybe<MmAlgoOrder>;
  /** Find and return MM algo status by parent order ID. */
  mmAlgoStatus: Array<MmAlgoStatus>;
  /** List all open orders known to the OMS. */
  openOrders: Array<OrderLog>;
  /** Get a snapshot of the options data for a given underlying, at a given time. */
  optionsMarketSnapshots: Array<OptionsMarketSnapshot>;
  /** Find order details by order ID from the OMS. */
  order?: Maybe<OrderLog>;
  /** List all recently outed orders known to the OMS. */
  outedOrders: Array<OrderLog>;
  /** Find and return POV order details by parent order ID. */
  povOrder?: Maybe<PovAlgoOrder>;
  /** Find and return POV algo status by parent order ID. */
  povStatus: Array<PovAlgoStatus>;
  /** Find a product and its details by its ID. */
  product?: Maybe<Product>;
  /**
   * Find products and their details by their IDs.  Products are uniquely identified by their
   * names or IDs; product IDs are fully determined by their string names as UUIDv5.
   */
  products: Array<Maybe<Product>>;
  /** Find a route by its ID. */
  route?: Maybe<Route>;
  /**
   * List all known routes in symbology.  Routes are uniquely identified by their names or IDs;
   * route IDs are fully determined by their string names as UUIDv5.
   */
  routes: Array<Route>;
  /** Find and return SOR order details by parent order ID. */
  smartOrderRouterOrder?: Maybe<SmartOrderRouterOrder>;
  /** Find and return SOR algo status by parent order ID. */
  smartOrderRouterStatus: Array<SmartOrderRouterStatus>;
  /** Find and return spread algo status by parent order ID. */
  spreadAlgoOrder?: Maybe<MmAlgoOrder>;
  /** Find and return spread algo status by parent order ID. */
  spreadAlgoStatus: Array<MmAlgoStatus>;
  /**
   * Query TCA balance pnl stats, the account_id is a required field.
   * The following filtering is allowed ..
   * If no venue is provided then all venues will be included
   * If use_purchasing_power is false or not provided then we will use
   *   the balance column in the table. If it's true then we will use
   *   the purchasing power column. This is needed for the rfb environment
   */
  tcaBalancePnl: Array<TcaBalancePnlV1>;
  /**
   * Query TCA balance pnl timeseries, the account_id and venue_id are
   * required fields. If both date ranges are not valid then we will return
   * the timeseries for the last rolling 24 hours. If they are both provided
   * then the timeseries will return hourly data points for the range provided
   * If use_purchasing_power is false or not provided then we will use
   *   the balance column in the table. If it's true then we will use
   *   the purchasing power column. This is needed for the rfb environment
   */
  tcaBalancePnlTimeseries: Array<TcaPnlV1>;
  /** Query TCA pnl / marks stats, id is an optional field but the dates are required */
  tcaMarks: Array<TcaMarksV1>;
  /** Query TCA summary stats, id is an optional field but the dates are required */
  tcaSummary: Array<TcaSummaryV1>;
  /** Find and return TWAP algo order details by parent order ID. */
  twapOrder?: Maybe<TwapOrder>;
  /** Find and return TWAP algo status by parent order ID. */
  twapStatus: Array<TwapStatus>;
  /** Find a venue by its ID. */
  venue?: Maybe<Venue>;
  /**
   * List all known venues in symbology.  Venues are uniquely identified by their names or IDs;
   * venue IDs are fully determined by their string names as UUIDv5.
   */
  venues: Array<Venue>;
  version: Scalars['String']['output'];
};

export type QueryRootAccountSummariesForCptyArgs = {
  route: Scalars['RouteId']['input'];
  venue: Scalars['VenueId']['input'];
};

export type QueryRootAlgoLogArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootAlgoOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootBookSnapshotArgs = {
  delayed?: InputMaybe<Scalars['Boolean']['input']>;
  market: Scalars['MarketId']['input'];
  numLevels: Scalars['Int']['input'];
  precision?: InputMaybe<Scalars['Decimal']['input']>;
  retainSubscriptionForNSeconds?: InputMaybe<Scalars['Int']['input']>;
};

export type QueryRootCoinInfoArgs = {
  product: Scalars['ProductId']['input'];
};

export type QueryRootFillsArgs = {
  base?: InputMaybe<Scalars['ProductId']['input']>;
  quote?: InputMaybe<Scalars['ProductId']['input']>;
  route?: InputMaybe<Scalars['RouteId']['input']>;
  venue?: InputMaybe<Scalars['VenueId']['input']>;
};

export type QueryRootFilterMarketsArgs = {
  filter: MarketFilter;
};

export type QueryRootHistoricalCandlesArgs = {
  end: Scalars['DateTime']['input'];
  id: Scalars['MarketId']['input'];
  start: Scalars['DateTime']['input'];
  width: CandleWidth;
};

export type QueryRootMarketArgs = {
  id: Scalars['MarketId']['input'];
};

export type QueryRootMarketSnapshotArgs = {
  latestAtOrBefore?: InputMaybe<Scalars['DateTime']['input']>;
  market: Scalars['MarketId']['input'];
};

export type QueryRootMarketsArgs = {
  id: Array<Scalars['MarketId']['input']>;
};

export type QueryRootMarketsSnapshotsArgs = {
  latestAtOrBefore?: InputMaybe<Scalars['DateTime']['input']>;
};

export type QueryRootMmAlgoOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootMmAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootOptionsMarketSnapshotsArgs = {
  latestAtOrBefore?: InputMaybe<Scalars['DateTime']['input']>;
  underlying: Scalars['ProductId']['input'];
};

export type QueryRootOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootOutedOrdersArgs = {
  fromInclusive?: InputMaybe<Scalars['DateTime']['input']>;
  toExclusive?: InputMaybe<Scalars['DateTime']['input']>;
};

export type QueryRootPovOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootPovStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootProductArgs = {
  id: Scalars['ProductId']['input'];
};

export type QueryRootProductsArgs = {
  id: Array<Scalars['ProductId']['input']>;
};

export type QueryRootRouteArgs = {
  id: Scalars['RouteId']['input'];
};

export type QueryRootSmartOrderRouterOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootSmartOrderRouterStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootSpreadAlgoOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootSpreadAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootTcaBalancePnlArgs = {
  accountId: Scalars['AccountId']['input'];
  usePurchasingPower?: InputMaybe<Scalars['Boolean']['input']>;
  venueId?: InputMaybe<Scalars['VenueId']['input']>;
};

export type QueryRootTcaBalancePnlTimeseriesArgs = {
  accountId: Scalars['AccountId']['input'];
  fromInclusive?: InputMaybe<Scalars['DateTime']['input']>;
  toExclusive?: InputMaybe<Scalars['DateTime']['input']>;
  usePurchasingPower?: InputMaybe<Scalars['Boolean']['input']>;
  venueId: Scalars['VenueId']['input'];
};

export type QueryRootTcaMarksArgs = {
  fromInclusive: Scalars['DateTime']['input'];
  id?: InputMaybe<Scalars['MarketId']['input']>;
  toExclusive: Scalars['DateTime']['input'];
};

export type QueryRootTcaSummaryArgs = {
  currency?: InputMaybe<Scalars['String']['input']>;
  fromInclusive: Scalars['DateTime']['input'];
  id?: InputMaybe<Scalars['MarketId']['input']>;
  toExclusive: Scalars['DateTime']['input'];
};

export type QueryRootTwapOrderArgs = {
  orderId: Scalars['OrderId']['input'];
};

export type QueryRootTwapStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
};

export type QueryRootVenueArgs = {
  id: Scalars['VenueId']['input'];
};

export enum Reason {
  AlgoPaused = 'ALGO_PAUSED',
  AlgoStopped = 'ALGO_STOPPED',
  CancelPending = 'CANCEL_PENDING',
  MaxPosition = 'MAX_POSITION',
  MinPosition = 'MIN_POSITION',
  NoAsk = 'NO_ASK',
  NoBid = 'NO_BID',
  NoReferencePrice = 'NO_REFERENCE_PRICE',
  NoReferenceSize = 'NO_REFERENCE_SIZE',
  OpenOrderOutsideTolerance = 'OPEN_ORDER_OUTSIDE_TOLERANCE',
  OpenOrderWithinTolerance = 'OPEN_ORDER_WITHIN_TOLERANCE',
  WithinFillLockout = 'WITHIN_FILL_LOCKOUT',
  WithinOrderLockout = 'WITHIN_ORDER_LOCKOUT',
  WithinRejectLockout = 'WITHIN_REJECT_LOCKOUT',
}

export enum ReferencePrice {
  BidAsk = 'BID_ASK',
  HedgeMarketBidAsk = 'HEDGE_MARKET_BID_ASK',
  Mid = 'MID',
}

export type Reject = {
  __typename?: 'Reject';
  order?: Maybe<Order>;
  orderId: Scalars['OrderId']['output'];
  reason: Scalars['String']['output'];
};

export type RfqResponse = {
  __typename?: 'RfqResponse';
  buy?: Maybe<RfqResponseSide>;
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  sell?: Maybe<RfqResponseSide>;
};

export type RfqResponseSide = {
  __typename?: 'RfqResponseSide';
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Decimal']['output'];
  quoteId?: Maybe<Scalars['String']['output']>;
};

export type Route = {
  __typename?: 'Route';
  id: Scalars['RouteId']['output'];
  name: Scalars['Str']['output'];
};

export type SmartOrderRouterOrder = {
  __typename?: 'SmartOrderRouterOrder';
  base: Product;
  dir: Scalars['Dir']['output'];
  executionTimeLimitMs: Scalars['Int']['output'];
  limitPrice: Scalars['Decimal']['output'];
  markets: Array<Market>;
  orderId: Scalars['OrderId']['output'];
  parentOrderId?: Maybe<Scalars['OrderId']['output']>;
  quote: Product;
  targetSize: Scalars['Decimal']['output'];
};

export type SmartOrderRouterStatus = {
  __typename?: 'SmartOrderRouterStatus';
  order?: Maybe<SmartOrderRouterOrder>;
  status: AlgoStatus;
};

export type StopLossLimitOrderType = {
  __typename?: 'StopLossLimitOrderType';
  limitPrice: Scalars['Decimal']['output'];
  triggerPrice: Scalars['Decimal']['output'];
};

export type SubscriptionRoot = {
  __typename?: 'SubscriptionRoot';
  /** Subscribe to the orderbook feed of a market. */
  book: Book;
  /** Subscribe to the candle feed of a market. */
  candles: CandleV1;
  /** Subscribe to exchange-specific data from markets.  This is a multiplexed stream. */
  exchangeSpecific: Array<ExchangeSpecificUpdate>;
  /** Subscribe to all fills */
  fills: Fill;
  /** Subscribe to all orderflow. */
  orderflow: Orderflow;
  pollAccountSummaries: Array<AccountSummaries>;
  pollAlgoStatus: Array<AlgoStatus>;
  pollFills: Fills;
  pollMmAlgoStatus: Array<MmAlgoStatus>;
  pollOpenOrders: Array<OrderLog>;
  pollSorAlgoStatus: Array<SmartOrderRouterStatus>;
  pollSpreadAlgoStatus: Array<MmAlgoStatus>;
  pollTwapAlgoStatus: Array<TwapStatus>;
  /** Subscribe to an RFQ feed. */
  rfqs: Array<RfqResponse>;
  /** Subscribe to the trade feed of a market. */
  trades: TradeV1;
};

export type SubscriptionRootBookArgs = {
  delayed?: InputMaybe<Scalars['Boolean']['input']>;
  market: Scalars['MarketId']['input'];
  precision?: InputMaybe<Scalars['Decimal']['input']>;
};

export type SubscriptionRootCandlesArgs = {
  candleWidth: CandleWidth;
  delayed?: InputMaybe<Scalars['Boolean']['input']>;
  finalized?: InputMaybe<Scalars['Boolean']['input']>;
  market: Scalars['MarketId']['input'];
};

export type SubscriptionRootExchangeSpecificArgs = {
  delayed?: InputMaybe<Scalars['Boolean']['input']>;
  fields: Array<Scalars['String']['input']>;
  markets: Array<Scalars['MarketId']['input']>;
};

export type SubscriptionRootPollAccountSummariesArgs = {
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollFillsArgs = {
  base?: InputMaybe<Scalars['ProductId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
  quote?: InputMaybe<Scalars['ProductId']['input']>;
  route?: InputMaybe<Scalars['RouteId']['input']>;
  venue?: InputMaybe<Scalars['VenueId']['input']>;
};

export type SubscriptionRootPollMmAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollOpenOrdersArgs = {
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollSorAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollSpreadAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootPollTwapAlgoStatusArgs = {
  orderId?: InputMaybe<Scalars['OrderId']['input']>;
  pollIntervalMs: Scalars['Int']['input'];
};

export type SubscriptionRootRfqsArgs = {
  base: Scalars['ProductId']['input'];
  quantity: Scalars['Decimal']['input'];
  quote: Scalars['ProductId']['input'];
  venues: Array<Scalars['VenueId']['input']>;
};

export type SubscriptionRootTradesArgs = {
  delayed?: InputMaybe<Scalars['Boolean']['input']>;
  market: Scalars['MarketId']['input'];
};

export type TakeProfitLimitOrderType = {
  __typename?: 'TakeProfitLimitOrderType';
  limitPrice: Scalars['Decimal']['output'];
  triggerPrice: Scalars['Decimal']['output'];
};

export type TcaBalancePnlV1 = {
  __typename?: 'TcaBalancePnlV1';
  balanceNow: Scalars['Decimal']['output'];
  balancePast: Scalars['Decimal']['output'];
  pnl: Scalars['Decimal']['output'];
  tsNow: Scalars['DateTime']['output'];
  tsPast: Scalars['DateTime']['output'];
  venue: Scalars['String']['output'];
  venueId: Scalars['VenueId']['output'];
};

export type TcaData = {
  __typename?: 'TcaData';
  markPrice: Scalars['Decimal']['output'];
  tcaType: Scalars['String']['output'];
  tcaValue: Scalars['Decimal']['output'];
};

export type TcaMarksV1 = {
  __typename?: 'TcaMarksV1';
  dir: Scalars['Dir']['output'];
  feeCurrency?: Maybe<Scalars['String']['output']>;
  fees?: Maybe<Scalars['Decimal']['output']>;
  fillId: Scalars['FillId']['output'];
  market: Scalars['String']['output'];
  marketId: Scalars['MarketId']['output'];
  multiplier: Scalars['Decimal']['output'];
  orderId?: Maybe<Scalars['OrderId']['output']>;
  price: Scalars['Decimal']['output'];
  quantity: Scalars['Decimal']['output'];
  source?: Maybe<Scalars['String']['output']>;
  tcaValues: Array<TcaData>;
  tradeTime: Scalars['DateTime']['output'];
};

export type TcaPnlV1 = {
  __typename?: 'TcaPnlV1';
  pnl: Scalars['Decimal']['output'];
  ts: Scalars['DateTime']['output'];
};

export type TcaSummaryV1 = {
  __typename?: 'TcaSummaryV1';
  buyNotionalTraded: Scalars['Decimal']['output'];
  fees: Scalars['Decimal']['output'];
  label: Scalars['String']['output'];
  numberOfFills: Scalars['Int']['output'];
  pnlBps: Scalars['Decimal']['output'];
  pnlPriceCurrency: Scalars['Decimal']['output'];
  sellNotionalTraded: Scalars['Decimal']['output'];
  totalNotionalTraded: Scalars['Decimal']['output'];
};

export type TimeInForce = {
  __typename?: 'TimeInForce';
  goodTilDate?: Maybe<Scalars['DateTime']['output']>;
  instruction: Scalars['String']['output'];
};

export type TradeV1 = {
  __typename?: 'TradeV1';
  direction?: Maybe<Scalars['Dir']['output']>;
  price: Scalars['Decimal']['output'];
  size: Scalars['Decimal']['output'];
  time?: Maybe<Scalars['DateTime']['output']>;
};

export type TwapOrder = {
  __typename?: 'TwapOrder';
  accountId?: Maybe<Scalars['AccountId']['output']>;
  dir: Scalars['Dir']['output'];
  endTime: Scalars['DateTime']['output'];
  intervalMs: Scalars['Int']['output'];
  market?: Maybe<Market>;
  marketId: Scalars['MarketId']['output'];
  name: Scalars['String']['output'];
  orderId: Scalars['OrderId']['output'];
  quantity: Scalars['Decimal']['output'];
  rejectLockoutMs: Scalars['Int']['output'];
  takeThroughFrac?: Maybe<Scalars['Decimal']['output']>;
};

export type TwapStatus = {
  __typename?: 'TwapStatus';
  creationTime: Scalars['DateTime']['output'];
  fractionComplete?: Maybe<Scalars['Float']['output']>;
  order?: Maybe<TwapOrder>;
  orderId: Scalars['OrderId']['output'];
  quantityFilled: Scalars['Decimal']['output'];
  realizedTwap?: Maybe<Scalars['Decimal']['output']>;
  status: AlgoRunningStatus;
};

export type UnknownMarketKind = {
  __typename?: 'UnknownMarketKind';
  unused: Scalars['Boolean']['output'];
};

export type UpdateMarket = {
  isFavorite: Scalars['Boolean']['input'];
  marketId: Scalars['MarketId']['input'];
};

export type Venue = {
  __typename?: 'Venue';
  id: Scalars['VenueId']['output'];
  name: Scalars['Str']['output'];
};

export class TypedDocumentString<TResult, TVariables>
  extends String
  implements DocumentTypeDecoration<TResult, TVariables>
{
  __apiType?: DocumentTypeDecoration<TResult, TVariables>['__apiType'];

  constructor(
    private value: string,
    public __meta__?: Record<string, any>,
  ) {
    super(value);
  }

  toString(): string & DocumentTypeDecoration<TResult, TVariables> {
    return this.value;
  }
}
