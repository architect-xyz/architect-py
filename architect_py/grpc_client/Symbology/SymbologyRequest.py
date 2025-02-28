# generated by datamodel-codegen:
#   filename:  SymbologyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.SymbologySnapshot import SymbologySnapshot
import grpc
import msgspec

from msgspec import Struct


class SymbologyRequest(Struct):
    pass
def create_stub(channel: grpc.Channel | grpc.aio.Channel) -> None:
	channel.unary_unary(
		"/json.architect.Symbology/Symbology",
		request_serializer=msgspec.json.encode,
		response_deserializer=lambda buf: msgspec.json.decode(
			buf, type=SymbologySnapshot
		),
	)
