import orjson
import uuid
import websockets.client
from ..protocol import ProtocolQueryMessage, ProtocolResponseMessage
from ..protocol.symbology import SymbologySnapshot, Route, Venue, Product, Market
from ..protocol.marketdata import QueryL2BookSnapshot, L2BookSnapshot
from typing import Optional, Any


class JsonWsClient:
    def __init__(self, *, url: str):
        self.url = url
        self.next_request_id = 1

    def _connect(self):
        return websockets.client.connect(self.url, max_size=1_000_000_000)

    def _request_id(self):
        request_id = self.next_request_id
        self.next_request_id += 1
        return request_id

    async def request(self, method: str, params: Optional[Any] = None) -> Any:
        async with self._connect() as ws:
            id = self._request_id()
            query = ProtocolQueryMessage(
                id=id,
                type="query",
                method=method,
                params=params,
            )
            await ws.send(orjson.dumps(query))
            async for message in ws:
                m = orjson.loads(message)
                if m["type"] == "response":
                    res = ProtocolResponseMessage(**m)
                    if res.id == id:
                        if res.error:
                            raise Exception(res.error)
                        return res.result

    async def get_symbology_snapshot(self) -> SymbologySnapshot:
        res = await self.request("symbology/snapshot")
        snap = SymbologySnapshot(**res)
        # TODO: better/more complete rehydration
        snap.routes = [Route(**r) for r in snap.routes]
        snap.venues = [Venue(**v) for v in snap.venues]
        snap.products = [Product(**p) for p in snap.products]
        snap.markets = [Market(**m) for m in snap.markets]
        return snap

    async def get_l2_book_snapshot(self, market_id: uuid.UUID) -> L2BookSnapshot:
        res = await self.request(
            "marketdata/book/l2/snapshot", QueryL2BookSnapshot(market_id=market_id)
        )
        return L2BookSnapshot(**res)
