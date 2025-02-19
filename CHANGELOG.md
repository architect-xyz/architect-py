3.1.7
Features:
  - added historical_candles_snapshot
  - ExecutionInfo now has `initialMargin` and `maintenanceMargin`

Fixes:
  - small type changes on return types and function args
  - added back candle_snapshot

3.1.6
Features:
  - added explicit paper trading mode arg for client
  - composes graphql client instead of inheriting
  - added working TradableProduct scalar

Fixes:
  - fix the l2 snapshot function
  - get_order now works
  - fixed paper trading port

3.1.5
Fixes:
  - fix get_historical_orders
  - fix the sync client import

3.1.4
Features:
  - added get_order and get_orders


3.1.3
Fixes:
  - Fix send_market_pro_order

3.1.2 / 3.1.1
Features:
  - added marketStatus


Fixes:
  - fixed search_symbol
  - added rejectMessage attribute to Order



3.0.0

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
