# architect_py

`poetry run ariadne-codegen`

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