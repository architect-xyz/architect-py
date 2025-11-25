# 5.9.6
- Various algo improvements
- PlaceOrderRequest/Order now has a `tag` field so that users can put in arbitrary tags

# 5.9.5
- reconcile_out, manually reconciles out an order
- Improve spreader order
- Add better spreader + One-triggers-other order
- Add more algo functions and improve algo functionality: 
  - get_algo_order_status
  - resume_algo_order
  - pause_algo_order
  - stop_algo_order
  - modify_algo_order
  - get_historical_algo_orders


# 5.9.4
- Remove Bracket from OrderType, changed it to algo
- Added Spreader algo order

# 5.9.3
- tickers_to_dataframe no longer errors on empty df

# 5.9.2
- client connect now raises error if it does not successfully get a jwt
- equities candles now works

# 5.9.1
- fixed get_options_contract

# 5.9.0
(skipped version)
- improvements to options work
- add the open_paper_accounts/delete_paper_accounts/refresh_paper_account

# 5.7.0 
- add on_batch_cancel_orders to AsyncCpty

# 5.6.0
- simplified / improved TickRoundMethod
- added options methods along with an options category for the client

# 5.5.0
- batch cancels and other OMS enhancements

# 5.4.1
- improved search_symbols with more args (include_expired, order_alphabetically)
- add options section to client

# 5.4.0

- Add marketdata server functionality to external cpty

# 5.3.1

- Add native cancel-all support to cancel_all_orders(); default behavior (synthetic cancel-all) remains unchanged

# 5.3.0

- Add on_cancel_all_orders callback to AsyncCpty

# 5.2.0

- New external cpty interface AsyncCpty, makes building custom connectors easier

# 5.1.5

- Add get_tickers to AsyncClient
- Add get_positions to AsyncClient

# 5.1.4

- Add grpc_options to AsyncClient and Client constructors to allow customization of gRPC channels
- Deprecated place_limit_order in favor of place_order. Dir is now required.
- Added algo types and create_algo_order 
- Added easy interface for accessing orderflow bi-directional stream, use client.orderflow() / OrderflowChannel to access
- Added bracket and market orders to OrderType
- Paper trading should be active very soon for all order types except Bracket
- Add as_user and as_role to AsyncClient and Client constructors
- Add auth_info endpoint
- Various small type fixes
- Add send_initial_snapshots to stream_l1_book_snapshots

# 5.1.3
- Fix stream_orderflow endpoint
- Add cpty_status endpoint

# 5.1.2
- Paper trading mode now CORRECTLY sets the port automatically
- Fixed get_front_future
- Place_orders is a new low level function oto place multiple orders in a single function


# 5.1.1
This patch contains only fixes:
- Paper trading mode now sets the port automatically
- Fixed sys.excepthook when a script closes via the Client.close() function. This is cosmetic though and is for reducing log lines.
- Fix serializing TradableProduct vs str

# 5.1.0
- Added a type-checker-friendly way to get enum-like constants + a payload-carrying variant (GTD) in one class for TimeInForce
- Fixed client_interface to use mypy stubgen and use a pyi file instead of a protocol
- Remove no_pandas
- TickersRequest, added titles for the fields
- Removed unused graphql queries and types
- TradableProduct improvement and comment fixes
- Add `get_front_future` method to async client
- Fixed import story, you don't need to do `from architect_py.grpc.models.AccountsRequest import AccountsRequest`, you can just do `from architect_py.grpc

# 5.0.0

- Refactor AsyncClient to be more gRPC-centric, leveraging new dynamic marketdata endpoint discovery
- As a consequence, many marketdata methods require a `venue` argument
- Some methods renamed:
  - Send_limit_order -> place_limit_order
- Moved some directories around, esp auto-generated files
- Added justfile and switched to ruff for linting and formatting
- Switched to pyright for typechecking
- In AsyncClient, replaced functions in Account Management, Order Management, and Order Entry with their grpc counterparts
- Moved around some of the subscription stream types (e.g. orderflow) from the grpc_client to the AsyncClient 

Migration from v3.2.2:

- In `cancel_order`, return field `recv_time` is no longer a `datetime`; instead, `recv_time` and `recv_time_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return field `status` is now an integer enum instead of a string enum.
- In `list_accounts`, returned field `account.id` is now a string in UUID format instead of a `uuid.UUID`.
- In `get_account_summary`, `get_account_summaries` and `get_account_history`, return field `account` is now a string in UUID format instead of a `uuid.UUID`. Return field `balances` is now a `dict[str, Decimal]` instead of a list. Return field `positions` is now a `dict[str, list[AccountPosition]]` instead of a list.
- In `send_limit_order`, `place_limit_order`, `get_order`, `get_orders`, `get_open_orders` and `get_historical_orders`; returned field `recv_time` is no longer a `datetime`; instead, `recv_time` and `recv_time_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return field `status` is now an integer enum instead of a string enum. Return field `account` is now a string in UUID format instead of a `uuid.UUID`. Return field `time_in_force`, in addition to being a string enum, can now be a `GoodTilDate` as well. Return field `good_til_date` is removed; see `time_in_force`. Return field `order_source` is now an integer enum instead of a string enum.
- In `place_limit_order`, `odir` is now deprecated, use `dir` instead.
- In `get_market_snapshot`, `get_market_snapshots`, `get_l1_book_snapshot`, and `get_l1_book_snapshots`; returned field `timestamp` is no longer a `datetime`; instead, `timestamp` and `timestamp_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return fields `bid_price`, `bid_size`, `ask_price`, and `ask_size` are now `best_bid` and `best_ask` respectively, of type `list[Decimal]` whose elements are `[price, size]`. Return fields `last_price`, `last_size` have been removed.
- In `get_l2_book_snapshot`, return field `timestamp` is no longer a `datetime`; instead, `timestamp` and `timestamp_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return field `bids` and `asks` are now lists of `[price, size]`.
- In `get_historical_candles`, parameter `venue` is now required. It's return type is now a `list[Candle]` directly instead of an object containing a `candles` field.
- In `get_fills`, return field `recv_time` is no longer a `datetime`; instead, `recv_time` and `recv_time_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return field `trade_time` is no longer a `datetime`; instead, `trade_time` and `trade_time_ns` are integers representing epoch seconds, and nanoseconds part respectively. Return fields `fill_id`, `account` are now strings in UUID format instead of `uuid.UUID`s. Return field `fill_kind` is now an integer enum instead of a string enum.
- Renamed `subscribe_l1_book_stream`, use `stream_l1_book_snapshots` instead.
- Renamed `subscribe_l2_book_stream`, use `stream_l2_book_snapshots` instead.
- `subscribe_l1_book` only takes a single symbols and venue now; to subscribe to multiple symbols, call `subscribe_l1_book` multiple times.
- In `subscribe_l1_book` and `subscribe_l2_book`, `venue` is now required.
- Renamed `subscribe_trades_stream`, use `stream_trades` instead.
- Renamed `subscribe_candles_stream`, use `stream_candles` instead.

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
