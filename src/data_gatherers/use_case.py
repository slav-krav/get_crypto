import asyncio
from typing import Sequence

from data_gatherers.fetcher import PriceFetcher
from models import AggregatedPrices, PlatformPrices

__all__ = ['get_all_prices', 'get_one_price']


async def get_all_prices(fetchers: Sequence[PriceFetcher]) -> list[AggregatedPrices]:
    all_platforms = await asyncio.gather(
        *[fetcher.fetch_prices() for fetcher in fetchers],
        return_exceptions=True
    )

    return _group_by_symbol(all_platforms)


def _group_by_symbol(platform_prices_seq: Sequence[PlatformPrices]) -> list[AggregatedPrices]:
    result = []

    all_symbols = _get_unique_symbols(platform_prices_seq)
    for symbol in all_symbols:
        prices = {}
        for platform_prices in platform_prices_seq:
            try:
                price = platform_prices.prices[symbol].float_value
            except KeyError:
                price = None
            prices[platform_prices.platform] = price
        result.append(AggregatedPrices(name=symbol, prices=prices))
    return result


def _get_unique_symbols(platform_prices_seq: Sequence[PlatformPrices]) -> set[str]:
    unique_symbols = set()
    for platform_prices in platform_prices_seq:
        unique_symbols.update(platform_prices.prices)
    return unique_symbols


async def get_one_price(symbol: str) -> AggregatedPrices:
    ...