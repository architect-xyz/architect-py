# Generated by ariadne-codegen
# Source: queries.graphql

from .base_model import BaseModel
from .fragments import MarketTickerFields


class GetMarketSnapshotQuery(BaseModel):
    marketdata: "GetMarketSnapshotQueryMarketdata"


class GetMarketSnapshotQueryMarketdata(BaseModel):
    ticker: "GetMarketSnapshotQueryMarketdataTicker"


class GetMarketSnapshotQueryMarketdataTicker(MarketTickerFields):
    pass


GetMarketSnapshotQuery.model_rebuild()
GetMarketSnapshotQueryMarketdata.model_rebuild()
