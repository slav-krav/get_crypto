from data_gatherers.gatherer import DataGatherer
from data_gatherers.parsers.bybit import BybitParser
from models import AllPrices


async def test_bybit_fetch():
    """smoke test to fetch and see if type is OK and data is there"""
    bybit_parser = BybitParser()
    gatherer = DataGatherer(url='https://api.bybit.com/v2/public/tickers', parser=bybit_parser)
    all_prices = await gatherer.fetch_prices()
    assert isinstance(all_prices, AllPrices)  # pydantic did validation
    assert all_prices.prices  # not empty
