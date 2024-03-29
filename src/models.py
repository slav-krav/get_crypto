from annotated_types import Len
from typing_extensions import Annotated
from pydantic import BaseModel

Symbol = Annotated[str, Len(min_length=1)]  # currency name


class Price(BaseModel):
    price: str
    symbol: str

    @property
    def float_price(self) -> float:
        """Could be some additional logic on how to get a floating point price"""
        return float(self.price)


class AllPrices(BaseModel):
    prices: dict[Symbol, Price]

    @classmethod
    def get_empty(cls):
        return cls(prices={})
