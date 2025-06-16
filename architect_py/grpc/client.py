from types import UnionType
from typing import Any, AsyncIterator, Sequence, Tuple

import grpc.aio
import msgspec

from . import *
from .utils import RequestType, ResponseTypeGeneric, decoders, encoder


def dec_hook(type, obj):
    # type should have a static method deserialize
    return type.deserialize(obj)


class GrpcClient:
    endpoint: str
    channel: grpc.aio.Channel
    jwt: str | None = None
    as_user: str | None = None
    as_role: str | None = None

    def __init__(
        self,
        *,
        host: str,
        port: int,
        use_ssl: bool = False,
        options: Sequence[Tuple[str, Any]] | None = None,
        as_user: str | None = None,
        as_role: str | None = None,
    ):
        scheme = "https" if use_ssl else "http"
        self.endpoint = f"{scheme}://{host}:{port}"
        self.as_user = as_user
        self.as_role = as_role
        if use_ssl:
            credentials = grpc.ssl_channel_credentials()
            self.channel = grpc.aio.secure_channel(
                f"{host}:{port}", credentials, options=options
            )
        else:
            self.channel = grpc.aio.insecure_channel(f"{host}:{port}", options=options)

    def set_jwt(self, jwt: str | None):
        self.jwt = jwt

    def metadata(self) -> Sequence[Tuple[str, str]]:
        metadata = []
        if self.jwt is not None:
            metadata.append(("authorization", f"Bearer {self.jwt}"))
        if self.as_user is not None:
            metadata.append(("x-architect-user", self.as_user))
        if self.as_role is not None:
            metadata.append(("x-architect-role", self.as_role))
        return metadata

    async def close(self):
        await self.channel.close()

    @staticmethod
    def encoder() -> msgspec.json.Encoder:
        return encoder

    def get_decoder(
        self, response_type: type[ResponseTypeGeneric] | UnionType
    ) -> msgspec.json.Decoder:
        try:
            return decoders[response_type]
        except KeyError:
            decoder = msgspec.json.Decoder(type=response_type, dec_hook=dec_hook)
            decoders[response_type] = decoder
            return decoder

    async def unary_unary(
        self,
        request: RequestType[ResponseTypeGeneric],
        *,
        no_metadata: bool = False,
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
        if no_metadata:
            metadata = ()
        else:
            metadata = self.metadata()
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
        metadata = self.metadata()
        call: grpc.aio.UnaryStreamCall[
            RequestType[ResponseTypeGeneric], ResponseTypeGeneric
        ] = stub(request, metadata=metadata)
        async for update in call:
            yield update
