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

## Method catalog 

Go to [FUNCTIONS.md](FUNCTIONS.md) file to see a catalog of methods.

## Examples

Go to the [Examples](./examples) to see examples of a variety of common use cases.  To run a specific example, use e.g. `python -m examples.orderflow_streaming`.

## Documentation 

See the [Getting started with Python](https://docs.architect.co/getting-started-with-python) guide for more information.

## Imports

In general, most types in the package can be imported from the top-level; in rare cases, some types may come from GraphQL and need to be imported from `architect_py.graphql_client.fragments`.

```python
from architect_py import *  # includes both AsyncClient and Client
from architect_py.graphql_client.fragments import (
    ExecutionInfoFields,
    ProductInfoFields,
)
```

Using an LLM or an IDE with code completion like VSCode or PyCharm can be very helpful.