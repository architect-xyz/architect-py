import asyncio
from websockets.exceptions import ConnectionClosed
import json
import logging


from websockets.asyncio.server import serve, ServerConnection

from typing import Any, Callable, Dict, Optional


class JsonWsServer:
    def __init__(self) -> None:
        pass

    async def start(self, host: str, port: int) -> None:
        start_server = serve(self.accept_connection, host, port)
        logging.critical("JsonWsServer started on ws://localhost:8765")
        await start_server

    async def serve(self, host: str, port: int) -> None:
        logging.critical(f"Starting server on {host}:{port}")
        await serve(self.accept_connection, host, port)

    async def accept_connection(self, websocket: ServerConnection):
        try:
            async for message in websocket:
                data = json.loads(message)
                response = await self.handle_message(data, websocket)
                await websocket.send(json.dumps(response))
        except ConnectionClosed as e:
            print(f"Connection closed: {e}")

    async def handle_message(
        self, message: Dict[str, Any], websocket: ServerConnection
    ) -> Dict[str, Any]:
        message_type = message.get("type")
        if message_type == "query":
            return await self.handle_query(message)
        elif message_type == "subscribe":
            return await self.handle_subscribe(message, websocket)
        else:
            return {"status": "error", "error": "Unknown message type"}

    async def handle_query(self, message: Dict[str, Any]) -> Dict[str, Any]:
        method = message.get("method")
        params = message.get("params")

        if not isinstance(method, str):
            return {
                "id": message["id"],
                "type": "response",
                "error": "Must pass method as string",
            }

        method = self.match_method(method)
        if method is None:
            return {
                "id": message["id"],
                "type": "response",
                "error": f"No matching method for {method}",
            }

        return {
            "id": message["id"],
            "type": "response",
            "result": method(params),
        }

    async def handle_subscribe(
        self, message: Dict[str, Any], websocket: ServerConnection
    ) -> Dict[str, Any]:
        topic = message.get("topic")
        id = message.get("id")
        if not isinstance(id, int):
            return {
                "id": message["id"],
                "type": "response",
                "error": f"id must be an integer, {id} of type {type(id)} was sent",
            }

        if not isinstance(topic, str):
            return {
                "id": message["id"],
                "type": "response",
                "error": "No topic provided",
            }

        asyncio.create_task(self._subscribe_poll(topic, id, websocket))
        return {"id": message["id"], "type": "response", "status": "subscribed"}

    async def _subscribe_poll(self, topic: str, id: int, websocket: ServerConnection):
        method = self.match_topic(topic)

        if method is None:
            await websocket.send(
                json.dumps(
                    {
                        "id": id,
                        "type": "response",
                        "error": f"No matching topic for {topic}",
                    }
                )
            )
            return

        while True:
            response = method()
            await websocket.send(
                json.dumps(
                    {
                        "id": id,
                        "type": "update",
                        "data": response,
                    }
                )
            )
            await asyncio.sleep(5)

    def match_method(self, method: str) -> Optional[Callable]:
        # for queries
        raise NotImplementedError

    def match_topic(self, topic: str) -> Optional[Callable]:
        # for subscriptions
        raise NotImplementedError

    def get_symbology_snapshot(self) -> Dict[str, Any]:
        raise NotImplementedError
        return {"routes": [], "venues": [], "products": [], "markets": []}

    def get_l2_book_snapshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        return {}

    def get_l3_book_snapshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
        return {"bids": [], "asks": []}


async def test():
    server = JsonWsServer()


if __name__ == "__main__":
    asyncio.run(test())
