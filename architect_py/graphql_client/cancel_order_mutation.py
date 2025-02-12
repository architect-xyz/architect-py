# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import CancelFields


class CancelOrderMutation(BaseModel):
    oms: "CancelOrderMutationOms"


class CancelOrderMutationOms(BaseModel):
    cancel_order: "CancelOrderMutationOmsCancelOrder" = Field(alias="cancelOrder")


class CancelOrderMutationOmsCancelOrder(CancelFields):
    pass


CancelOrderMutation.model_rebuild()
CancelOrderMutationOms.model_rebuild()
