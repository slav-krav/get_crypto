from typing import Type

import pytest

from data_gatherers.fetcher import PriceFetcher
from data_gatherers.parsers.abstract import AbstractParser
from data_gatherers.parsers.binance import BinanceParser
from data_gatherers.parsers.bybit import BybitParser
from models import AllPrices


@pytest.mark.parametrize('parser_type, url', [
    [BybitParser, 'https://api.bybit.com/v2/public/tickers'],
    [BinanceParser, 'https://api.binance.com/api/v3/ticker/price']
])
async def test_bybit_fetch(parser_type: Type[AbstractParser], url: str):
    """smoke test to fetch and see if type is OK and data is there"""
    parser = parser_type()
    fetcher = PriceFetcher(url=url, parser=parser)
    all_prices = await fetcher.fetch_prices()
    assert isinstance(all_prices, AllPrices)  # pydantic did validation
    assert all_prices.prices  # not empty
