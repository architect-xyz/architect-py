# Generated by ariadne-codegen
# Source: ../../queries.graphql

from pydantic import Field

from .base_model import BaseModel


class RemoveTelegramApiKeys(BaseModel):
    remove_telegram_api_keys: bool = Field(alias="removeTelegramApiKeys")