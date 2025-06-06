# generated by datamodel-codegen:
#   filename:  Symbology/SymbologyUpdate.json

from __future__ import annotations

from typing import Annotated, Optional

from msgspec import Meta, Struct

from .. import definitions


class SymbologyUpdate(Struct, omit_defaults=True):
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
    product_catalog: Optional[
        definitions.SnapshotOrUpdateForStringAndSnapshotOrUpdateForStringAndProductCatalogInfo
    ] = None
    products: Optional[definitions.SnapshotOrUpdateForStringAndProductInfo] = None

    # Constructor that takes all field titles as arguments for convenience
    @classmethod
    def new(
        cls,
        sequence_id: int,
        sequence_number: int,
        execution_info: Optional[
            definitions.SnapshotOrUpdateForStringAndSnapshotOrUpdateForStringAndExecutionInfo
        ] = None,
        options_series: Optional[
            definitions.SnapshotOrUpdateForStringAndOptionsSeriesInfo
        ] = None,
        product_aliases: Optional[
            definitions.SnapshotOrUpdateForAliasKindAndSnapshotOrUpdateForStringAndString
        ] = None,
        product_catalog: Optional[
            definitions.SnapshotOrUpdateForStringAndSnapshotOrUpdateForStringAndProductCatalogInfo
        ] = None,
        products: Optional[definitions.SnapshotOrUpdateForStringAndProductInfo] = None,
    ):
        return cls(
            sequence_id,
            sequence_number,
            execution_info,
            options_series,
            product_aliases,
            product_catalog,
            products,
        )

    def __str__(self) -> str:
        return f"SymbologyUpdate(sequence_id={self.sid},sequence_number={self.sn},execution_info={self.execution_info},options_series={self.options_series},product_aliases={self.product_aliases},product_catalog={self.product_catalog},products={self.products})"

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
