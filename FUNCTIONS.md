# Initialization

connect: The main way to create an AsyncClient object.
__init__: Users should not be using this constructor directly, unless they do not want to use any subscription methods.

# Symbology

search_symbols: Search for symbols in the Architect database.
get_product_info: Get the product information (product_type, underlying, multiplier, etc.) for a symbol.
get_product_infos: Get the product information (product_type, underlying, multiplier, etc.) for a list of symbols.
get_execution_info: Get the execution information (tick_size, step_size, margin, etc.) for a symbol.
get_execution_infos: Get the execution information (tick_size, step_size, etc.) for a list of symbols.
get_cme_first_notice_date: Get the first notice date for a CME future.
get_future_series: Get the series of futures for a given series symbol.
get_expiration_from_CME_name: Get the expiration date from a CME future name.
get_cme_futures_series: Get the futures in a series from the CME.
get_cme_future_from_root_month_year: Get the symbol for a CME future from the root, month, and year.

# Account Management

who_am_i: Gets the user_id and user_email for the user that the API key belongs to.
list_accounts: List accounts for the user that the API key belongs to.
get_account_summary: Gets the account summary for the given account.
get_account_summaries: Gets the account summaries for the given accounts and trader.
get_account_history: Gets the account history for the given account and dates.

# Order Management

get_open_orders: Returns a list of open orders for the user that match the filters.
get_all_open_orders: Returns a list of all open orders for the user.
get_historical_orders: Gets the historical orders that match the filters.
get_order: Returns the OrderFields object for the specified order.
get_orders: Returns a list of OrderFields objects for the specified orders.
get_fills: Returns a list of fills for the given filters.

# Market Data

get_market_status: Returns market status for symbol (ie if it is quoting and trading).
get_market_snapshot: This is an alias for l1_book_snapshot.
get_market_snapshots: This is an alias for l1_book_snapshot.
get_historical_candles: Gets the historical candles for a symbol.
get_l1_book_snapshot: Gets the L1 book snapshot for a symbol.
get_l1_book_snapshots: Gets the L1 book snapshots for a list of symbols.
get_l2_book_snapshot: Gets the L2 book snapshot for a symbol.
subscribe_l1_book_stream: Subscribe to the stream of L1BookSnapshots for a symbol.
subscribe_l2_book_stream: Subscribe to the stream of L2BookUpdates for a symbol.
subscribe_l1_book: Returns a L1BookSnapshot object that is constantly updating in the background.
subscribe_l2_book: Returns a L2BookSnapshot object that is constantly updating in the background.
subscribe_trades_stream: Subscribe to a stream of trades for a symbol
subscribe_candles_stream: Subscribe to a stream of candles for a symbol

# Order Entry and Cancellation

send_limit_order: Sends a regular limit order.
send_market_pro_order: Sends a market-order like limit price based on the BBO.
cancel_order: Cancels an order by order id.
cancel_all_orders: Cancels all open orders.

