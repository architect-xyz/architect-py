# 3.3.0
Breaking:
  - in AsyncClient, replaced functions in Account Management, Order Management, and Order Entry with their grpc counterparts
    - no functionality change, just changes to input types and output types
  - Moved around some of the subscription stream types (e.g. orderflow) from the grpc_client to the AsyncClient

# 3.2.2
Fixes:
  - removed lru_cache on execution_info
  - Fixed sync client not having grpc functions
  - Set order_id in send_order functions
  - Added External cpty protocol example
  - Fixed MinOrderQuantityUnit type
  - Fix some Enum grpc types that were incorrect
  - Updated examples and fixed test
  - added UnannotatedRequest types for Union Request types

# 3.2.1
Improvements:
  - removed pytz as a requirement, replaced with built in ZoneInfo for py3.9+
  - small type updates
  - grpc_definitions.TimeInForce1 -> grpc_definitions.TimeInForceEnum
  - Revamped grpc_client.request and grpc_client.subscribe to not include the ParamSpec
  - Added caching to get_product_info, get_execution_info
  - Loosened requirements for real this time - websockets requirement more flexible

# 3.2.0
Breaking:
  - Changed the way AsyncClient is instantiated, from normal __init__ to 
    - Can just change AsyncClient(args) -> AsyncClient.connect(args)
    - the port argument was removed, please remove it as an arg
  - changed the values of OrderDir to match Rust type
    class OrderDir(str, Enum):
      BUY = "buy"
      SELL = "sell"

    class OrderDir(str, Enum):
      BUY = "BUY"
      SELL = "SELL"


Features
  - Added get_account_history query
  - Added get_execution_infos (plural) query
  - Added gRPC client + subscription functions to AsynClient
  - Added docs for each function
  - OrderDir is now also a string

# 3.1.11
Features:
  - Added the who_am_i function to get userid + email

Fixes:
  - Fixed account summaries for paper trading (there is a corresponding backend PR)
  - Improved documentation


# 3.1.10
Fixes:
  - Fix part 2 for send_market_pro_order, prematurely updated the schema

# 3.1.9
Fixes:
  - Fix for send_market_pro_order
  - Minor internal renaming of functions
  - updated dependencies + poetry lock

# 3.1.8
Fixes:
  - Minor function fixes

# 3.1.7
Features:
  - added historical_candles_snapshot
  - ExecutionInfo now has `initialMargin` and `maintenanceMargin`

Fixes:
  - small type changes on return types and function args
  - added back candle_snapshot

# 3.1.6
Features:
  - added explicit paper trading mode arg for client
  - composes graphql client instead of inheriting
  - added working TradableProduct scalar

Fixes:
  - fix the l2 snapshot function
  - get_order now works
  - fixed paper trading port

# 3.1.5
Fixes:
  - fix get_historical_orders
  - fix the sync client import

# 3.1.4
Features:
  - added get_order and get_orders


# 3.1.3
Fixes:
  - Fix send_market_pro_order

# 3.1.2 / 3.1.1
Features:
  - added marketStatus


Fixes:
  - fixed search_symbol
  - added rejectMessage attribute to Order



# 3.0.0

Breaking Changes:
- Removed GetFilteredMarkets query, replaced by SearchMarkets
- Removed GetBalancesForCpty query, replace by GetAccountSummaries
- CreateOrder was replaced by PlaceOrder, most people should use send_limit_order anyway
- Removed SendOrders and CancelOrders for now (note the plural)
- moved utils.dt.convert_datetime_to_utc_str to scalars.
- Most scalars were changed as they were changed in the backend
- Temporarily removed ability to send algos via python API
- Removed get_accounts in favor of just using accountSummaries with no account field (returns all AccountSummaries)
- Changed args of get_book_snapshot
- removed SubscribeExchangeSpecific
- getOutedOrders replaced with GetHistoricalOrders
- removed GetAllMarketSnapshots, replaced with GetMarketSnapshots
- removed SearchMarket, replaced with SearchSymbols
- removed get_balance_anmd_position in favor of client.get_account_summaries
- subscribe_book replaced with watch_L2_book
- getBookSnapshot replaced with L2BookSnapshot

Features:

Fixes:

Improvement:
- removed _version.py and just put __version__ in __init__.py


Todo:
- test subscriptions
- algos need to work again

- test Date scalar in firstNoticeDate in the ProductInfo type

- re-add getmargin
query GetMargin($id: MarketId!) {
  market(id: $id) {
    initialMargin
    maintenanceMargin
  }
}
- need this
mutation RemoveTelegramApiKeys {
  removeTelegramApiKeys
}
