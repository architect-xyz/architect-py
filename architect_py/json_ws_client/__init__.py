from dataclasses import fields, is_dataclass, dataclass

import logging
import orjson
import uuid
import websockets.client
from ..protocol import (
    ProtocolQueryMessage,
    ProtocolResponseMessage,
    ProtocolSubscribeMessage,
)
from ..protocol.symbology import SymbologySnapshot, Route, Venue, Product, Market
from ..protocol.marketdata import (
    PriceV1,
    QueryL2BookSnapshot,
    QueryL3BookSnapshot,
    L2BookSnapshot,
    L3BookSnapshot,
    L3Order,
    QueryPriceV1,
    TradeV1,
)
from typing import (
    Any,
    AsyncIterator,
    Optional,
    TypeVar,
    Type,
    TYPE_CHECKING,
    get_origin,
    get_args,
    Tuple,
)

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

    T = TypeVar("T", bound=DataclassInstance)
else:
    T = TypeVar("T")


class JsonWsClient:
    def __init__(self, *, url: str):
        self.url = url
        self.next_request_id = 1
        self.logger = logging.getLogger(name=self.__class__.__name__)
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

    def _connect(self):
        return websockets.client.connect(self.url, max_size=1_000_000_000)

    def _request_id(self):
        request_id = self.next_request_id
        self.next_request_id += 1
        return request_id

    @staticmethod
    def hydrate_dataclass(data: Any, cls: Type[T]) -> T:
        # for simple dataclasses just use cls(**data)

        stack: list[Tuple[Type[DataclassInstance], Any, dict]] = [(cls, data, {})]
        field_cache: dict[Type, dict[str, Any]] = {}

        while stack:
            current_cls, current_data, current_kwargs = stack.pop()

            if current_cls not in field_cache:
                field_cache[current_cls] = {
                    f.name: (f.type, get_origin(f.type) or f.type)
                    for f in fields(current_cls)
                }

            field_types = field_cache[current_cls]

            for key, value in current_data.items():
                if key not in field_types:
                    logging.warning(
                        f"Unknown field {key} transmitted while creating {current_cls}"
                    )
                    continue

                origin_type: type
                field_type, origin_type = field_types[key]

                if origin_type in (int, float, str, bool):
                    current_kwargs[key] = value
                elif origin_type is dict:
                    val_type: Type[DataclassInstance]
                    _, val_type = get_args(field_type)
                    if is_dataclass(val_type):
                        current_kwargs[key] = {
                            k: JsonWsClient.hydrate_dataclass(v, val_type)
                            for k, v in value.items()
                        }
                    else:
                        current_kwargs[key] = value
                elif origin_type in (list, tuple, set):
                    item_type: Type[DataclassInstance] = get_args(field_type)[0]
                    if is_dataclass(item_type):
                        current_kwargs[key] = origin_type(
                            JsonWsClient.hydrate_dataclass(item, item_type)
                            for item in value
                        )
                    else:
                        current_kwargs[key] = value
                elif is_dataclass(origin_type):
                    stack.append((origin_type, value, {}))
                else:
                    raise ValueError(
                        f"Unknown type {origin_type}, field_type: {field_type},"
                        f"key: {key}, value: {value}"
                        f"cls: {current_cls}"
                    )

            if not stack:
                return current_cls(**current_kwargs)  # type: ignore

        raise ValueError(f"Unexpected end of dataclass hydration process {data} {cls}")

    async def request(self, method: str, params: Optional[Any] = None) -> Any:
        async with self._connect() as ws:
            id = self._request_id()
            query = ProtocolQueryMessage(
                id=id,
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

    async def subscribe(self, topic: str) -> AsyncIterator[Any]:
        async with self._connect() as ws:
            id = self._request_id()
            query = ProtocolSubscribeMessage(
                id=id,
                topic=topic,
            )
            await ws.send(message=orjson.dumps(query))
            async for message in ws:
                m = orjson.loads(message)
                if m["type"] == "update" and m["id"] == id:
                    yield m["data"]
                elif m["type"] == "response" and m["id"] == id:
                    if "error" in m:
                        raise Exception(m["error"])

    async def get_symbology_snapshot(self) -> SymbologySnapshot:
        res = await self.request("symbology/snapshot")
        snap = self.hydrate_dataclass(res, SymbologySnapshot)
        return snap

    async def get_l2_book_snapshot(self, market_id: uuid.UUID) -> L2BookSnapshot:
        res = await self.request(
            "marketdata/book/l2/snapshot", QueryL2BookSnapshot(market_id=market_id)
        )
        return L2BookSnapshot(**res)

    async def get_l3_book_snapshot(self, market_id: uuid.UUID) -> L3BookSnapshot:
        res: dict[str, Any] = await self.request(
            "marketdata/book/l3/snapshot", QueryL3BookSnapshot(market_id=market_id)
        )

        snap = self.hydrate_dataclass(res, L3BookSnapshot)

        return snap

    async def get_index_value(self, market_id: uuid.UUID) -> PriceV1:
        res = await self.request(
            "marketdata/book/price", QueryPriceV1(market_id=market_id)
        )
        snap = self.hydrate_dataclass(res, PriceV1)
        return snap

    async def subscribe_trades(self, market_id: uuid.UUID) -> AsyncIterator[TradeV1]:
        async for data in self.subscribe(f"marketdata/trades/{market_id}"):
            yield TradeV1(**data)


if __name__ == "__main__":
    # basic testing
    @dataclass
    class Test:
        f1: int
        f2: list[int]
        f3: dict[int, list[tuple[int, int]]]
        f4: dict[int, int]
        f5: str
        f6: list[str]

    json = {
        "f1": 4,
        "f2": [23, 123, 123, 213],
        "f3": {3: [(3, 4), (5, 4), (6, 7)], 5: [(2, 3)], 8: [(3, 3), (4, 4)]},
        "f4": {5: 5, 3: 3, 1: 1},
        "f5": "asfasf",
        "f6": ["this", "is", "a", "test"],
    }

    hydrated_class = JsonWsClient.hydrate_dataclass(json, Test)
    print(hydrated_class)
