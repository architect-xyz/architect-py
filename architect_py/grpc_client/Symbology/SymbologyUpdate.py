# generated by datamodel-codegen:
#   filename:  Symbology/SymbologyUpdate.json

from __future__ import annotations

from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class SymbologyUpdate(Struct):
    """
    Unique sequence id and number.
    """

    sid: Annotated[int, Meta(ge=0, title="sequence_id")]
    sn: Annotated[int, Meta(ge=0, title="sequence_number")]
    execution_info: Optional[
        definitions.SnapshotOrUpdateForStringAndSnapshotOrUpdateForStringAndExecutionInfo
    ] = None
    options_series: Optional[
        definitions.SnapshotOrUpdateForStringAndOptionsSeriesInfo
    ] = None
    product_aliases: Optional[
        definitions.SnapshotOrUpdateForAliasKindAndSnapshotOrUpdateForStringAndString
    ] = None
    products: Optional[definitions.SnapshotOrUpdateForStringAndProductInfo] = None

    @property
    def sequence_id(self) -> int:
        return self.sid

    @sequence_id.setter
    def sequence_id(self, value: int) -> None:
        self.sid = value

    @property
    def sequence_number(self) -> int:
        return self.sn

    @sequence_number.setter
    def sequence_number(self, value: int) -> None:
        self.sn = value
