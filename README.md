# architect_py

Clone this repository to run examples in the `examples` directory.

```bash
export ARCHITECT_HOST="<your installation domain>"
export ARCHITECT_API_KEY="<api key>"
export ARCHITECT_API_SECRET="<api secret>"

python -m examples.trades
```

## Example

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

## Maintainers

`poetry run ariadne-codegen`
