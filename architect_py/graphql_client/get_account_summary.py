# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import AccountSummaryFields


class GetAccountSummary(BaseModel):
    folio: "GetAccountSummaryFolio"


class GetAccountSummaryFolio(BaseModel):
    account_summary: "GetAccountSummaryFolioAccountSummary" = Field(
        alias="accountSummary"
    )


class GetAccountSummaryFolioAccountSummary(AccountSummaryFields):
    pass


GetAccountSummary.model_rebuild()
GetAccountSummaryFolio.model_rebuild()
