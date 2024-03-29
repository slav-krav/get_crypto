import abc

from models import AllPrices, Price


class AbstractParser(abc.ABC):
    @abc.abstractmethod
    def parse_response(self, data: dict or None) -> AllPrices:
        """Parse response and return all prices consolidated."""

    @abc.abstractmethod
    def parse_price(self, item: dict) -> Price or None:
        """Parse a single price from raw data dict."""
