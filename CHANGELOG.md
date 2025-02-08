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
- removed SearchSymbols, replaced with SearchSymbols
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

query GetOrder($orderId: OrderId!) {
  order(orderId: $orderId) {
    ...OrderLogFields
  }
}