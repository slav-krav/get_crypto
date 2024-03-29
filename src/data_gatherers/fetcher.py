import logging

import aiohttp

from data_gatherers.parsers.abstract import AbstractParser
from models import PlatformPrices


class PriceFetcher:
    MAX_RETRIES: int = 3

    def __init__(self, url: str, parser: AbstractParser) -> None:
        self.retry_counter = 0
        self.url = url
        self.parser = parser

    async def fetch_prices(self) -> PlatformPrices:
        """Fetch data from endpoint and return parsed data."""
        async with aiohttp.ClientSession() as session:
            data = None
            while self.retry_counter < self.MAX_RETRIES:
                try:
                    data = await self._fetch(session)
                    self.retry_counter = 0
                    break
                except aiohttp.ClientResponseError:
                    self.retry_counter += 1
            if data is None:
                logging.error(f"Unable to get data after retries: [{self.retry_counter}] from [{self.url}]")
            return self.parser.parse_response(data)

    async def _fetch(self, session: aiohttp.ClientSession):
        async with session.get(self.url) as response:
            data = await response.json()
            if response.status != 200:
                logging.error(f'Error fetching data from {self.url} API: {response.status}')
                raise aiohttp.ClientResponseError(response.request_info, (response,))
            return data


