# generated by datamodel-codegen:
#   filename:  L1BookSnapshotsRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.Array_of_L1BookSnapshot import ArrayOfL1BookSnapshot
import grpc
import msgspec

from typing import List, Optional

from msgspec import Struct


class L1BookSnapshotsRequest(Struct):
    symbols: Optional[List[str]] = None

    @staticmethod
    def create_stub(channel: grpc.aio.Channel) -> grpc.aio.UnaryUnaryMultiCallable["L1BookSnapshotsRequest", ArrayOfL1BookSnapshot]:
        return channel.unary_unary(
            "/json.architect.Marketdata/L1BookSnapshots",
            request_serializer=msgspec.json.encode,
            response_deserializer=lambda buf: msgspec.json.decode(
                buf, type=ArrayOfL1BookSnapshot
            ),
        )
