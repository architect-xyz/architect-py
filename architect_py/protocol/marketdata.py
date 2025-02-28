from typing import Union

import grpc
import msgspec

from architect_py.grpc_client.Marketdata.Marketdata_L1BookSnapshot import L1BookSnapshot
from architect_py.grpc_client.Marketdata.Marketdata_L2BookSnapshot import L2BookSnapshot
from architect_py.grpc_client.Marketdata.Marketdata_L2BookUpdate import L2BookUpdate


class JsonMarketdataStub:
    def __init__(self, channel: Union[grpc.Channel, grpc.aio.Channel]):
        self.SubscribeL1BookSnapshots = channel.unary_stream(
            "/json.architect.Marketdata/SubscribeL1BookSnapshots",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L1BookSnapshot
            ),
        )
        self.L2BookSnapshot = channel.unary_unary(
            "/json.architect.Marketdata/L2BookSnapshot",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L2BookSnapshot
            ),
        )
        self.SubscribeL2BookUpdates = channel.unary_stream(
            "/json.architect.Marketdata/SubscribeL2BookUpdates",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=L2BookUpdate
            ),
        )
