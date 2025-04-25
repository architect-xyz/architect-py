# [![Architect](https://avatars.githubusercontent.com/u/116864654?s=29&v=2)](https://architect.co) architect_py 
[![PyPI version](https://img.shields.io/pypi/v/architect-py.svg)](https://pypi.org/project/architect-py/)

A fully-featured Python SDK for trading on [Architect](https://architect.co).

Just some of the features of this SDK: symbology, portfolio management, order entry, advanced algos, and marketdata subscriptions.

Also, it is compatible with Jupyter notebooks! Check the [examples for an example notebook](examples/jupyter_example.ipynb).

## Installation

- pip: `pip install architect-py`
- poetry: `poetry add architect-py`
- uv: `uv add architect-py`

## API keys for the brokerage

API keys/secrets for the brokerage can be generated on the [user account page](https://app.architect.co/user/account).


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


## Method catalog 

Check out the [FUNCTIONS.md](FUNCTIONS.md)  file to see a catalog of methods.

---


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
