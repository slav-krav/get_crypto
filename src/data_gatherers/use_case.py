import asyncio
import logging
from typing import Iterable

from data_gatherers.fetcher import PriceFetcher
from models import AggregatedPrices, PlatformPrices

__all__ = ['get_all_prices', 'get_one_price']


async def get_all_prices(fetchers: Iterable[PriceFetcher]) -> list[AggregatedPrices]:
    all_platforms = await _fetch_platform_prices(fetchers)
    return _group_by_symbol(all_platforms)


def _group_by_symbol(platform_prices_seq: Iterable[PlatformPrices]) -> list[AggregatedPrices]:
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


def _get_unique_symbols(platform_prices_seq: Iterable[PlatformPrices]) -> set[str]:
    unique_symbols = set()
    for platform_prices in platform_prices_seq:
        unique_symbols.update(platform_prices.prices)
    return unique_symbols


async def _fetch_platform_prices(fetchers: Iterable[PriceFetcher]) -> tuple[PlatformPrices, ...]:
    all_platforms: tuple[PlatformPrices or Exception, ...] = await asyncio.gather(
        *[fetcher.fetch_prices() for fetcher in fetchers],
        return_exceptions=True
    )
    if any(isinstance(result, Exception) for result in all_platforms):
        logging.critical('ONE OR MORE FETCHING FAILED AND EXCEPTION WAS NOT HANDLED. FINAL RESULT WILL HAVE LESS DATA.')
        all_platforms = tuple(result for result in all_platforms if not isinstance(result, Exception))
    return all_platforms


async def get_one_price(fetchers: Iterable[PriceFetcher], symbol: str) -> AggregatedPrices:
    """Gets AggregatedPrices for a single symbol.

    Note:
        probably there are better ways to get data for a single price per platform.
        But we will fetch all prices and filter out anything else besides our symbol.
    """
    all_platforms = await _fetch_platform_prices(fetchers)
    prices = {}
    for platform_prices in all_platforms:
        try:
            price = platform_prices.prices[symbol].float_value
        except KeyError:
            price = None
        prices[platform_prices.platform] = price

    return AggregatedPrices(name=symbol, prices=prices)
