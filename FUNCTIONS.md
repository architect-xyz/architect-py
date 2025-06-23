### 🚀 Initialization and configuration

- **`connect`**: Connect to an Architect installation.
- **`close`**: Close the gRPC channel and GraphQL client.
- **`refresh_jwt`**: Refresh the JWT for the gRPC channel if it's nearing expiration (within 1 minute).
- **`set_jwt`**: Manually set the JWT for gRPC authentication.
- **`discover_marketdata`**: Load marketdata endpoints from the server config.
- **`set_marketdata`**: Manually set the marketdata endpoint for a venue.
- **`marketdata`**: Get the marketdata client for a venue.
- **`set_hmart`**: Manually set the hmart (historical marketdata service) endpoint.
- **`hmart`**: Get the hmart (historical marketdata service) client.
- **`core`**: Get the core client.
- **`who_am_i`**: Gets the user_id and user_email for the user that the API key belongs to.
- **`auth_info`**
- **`cpty_status`**: Get cpty status.

---

### 🔍 Symbology

- **`list_symbols`**: List all symbols.
- **`search_symbols`**: Search for tradable products on Architect.
- **`get_product_info`**: Get information about a product, e.g. product_type, underlying, multiplier.
- **`get_product_infos`**: Get information about products, e.g. product_type, underlying, multiplier.
- **`get_execution_info`**: Get information about tradable product execution, e.g. tick_size,
- **`get_execution_infos`**: Get information about tradable product execution, e.g. tick_size,
- **`get_futures_series`**: List all futures in a given series.
- **`get_front_future`**: Gets the front future.
- **`get_cme_future_from_root_month_year`**: Get the symbol for a CME future from the root, month, and year.

---

### 🧮 Marketdata

- **`get_market_status`**: Returns market status for symbol (e.g. if it's currently quoting or trading).
- **`get_historical_candles`**: Gets historical candles for a symbol.
- **`get_l1_book_snapshot`**: Gets the L1 book snapshot for a symbol.
- **`get_l1_book_snapshots`**: Gets the L1 book snapshots for a list of symbols.
- **`get_l2_book_snapshot`**: Gets the L2 book snapshot for a symbol.
- **`get_ticker`**: Gets the ticker for a symbol.
- **`get_tickers`**
- **`stream_l1_book_snapshots`**: Subscribe to the stream of L1BookSnapshots for a symbol.
- **`stream_l2_book_updates`**: Subscribe to the stream of L2BookUpdates for a symbol.
- **`subscribe_l1_book`**: Subscribe to the L1 stream for a symbol in the background.
- **`unsubscribe_l1_book`**: Unsubscribe from the L1 stream for a symbol, ie undoes subscribe_l1_book.
- **`subscribe_l2_book`**: Subscribe to the L2 stream for a symbol in the background.
- **`stream_trades`**: Subscribe to a stream of trades for a symbol.
- **`stream_candles`**: Subscribe to a stream of candles for a symbol.

---

### 💹 Portfolio management

- **`list_accounts`**: List accounts for the user that the API key belongs to.
- **`get_account_summary`**: Get account summary, including balances, positions, pnls, etc.
- **`get_account_summaries`**: Get account summaries for accounts matching the filters.
- **`get_account_history`**: Get historical sequence of account summaries for the given account.

---

### 📝 Order management

- **`get_open_orders`**: Returns a list of open orders for the user that match the filters.
- **`get_historical_orders`**: Returns a list of all historical orders that match the filters.
- **`get_order`**: Returns the specified order.  Useful for looking at past sent orders.
- **`get_orders`**: Returns the specified orders.  Useful for looking at past sent orders.
- **`get_fills`**: Returns all fills matching the given filters.
- **`orderflow`**: A two-way channel for both order entry and listening to order updates (fills, acks, outs, etc.).
- **`stream_orderflow`**: A stream for listening to order updates (fills, acks, outs, etc.).

---

### 📣 Order entry

- **`place_orders`**: A low level function to place multiple orders in a single function.
- **`place_order`**: Sends a regular order.
- **`send_market_pro_order`**: Sends a market-order like limit price based on the BBO.
- **`cancel_order`**: Cancels an order by order id.
- **`cancel_all_orders`**: Cancels all open orders.
- **`create_algo_order`**: Sends an advanced algo order such as the spreader.

---

