import abc

from models import PlatformPrices, Price, Platform


class AbstractParser(abc.ABC):
    PLATFORM: Platform

    @abc.abstractmethod
    def parse_response(self, data: dict or None) -> PlatformPrices:
        """Parse response and return all prices consolidated."""

    @abc.abstractmethod
    def parse_price(self, item: dict) -> Price or None:
        """Parse a single price from raw data dict."""
