from typing import Optional

from annotated_types import Len
from pydantic import BaseModel, Field
from typing_extensions import Annotated

Symbol = Annotated[str, Len(min_length=1)]  # currency name
Platform = Annotated[str, Len(min_length=1)]  # platform name


class Price(BaseModel):
    value: str
    symbol: str

    @property
    def float_value(self) -> float:
        """Could be some proper logic on how to get a floating point price.
        Do not want to mess with mantissa now...
        """
        return float(self.value)


class PlatformPrices(BaseModel):
    """All prices across a platform"""
    prices: dict[Symbol, Price]
    platform: Platform

    @classmethod
    def get_empty(cls):
        return cls(prices={})



_aggregated_prices_example = """
{
  "binance": "50.05000000",
  "bybit": "50.05"
}
"""
class AggregatedPrices(BaseModel):
    """Prices for a currency from different platforms."""
    name: Symbol = Field(example='KSMUSDT')
    prices: dict[Platform, Optional[str]] = Field(example=_aggregated_prices_example)
