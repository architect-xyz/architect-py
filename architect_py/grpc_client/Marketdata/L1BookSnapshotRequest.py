# generated by datamodel-codegen:
#   filename:  L1BookSnapshotRequest.json

from __future__ import annotations
from architect_py.grpc_client.Marketdata.L1BookSnapshot import L1BookSnapshot
from architect_py.grpc_client.request import RequestUnary


from msgspec import Struct


class L1BookSnapshotRequest(Struct):
    symbol: str

    @staticmethod
    def get_request_helper():
        return request_helper


request_helper = RequestUnary(L1BookSnapshotRequest, L1BookSnapshot, "/json.architect.Marketdata/L1BookSnapshot")

