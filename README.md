# architect_py

## Example

```python
import asyncio
from architect_py.client import Client


async def main():
    c = Client(
        "https://<your installation domain>:4567",
        "wss://<your installation domain>:4567/subscriptions",
        "<api key>",
        "<api secret>"
    )
    print(await c.execute_async("query { me { userId email } }"))
    s = await c.subscribe_async(
        """
    subscription {
        trades(market: "BTC Crypto/USD*COINBASE/DIRECT") {
            time
            direction
            price
            size
        }
    }
    """
    )
    async for trade in s:
        print(trade)


asyncio.run(main())
```