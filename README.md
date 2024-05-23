# architect_py

## Example usage

```python
import asyncio
from architect_py.client import Client


async def main():
    c = Client(
        host="<your installation domain>",
        api_key="<api key>",
        api_secret="<api secret>"
    )
    print(await c.execute("query { me { userId email } }"))
    s = c.subscribe_trades("BTC Crypto/USD*COINBASE/DIRECT")
    async for trade in s:
        print(trade)


asyncio.run(main())
```

## Running additional examples from this package

Clone this repository to run examples in the `examples` directory.  This package
uses poetry for dependency management.  To enter a poetry virtual environment, make
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

You can exit the poetry shell by running `exit`.  Environment variables set
within the shell are not persisted.

## Maintainers

`poetry run ariadne-codegen`
