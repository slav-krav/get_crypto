import logging

import pydantic

from data_gatherers.parsers.abstract import AbstractParser
from models import PlatformPrices, Price


class BybitParser(AbstractParser):
    PLATFORM = 'bybit'

    def parse_response(self, data: dict or None) -> PlatformPrices:
        if data is None:
            return PlatformPrices.get_empty()

        try:
            all_prices_raw = data['result']
            all_prices = {}
            for price in all_prices_raw:
                price = self.parse_price(price)
                if price is not None:
                    all_prices[price.symbol] = price
            return PlatformPrices(prices=all_prices, platform=self.PLATFORM)
        except KeyError:
            logging.error(f'Unable to parse data from {self.PLATFORM}. Wrong format? Raw data:\n{data}')
            return PlatformPrices.get_empty()

    def parse_price(self, item: dict) -> Price or None:
        try:
            return Price(symbol=item['symbol'], value=item['last_price'])
        except (KeyError, pydantic.ValidationError):
            logging.error(f'[{self.PLATFORM}] | Unable to construct Price for item {item}')
