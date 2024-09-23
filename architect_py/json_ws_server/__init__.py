import asyncio
from websockets.exceptions import ConnectionClosed
import json
import logging


from websockets.asyncio.server import serve, ServerConnection

from typing import Any, Dict


class JsonWsServer:
    def __init__(self) -> None:
        pass

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
        if method == "symbology/snapshot":
            return {
                "id": message["id"],
                "type": "response",
                "result": self.get_symbology_snapshot(),
            }
        elif method == "marketdata/book/l2/snapshot":
            if params is not None:
                return {
                    "id": message["id"],
                    "type": "response",
                    "result": self.get_l2_book_snapshot(params),
                }
            else:
                return {
                    "id": message["id"],
                    "type": "response",
                    "result": "error: params was None",
                }
        elif method == "marketdata/book/l3/snapshot":
            if params is not None:
                return {
                    "id": message["id"],
                    "type": "response",
                    "result": self.get_l3_book_snapshot(params),
                }
            else:
                return {
                    "id": message["id"],
                    "type": "response",
                    "result": "error: params was None",
                }
        else:
            return {"id": message["id"], "type": "response", "error": "Unknown method"}

    async def handle_subscribe(
        self, message: Dict[str, Any], websocket: ServerConnection
    ) -> Dict[str, Any]:
        topic = message.get("topic")

        if topic is None:
            return {"id": message["id"], "type": "response", "error": "No topic provided"}
        
        

        asyncio.create_task(self._subscribe(topic, websocket))
        return {"id": message["id"], "type": "response", "status": "subscribed"}

    async def _subscribe(self, topic: str, websocket: ServerConnection):
        # acho CR: This is a potentially inoptimal implementation
        await asyncio.sleep(5)


        await websocket.send(json.dumps(response))


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
