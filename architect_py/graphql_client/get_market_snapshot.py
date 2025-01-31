# Generated by ariadne-codegen
# Source: queries.graphql

from .base_model import BaseModel
from .fragments import MarketTickerFields


class GetMarketSnapshot(BaseModel):
    marketdata: "GetMarketSnapshotMarketdata"


class GetMarketSnapshotMarketdata(BaseModel):
    ticker: "GetMarketSnapshotMarketdataTicker"


class GetMarketSnapshotMarketdataTicker(MarketTickerFields):
    pass


GetMarketSnapshot.model_rebuild()
GetMarketSnapshotMarketdata.model_rebuild()
