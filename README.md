# architect_py
[![PyPI version](https://img.shields.io/pypi/v/architect-py.svg)](https://pypi.org/project/architect-py/)

A Python API for [Architect](https://architect.co).

Just some of the features of this API:
symbology, market snapshots, past trades, account queries, order management (including sending advanced algos!), and market feed subscriptions.

This repo heavily uses type hinting, so using a type checker such as Pylance or mypy is suggestible to reduce potential for error.


## Example usage

`AsyncClient` and `Client` are the entryways into making calls to the Architect backend.
Note that the sync `Client` does not have access to any subscription functions, because they are async by nature.


```python
import asyncio

from architect_py.async_client import AsyncClient
from architect_py.scalars import TradableProduct

async def main():
    c = await AsyncClient.connect(
        host="<your installation domain>",  # e.g. app.architect.co for the brokerage
        api_key="<api key>",
        api_secret="<api secret>"
        paper_trading=True,
    )
    print(await c.who_am_i())

    series = await async_client.get_cme_futures_series("ES CME Futures")
    front_ES_future = series[0][1]

    s = c.subscribe_trades_stream(front_ES_future)
    async for trade in s:
        print(trade)

asyncio.run(main())
```

```python
from architect_py.client import Client

def main():
    c = Client(
        host="<your installation domain>",
        api_key="<api key>",
        api_secret="<api secret>"
        paper_trading=True,
    )
    print(c.who_am_i())

    print(client.get_account_summaries())

    print(client.search_symbols("ES"))
```

While the AsyncClient is the recommended way to use the Architect API, the Client instead without any familiarity with `async/await`.
The sync clients and async clients usage is identical, except one removes the `await` before the call. The only exception to this is that the sync client does not support any subscriptions, because they are inherently asynchronous.

Check the `examples` folder or the `architect_py/tests` folders for example usages.


## Function Breakdown


The `async` client has the following functions
```
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
```


### Running examples from this package

Clone this repository to run examples in the `examples` directory. This package
uses poetry for dependency management. To enter a poetry virtual environment, make
sure you have [poetry](https://python-poetry.org/docs/) installed and run the
following from the repository root.

```bash
poetry shell
poetry install --sync

export ARCHITECT_HOST="<your installation domain>"
export ARCHITECT_API_KEY="<api key>"
export ARCHITECT_API_SECRET="<api secret>"

python -m examples.trades
```

You can exit the poetry shell by running `exit`. Environment variables set
within the shell are not persisted.


## API keys for the brokerage

API keys/secrets for the brokerage can be generated on the [user account page](https://app.architect.co/user/account).


## Maintainers

Python type conversions for scalars should be added to the codegen toml files, if needed.

Important files:
- `schema.graphql`: autogenerated from `architect-gql schema`
- `queries.graphql`: add any new queries/mutations
- `generate_protocol.py`: autogenerates the `architect_py/protocol/client_protocol.py`
- `architect_py/protocol/client_protocol.py`: autogenerated from `generate_protocol.py`, contains the class that the sync client inherits from
- `architect_py/async_client.py`: inherits from the ariadne generated base client
- `architect_py/client.py`: contains the sync client, delegates functions calls to a composed AsyncClient in the innards, inherits from the client_protocol to give the correct type hinting from Pylance
- `tests` and `examples`: self-explanatory

The purpose of the client_protocol.py is so that the sync client can inherit from it and users can get good code completion and get the correct typing on their function calls, because
the type-checker would otherwise not play nice with the way the sync_client is using the getattr magic function.

On any update, please run `update.sh` and update the version in the `version` file on the top level.
To publish a version, run `poetry build` then `poetry publish`.


In addition, any new function should have a test included in test.py

To run tests:
`export $(cat pytest.env | xargs)`
`pytest tests/*`

### What does `update.sh` do?

1. Uses ariadne-codegen to generate the async client
2. Autogenerates the protocol that the sync client inherits from
