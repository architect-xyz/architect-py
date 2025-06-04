# """
# Example of using a bidirectional orderflow channel with the Architect OEMS.

# This connection style is ~equivalent to having a websocket.

# This code example sends a series of orders to Architect while concurrently
# listening to orderflow events.  Compare to `examples/orderflow_streaming.py`,
# which accomplishes the same thing but using a separate asyncio task.
# """

# import asyncio
# from decimal import Decimal

# from architect_py import AsyncClient, OrderDir, PlaceOrderRequest
# from architect_py.grpc.models.Orderflow.OrderflowRequest import PlaceOrder

# from .config import connect_async_client


# async def send_orders(client: AsyncClient):
#     symbol = await client.get_front_future("ES CME Futures")
#     print(f"symbol={symbol}")

#     while True:
#         await asyncio.sleep(1)
#         snap = await client.get_l1_book_snapshot(symbol, "CME")
#         if snap.best_ask is not None:
#             limit_price = snap.best_ask[0]
#             print(f"\nPlacing buy order at {limit_price}\n")
#             try:
#                 req = PlaceOrderRequest.new(
#                     symbol=symbol,
#                     execution_venue="CME",
#                     dir=OrderDir.BUY,
#                     quantity=Decimal(1),
#                     limit_price=limit_price,
#                     post_only=True,
#                     time_in_force="DAY",
#                     order_type="LIMIT",
#                 )
#                 print(f"req={req}")
#                 yield PlaceOrder(req)
#             except Exception as e:
#                 print(f"Error placing order: {e}")
#         else:
#             print("\nNo ask price from snapshot, doing nothing\n")


# async def main():
#     client = await connect_async_client()

#     async for event in client.orderflow(send_orders(client)):
#         print(f" --> {event}")


# asyncio.run(main())
