import asyncio
from websockets.exceptions import ConnectionClosed
import json
import logging


import asyncio

from websockets.asyncio.server import serve

from typing import Any, Dict


class JsonWsServer:
    def __init__(self) -> None:
        self.subscriptions = {}

    async def serve(self, host: str, port: int) -> None:
        logging.critical(f"Starting server on {host}:{port}")
        await serve(self.accept_connection, host, port)

    async def accept_connection(self, websocket):
        try:
            async for message in websocket:
                data = json.loads(message)
                response = await self.handle_message(data)
                await websocket.send(json.dumps(response))
        except ConnectionClosed as e:
            print(f"Connection closed: {e}")

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        message_type = message.get("type")
        if message_type == "query":
            return await self.handle_query(message)
        elif message_type == "subscribe":
            return await self.handle_subscribe(message)
        else:
            return {"status": "error", "error": "Unknown message type"}

    async def handle_query(self, message: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        method = message.get("method")
        params = message.get("params")
        if method == "symbology/snapshot":
            return {
                "id": message["id"],
                "type": "response",
                "result": self.get_symbology_snapshot(),
            }
        elif method == "marketdata/book/l2/snapshot":
            return {
                "id": message["id"],
                "type": "response",
                "result": self.get_l2_book_snapshot(params),
            }
        elif method == "marketdata/book/l3/snapshot":
            return {
                "id": message["id"],
                "type": "response",
                "result": self.get_l3_book_snapshot(params),
            }
        else:
            return {"id": message["id"], "type": "response", "error": "Unknown method"}

    async def handle_subscribe(self, message: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        topic = message.get("topic")
        self.subscriptions[topic] = message["id"]
        return {"id": message["id"], "type": "response", "status": "subscribed"}

    def get_symbology_snapshot(self) -> Dict[str, Any]:
        raise NotImplementedError
        return {"routes": [], "venues": [], "products": [], "markets": []}

    def get_l2_book_snapshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        return {}

    def get_l3_book_snapshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        return {"bids": [], "asks": []}


async def start_server():
    server = JsonWsServer()
    start_server = serve(server.accept_connection, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await start_server


async def test():
    server = JsonWsServer()
    start_server = serve(server.accept_connection, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    await start_server


if __name__ == "__main__":
    asyncio.run(test())
