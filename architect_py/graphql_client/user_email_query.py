# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel


class UserEmailQuery(BaseModel):
    user: "UserEmailQueryUser"


class UserEmailQueryUser(BaseModel):
    user_email: str = Field(alias="userEmail")


UserEmailQuery.model_rebuild()
