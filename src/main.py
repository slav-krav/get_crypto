from data_gatherers.parsers.binance import BinanceParser
from data_gatherers.parsers.bybit import BybitParser
from data_gatherers.fetcher import PriceFetcher

FETCHERS = (
    PriceFetcher(url='https://api.binance.com/api/v3/ticker/price', parser=BinanceParser()),
    PriceFetcher('https://api.bybit.com/v2/public/tickers', parser=BybitParser()),
)


