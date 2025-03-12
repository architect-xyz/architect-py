# generated by datamodel-codegen:
#   filename:  Symbology/UploadSymbologyRequest.json

from __future__ import annotations
from architect_py.grpc_client.Symbology.UploadSymbologyResponse import (
    UploadSymbologyResponse,
)

from typing import Dict, Optional

from msgspec import Struct

from .. import definitions


class UploadSymbologyRequest(Struct):
    execution_info: Optional[Dict[str, Dict[str, definitions.ExecutionInfo]]] = None
    options_series: Optional[Dict[str, definitions.OptionsSeriesInfo]] = None
    product_aliases: Optional[Dict[str, Dict[str, str]]] = None
    products: Optional[Dict[str, definitions.ProductInfo]] = None

    @staticmethod
    def get_response_type():
        return UploadSymbologyResponse

    @staticmethod
    def get_route() -> str:
        return "/json.architect.Symbology/UploadSymbology"

    @staticmethod
    def get_unary_type():
        return "unary"
