from data_gatherers.use_case import get_all_prices, get_one_price
from main import FETCHERS


async def test_get_all_prices() -> None:
    """Smoke test for get_all_prices"""
    await get_all_prices(FETCHERS)


async def test_get_one_price() -> None:
    """Smoke test for get_one_price"""
    await get_one_price(FETCHERS, 'BTC')
