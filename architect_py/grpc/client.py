from types import UnionType
from typing import AsyncIterator

import grpc
import msgspec

from . import *
from .utils import RequestType, ResponseTypeGeneric, decoders, encoder


class GrpcClient:
    endpoint: str
    channel: grpc.aio.Channel
    jwt: str | None = None

    def __init__(self, *, host: str, port: int, use_ssl: bool = False):
        scheme = "https" if use_ssl else "http"
        self.endpoint = f"{scheme}://{host}:{port}"
        if use_ssl:
            credentials = grpc.ssl_channel_credentials()
            self.channel = grpc.aio.secure_channel(f"{host}:{port}", credentials)
        else:
            self.channel = grpc.aio.insecure_channel(f"{host}:{port}")

    def set_jwt(self, jwt: str | None):
        self.jwt = jwt

    @staticmethod
    def encoder() -> msgspec.json.Encoder:
        return encoder

    def get_decoder(
        self, response_type: type[ResponseTypeGeneric] | UnionType
    ) -> msgspec.json.Decoder:
        try:
            return decoders[response_type]
        except KeyError:
            decoder = msgspec.json.Decoder(type=response_type)
            decoders[response_type] = decoder
            return decoder

    async def unary_unary(
        self,
        request: RequestType[ResponseTypeGeneric],
    ) -> ResponseTypeGeneric:
        """
        Generic function for making a unary RPC call to the gRPC server.

        NB: request_type and ResponseTypeGeneric *cannot* be union types
        """
        decoder: msgspec.json.Decoder[ResponseTypeGeneric] = self.get_decoder(
            request.get_unannotated_response_type()
        )
        stub: grpc.aio.UnaryUnaryMultiCallable[
            RequestType[ResponseTypeGeneric], ResponseTypeGeneric
        ] = self.channel.unary_unary(
            request.get_route(),
            request_serializer=encoder.encode,
            response_deserializer=decoder.decode,
        )
        if self.jwt is not None:
            metadata = (("authorization", f"Bearer {self.jwt}"),)
        else:
            metadata = ()
        return await stub(request, metadata=metadata)

    async def unary_stream(
        self,
        request: RequestType[ResponseTypeGeneric],
    ) -> AsyncIterator[ResponseTypeGeneric]:
        """
        Generic function for subscribing to a stream of updates from the gRPC server.

        NB: request_type and ResponseTypeGeneric *cannot* be union types
        """
        decoder: msgspec.json.Decoder[ResponseTypeGeneric] = self.get_decoder(
            request.get_unannotated_response_type()
        )
        stub: grpc.aio.UnaryStreamMultiCallable[
            RequestType[ResponseTypeGeneric], ResponseTypeGeneric
        ] = self.channel.unary_stream(
            request.get_route(),
            request_serializer=encoder.encode,
            response_deserializer=decoder.decode,
        )
        if self.jwt is not None:
            metadata = (("authorization", f"Bearer {self.jwt}"),)
        else:
            metadata = ()
        call: grpc.aio._base_call.UnaryStreamCall[
            RequestType[ResponseTypeGeneric], ResponseTypeGeneric
        ] = stub(request, metadata=metadata)
        async for update in call:
            yield update
