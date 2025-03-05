# generated by datamodel-codegen:
#   filename:  SubscribeOrderflowRequest.json

from __future__ import annotations
from architect_py.grpc_client.Orderflow.Orderflow import Orderflow
from architect_py.grpc_client.request import RequestStream


from typing import Optional

from msgspec import Struct

AccountIdOrName = str


TraderIdOrEmail = str


class SubscribeOrderflowRequest(Struct):
    """
    Subscribe/listen to orderflow events.
    """

    account: Optional[AccountIdOrName] = None
    execution_venue: Optional[str] = None
    trader: Optional[TraderIdOrEmail] = None

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestStream(SubscribeOrderflowRequest, Orderflow, "/json.architect.Orderflow/SubscribeOrderflow")

