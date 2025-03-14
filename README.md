# architect_py
[![PyPI version](https://img.shields.io/pypi/v/architect-py.svg)](https://pypi.org/project/architect-py/)

A Python API for [Architect](https://architect.co).

Just some of the features of this API:
symbology, market snapshots, past trades, account queries, order management (including sending advanced algos!), and market feed subscriptions.

This repo heavily uses type hinting, so using a type checker such as Pylance or mypy is suggestible to reduce potential for error.


## Example usage

`AsyncClient` and `Client` are the entryways into making calls to the Architect backend.


```python
import asyncio
from architect_py.async_client import AsyncClient


async def main():
    c = AsyncClient(
        host="<your installation domain>",  # e.g. app.architect.co for the brokerage
        api_key="<api key>",
        api_secret="<api secret>"
    )
    print(await c.execute("query { me { userId email } }"))
    s = c.subscribe_trades("BTC Crypto/USD*COINBASE/DIRECT")
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
    )
    print(await c.execute("query { me { userId email } }"))
    print("\n\n")
    print(client.get_balances_and_positions())
    print("\n\n")
    print(client.search_markets(glob="ES*", venue="CME"))
```

While the AsyncClient is the recommended way to use the Architect API, the Client instead without any familiarity with `async/await`.
The sync clients and async clients usage is identical, except one removes the `await` before the call. The only exception to this is that the sync client does not support any subscriptions, because they are inherently asynchronous.

Check the `examples` folder or the `architect_py/tests` folders for example usages.


## Function Breakdown


The `async` client has the following functions
```
""" SYMBOLOGY + PRODUCT INFO """
    search_symbols
    get_product_info
    get_product_infos
    get_cme_first_notice_date
    get_future_series
    get_execution_info
    get_expiration_from_CME_name
    get_cme_futures_series
    get_cme_future_from_root_month_year

""" ACCOUNT INFO """
    list_accounts
    get_account_summary
    get_account_summaries

""" ORDER HISTORY """
    get_open_orders
    get_all_open_orders
    get_historical_orders
    get_order
    get_orders
    get_fills

""" MARKET DATA """
    get_market_status
    market_snapshot
    market_snapshots
    l1_book_snapshot
    l1_book_snapshots
    l2_book_snapshot
    subscribe_l1_book_snapshots
    subscribe_l2_book_updates
    watch_l2_book
    get_external_l2_book_snapshot
    get_l3_book_snapshot
    subscribe_trades

""" ORDER SENDING """
    send_limit_order
    send_market_pro_order
    cancel_order
    cancel_all_orders
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
