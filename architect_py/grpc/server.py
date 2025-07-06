"""
Utility functions for hosting an Architect gRPC server;
external cptys, python-based marketdata feeds, etc.
"""

import grpc
import msgspec

from .models.Cpty.CptyRequest import UnannotatedCptyRequest
from .models.Marketdata.L1BookSnapshotRequest import L1BookSnapshotRequest
from .models.Marketdata.L2BookSnapshotRequest import L2BookSnapshotRequest
from .models.Marketdata.SubscribeL1BookSnapshotsRequest import (
    SubscribeL1BookSnapshotsRequest,
)
from .models.Marketdata.SubscribeL2BookUpdatesRequest import (
    SubscribeL2BookUpdatesRequest,
)
from .models.Marketdata.SubscribeTradesRequest import SubscribeTradesRequest
from .models.Orderflow.SubscribeOrderflowRequest import SubscribeOrderflowRequest
from .utils import encoder


def dec_hook(type, obj):
    # type should have a static method deserialize
    return type.deserialize(obj)


class CptyServicer(object):
    def Cpty(self, _request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CptyServicer_to_server(servicer, server):
    decoder = msgspec.json.Decoder(type=UnannotatedCptyRequest, dec_hook=dec_hook)
    rpc_method_handlers = {
        "Cpty": grpc.stream_stream_rpc_method_handler(
            servicer.Cpty,
            request_deserializer=decoder.decode,
            response_serializer=encoder.encode,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "json.architect.Cpty", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class OrderflowServicer(object):
    def SubscribeOrderflow(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_OrderflowServicer_to_server(servicer, server):
    decoder = msgspec.json.Decoder(type=SubscribeOrderflowRequest, dec_hook=dec_hook)
    rpc_method_handlers = {
        "SubscribeOrderflow": grpc.unary_stream_rpc_method_handler(
            servicer.SubscribeOrderflow,
            request_deserializer=decoder.decode,
            response_serializer=encoder.encode,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "json.architect.Orderflow", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


class MarketdataServicer(object):
    def _unimplemented(self, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def L1BookSnapshot(self, _request, context):
        self._unimplemented(context)

    def SubscribeL1BookSnapshots(self, _request, context):
        self._unimplemented(context)

    def L2BookSnapshot(self, _request, context):
        self._unimplemented(context)

    def SubscribeL2BookUpdates(self, _request, context):
        self._unimplemented(context)

    def SubscribeTrades(self, _request, context):
        self._unimplemented(context)


def add_MarketdataServicer_to_server(servicer, server):
    decoders = {
        "L1BookSnapshot": msgspec.json.Decoder(
            type=L1BookSnapshotRequest, dec_hook=dec_hook
        ),
        "SubscribeL1BookSnapshots": msgspec.json.Decoder(
            type=SubscribeL1BookSnapshotsRequest, dec_hook=dec_hook
        ),
        "L2BookSnapshot": msgspec.json.Decoder(
            type=L2BookSnapshotRequest, dec_hook=dec_hook
        ),
        "SubscribeL2BookUpdates": msgspec.json.Decoder(
            type=SubscribeL2BookUpdatesRequest, dec_hook=dec_hook
        ),
        "SubscribeTrades": msgspec.json.Decoder(
            type=SubscribeTradesRequest, dec_hook=dec_hook
        ),
    }
    rpc_method_handlers = {
        "L1BookSnapshot": grpc.unary_unary_rpc_method_handler(
            servicer.L1BookSnapshot,
            request_deserializer=decoders["L1BookSnapshot"].decode,
            response_serializer=encoder.encode,
        ),
        "SubscribeL1BookSnapshots": grpc.unary_stream_rpc_method_handler(
            servicer.SubscribeL1BookSnapshots,
            request_deserializer=decoders["SubscribeL1BookSnapshots"].decode,
            response_serializer=encoder.encode,
        ),
        "L2BookSnapshot": grpc.unary_unary_rpc_method_handler(
            servicer.L2BookSnapshot,
            request_deserializer=decoders["L2BookSnapshot"].decode,
            response_serializer=encoder.encode,
        ),
        "SubscribeL2BookUpdates": grpc.unary_stream_rpc_method_handler(
            servicer.SubscribeL2BookUpdates,
            request_deserializer=decoders["SubscribeL2BookUpdates"].decode,
            response_serializer=encoder.encode,
        ),
        "SubscribeTrades": grpc.unary_stream_rpc_method_handler(
            servicer.SubscribeTrades,
            request_deserializer=decoders["SubscribeTrades"].decode,
            response_serializer=encoder.encode,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "json.architect.Marketdata", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
