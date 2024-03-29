from data_gatherers.use_case import get_all_prices
from main import FETCHERS


async def test_get_all_prices() -> None:
    """Smoke test for get_all_prices"""
    await get_all_prices(FETCHERS)