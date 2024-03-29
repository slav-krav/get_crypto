from typing import Optional

from annotated_types import Len
from typing_extensions import Annotated
from pydantic import BaseModel

Symbol = Annotated[str, Len(min_length=1)]  # currency name
Platform = Annotated[str, Len(min_length=1)]  # platform name


class Price(BaseModel):
    value: str
    symbol: str

    @property
    def float_value(self) -> float:
        """Could be some additional logic on how to get a floating point price"""
        return float(self.value)


class PlatformPrices(BaseModel):
    """All prices across a platform"""
    prices: dict[Symbol, Price]
    platform: Platform

    @classmethod
    def get_empty(cls):
        return cls(prices={})


class AggregatedPrices(BaseModel):
    """Prices for a currency from different platforms."""
    name: Symbol
    prices: dict[Platform, Optional[float]]
