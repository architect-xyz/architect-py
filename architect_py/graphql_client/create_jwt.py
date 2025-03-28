# Generated by ariadne-codegen
# Source: queries.graphql

from pydantic import Field

from .base_model import BaseModel


class CreateJwt(BaseModel):
    user: "CreateJwtUser"


class CreateJwtUser(BaseModel):
    create_jwt: str = Field(alias="createJwt")


CreateJwt.model_rebuild()
