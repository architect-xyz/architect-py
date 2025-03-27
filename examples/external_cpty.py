from decimal import Decimal
import time
from typing import Iterator
import grpc
from concurrent import futures
from architect_py.grpc_client.Cpty.CptyRequest import CancelOrder, PlaceOrder
from architect_py.grpc_client.Cpty.CptyResponse import Symbology
from architect_py.grpc_client.definitions import (
    CptyLoginRequest,
    CptyLogoutRequest,
    ExecutionInfo,
    MinOrderQuantityUnit,
    SimpleDecimal,
    Unit,
)
from architect_py.grpc_client.grpc_server import (
    add_CptyServicer_to_server,
    CptyServicer,
    add_OrderflowServicer_to_server,
    OrderflowServicer,
)


class MockCptyServicer(CptyServicer, OrderflowServicer):
    def Cpty(self, request_iterator: Iterator, context):
        context.set_code(grpc.StatusCode.OK)
        context.send_initial_metadata({})
        # send symbology
        yield Symbology(
            execution_info={
                "FOO Crypto/USD": {
                    "MOCK": ExecutionInfo(
                        execution_venue="MOCK",
                        exchange_symbol=None,
                        tick_size=SimpleDecimal(Decimal("0.01")),
                        step_size=Decimal("0.1"),
                        min_order_quantity=Decimal(0),
                        min_order_quantity_unit=MinOrderQuantityUnit(Unit.base),
                        is_delisted=False,
                        initial_margin=None,
                        maintenance_margin=None,
                    ),
                }
            }
        )
        for req in request_iterator:
            if isinstance(req, CptyLoginRequest):
                print("login message received", req)
            elif isinstance(req, CptyLogoutRequest):
                print("logout message received", req)
            elif isinstance(req, PlaceOrder):
                print("place_order message received", req)
            elif isinstance(req, CancelOrder):
                print("cancel_order message received", req)

    def SubscribeOrderflow(self, request, context):
        context.set_code(grpc.StatusCode.OK)
        context.send_initial_metadata({})
        time.sleep(100)


def serve():
    thread_pool = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(thread_pool)
    servicer = MockCptyServicer()
    add_CptyServicer_to_server(servicer, server)
    add_OrderflowServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
