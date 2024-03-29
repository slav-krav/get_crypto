import logging

import pydantic

from data_gatherers.parsers.abstract import AbstractParser
from models import AllPrices, Price


class BybitParser(AbstractParser):
    def parse_response(self, data: dict or None) -> AllPrices:
        if data is None:
            return AllPrices.get_empty()

        try:
            all_prices_raw = data['result']
            all_prices = {}
            for price in all_prices_raw:
                price = self.parse_price(price)
                if price is not None:
                    all_prices[price.symbol] = price
            return AllPrices(prices=all_prices)
        except KeyError:
            logging.error(f'{self.__class__.__name__} is unable to parse data. Wrong format? Raw data:\n{data}')
            return AllPrices.get_empty()

    def parse_price(self, item: dict) -> Price or None:
        try:
            return Price(symbol=item['symbol'], price=item['last_price'])
        except (KeyError, pydantic.ValidationError):
            logging.error(f'Unable to construct Price for item {item}')
