3.0.0

Breaking Changes:
- Removed GetFilteredMarkets query in favor of SearchMarkets
- Removed GetBalancesForCpty query in favor of GetAccountSummariesForCpty
- CreateOrder was replaced by PlaceOrder
- Removed SendOrders and CancelOrders (for now...)
- moved utils.dt.convert_datetime_to_utc_str to scalars.convert_datetime_to_utc_str 
- Most scalars were changed as they were changed in the backend
- Temporarily removed ability to send algos via python API
- Removed get_accounts in favor of just using accountSummaries with no account field (returns all AccountSummaries)
- Changed args of get_book_snapshot
- removed SubscribeExchangeSpecific
- getOutedOrders replaced with GetHistoricalOrders
- removed GetAllMarketSnapshots, replaced with GetMarketSnapshots
- removed SearchSymbols, replaced with SearchSymbols
- algos currently not working

Features:

Fixes:

Improvement:
- removed _version.py and just put __version__ in __init__.py



Todo:
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
- need these subscriptions back
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
    timestamp
  }
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