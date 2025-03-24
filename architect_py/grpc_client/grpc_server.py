import grpc
import msgspec
from typing import Union
from .grpc_client import encoder
from .Cpty.CptyRequest import Login, Logout, PlaceOrder, CancelOrder
from .Orderflow.SubscribeOrderflowRequest import SubscribeOrderflowRequest


class CptyServicer(object):
    def Cpty(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_CptyServicer_to_server(servicer, server):
    # CR alee: there must be a better way to get the unannotated request type
    decoder = msgspec.json.Decoder(type=Union[Login, Logout, PlaceOrder, CancelOrder])
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
    # CR alee: this doesn't work
    # decoder = msgspec.json.Decoder(type=SubscribeOrderflowRequest.get_unannotated_response_type())
    decoder = msgspec.json.Decoder(type=dict)
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
