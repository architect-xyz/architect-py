import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Generic, Literal, Optional, TypeVar
from .utils import valid_decimal, valid_uuid


@dataclass(kw_only=True)
class Route:
    NS = uuid.UUID("{0cadbcc5-98bc-4888-94ba-fbbcb6f39132}")
    id: uuid.UUID
    name: str

    def __init__(self, *, id: Optional[uuid.UUID | str] = None, name: str):
        self.id = valid_uuid(id) if id else uuid.uuid5(Route.NS, name)
        self.name = name


@dataclass(kw_only=True)
class Venue:
    NS = uuid.UUID("{dd85a6c5-b45f-46d1-bf50-793dacb1e51a}")
    id: uuid.UUID
    name: str

    def __init__(self, *, id: Optional[uuid.UUID] = None, name: str):
        self.id = valid_uuid(id) if id else uuid.uuid5(Venue.NS, name)
        self.name = name


@dataclass(kw_only=True)
class ProductKind:
    type: str
    value: Optional[dict] = None


@dataclass(kw_only=True)
class CoinProductKind(ProductKind):
    def __init__(self, *, token_info=None):
        super().__init__(type="Coin")
        self.value = {"token_info": token_info if token_info else {}}


@dataclass(kw_only=True)
class EventGroupProductKind(ProductKind):
    def __init__(self, *, event_group: Optional[uuid.UUID] = None):
        super().__init__(type="EventGroup")
        self.value = {"event_group": event_group}


@dataclass(kw_only=True)
class EventContractProductKind(ProductKind):
    def __init__(
        self,
        *,
        event_group: Optional[uuid.UUID] = None,
        outcome_label: Optional[str] = None,
    ):
        super().__init__(type="EventContract")
        self.value = {"event_group": event_group, "outcome_label": outcome_label}


@dataclass(kw_only=True)
class Product:
    NS = uuid.UUID("{bb25a7a7-a61c-485a-ac29-1de369a6a043}")
    id: uuid.UUID
    name: str
    kind: ProductKind

    def __init__(self, *, id: Optional[uuid.UUID] = None, name: str, kind: ProductKind):
        self.id = valid_uuid(id) if id else uuid.uuid5(Product.NS, name)
        self.name = name
        self.kind = kind
        # TODO: check that the name suffix matches the kind, e.g. "Crypto" for "USDC Crypto"


@dataclass(kw_only=True)
class MarketInfo:
    type: str
    value: Optional[dict] = None

    def __init__(
        self,
        *,
        tick_size: Decimal,
        step_size: Decimal,
        min_order_quantity: Optional[Decimal] = None,
        min_order_quantity_unit: Literal["Base", "Quote"] = "Base",
        is_delisted: bool,
    ):
        self.type = "External"
        self.value = {
            "tick_size": tick_size,
            "step_size": step_size,
            "min_order_quantity": min_order_quantity,
            "min_order_quantity_unit": min_order_quantity_unit,
            "is_delisted": is_delisted,
        }


@dataclass(kw_only=True)
class MarketKind:
    type: str
    value: Optional[dict] = None


@dataclass(kw_only=True)
class ExchangeMarketKind(MarketKind):
    def __init__(
        self,
        *,
        base: uuid.UUID,
        quote: uuid.UUID,
    ):
        self.type = "Exchange"
        self.value = {"base": base, "quote": quote}

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            base=uuid.UUID(data["value"]["base"]),
            quote=uuid.UUID(data["value"]["quote"]),
        )


@dataclass(kw_only=True)
class Market:
    NS = uuid.UUID("{0bfe858c-a749-43a9-a99e-6d1f31a760ad}")
    id: uuid.UUID
    name: str
    kind: ExchangeMarketKind
    venue: uuid.UUID
    route: uuid.UUID
    exchange_symbol: str
    extra_info: MarketInfo

    @classmethod
    def derive_id(cls, name: str) -> uuid.UUID:
        return uuid.uuid5(cls.NS, name)

    def __init__(
        self,
        *,
        id: Optional[uuid.UUID | str] = None,
        name: str,
        # if kind is None, base and quote must be provided
        kind: Optional[ExchangeMarketKind | dict] = None,
        base: Optional[uuid.UUID | str] = None,
        quote: Optional[uuid.UUID | str] = None,
        venue: uuid.UUID | str,
        route: uuid.UUID | str,
        exchange_symbol: str,
        # if extra_info is None, the following fields must be provided
        extra_info: Optional[MarketInfo] = None,
        tick_size: Decimal | str = None,
        step_size: Decimal | str = None,
        min_order_quantity: Optional[Decimal | str] = None,
        min_order_quantity_unit: Literal["Base", "Quote"] = "Base",
        is_delisted: bool = None,
    ):
        self.id = valid_uuid(id) if id else uuid.uuid5(Market.NS, name)
        self.name = name
        if kind is not None:
            if isinstance(kind, ExchangeMarketKind):
                self.kind = kind
            else:
                self.kind = ExchangeMarketKind.from_json(kind)
        elif base is not None and quote is not None:
            self.kind = ExchangeMarketKind(
                base=valid_uuid(base), quote=valid_uuid(quote)
            )
        else:
            raise ValueError("either kind or base and quote must be provided")
        self.venue = valid_uuid(venue)
        self.route = valid_uuid(route)
        self.exchange_symbol = exchange_symbol
        if extra_info is not None:
            self.extra_info = extra_info
        else:
            self.extra_info = MarketInfo(
                tick_size=valid_decimal(tick_size),
                step_size=valid_decimal(step_size),
                min_order_quantity=(
                    valid_decimal(min_order_quantity)
                    if min_order_quantity is not None
                    else None
                ),
                min_order_quantity_unit=min_order_quantity_unit,
                is_delisted=is_delisted,
            )
        # TODO: check name matches kind
        # TODO: construct name automatically if ExchangeMarketKind

    def base(self) -> uuid.UUID:
        return self.kind.value["base"]

    def quote(self) -> uuid.UUID:
        return self.kind.value["quote"]

    def tick_size(self) -> Decimal:
        return self.extra_info.value["tick_size"]

    def step_size(self) -> Decimal:
        return self.extra_info.value["step_size"]

    def min_order_quantity(self) -> Decimal:
        return self.extra_info.value["min_order_quantity"]

    def min_order_quantity_unit(self) -> Literal["Base", "Quote"]:
        return self.extra_info.value["min_order_quantity_unit"]

    def is_delisted(self) -> bool:
        return self.extra_info.value["is_delisted"]


@dataclass(kw_only=True)
class SymbologySnapshot:
    epoch: datetime
    seqno: int = 0
    routes: list[Route] = field(default_factory=list)
    venues: list[Venue] = field(default_factory=list)
    products: list[Product] = field(default_factory=list)
    markets: list[Market] = field(default_factory=list)
