import datetime
import logging

import fastapi

from data_gatherers.fetcher import PriceFetcher
from data_gatherers.parsers.binance import BinanceParser
from data_gatherers.parsers.bybit import BybitParser
from data_gatherers.use_case import get_all_prices, get_one_price
from db.connection import get_connection
from models import AggregatedPrices, Symbol

logging.basicConfig(level=logging.DEBUG)

FETCHERS = (
    PriceFetcher(url='https://api.binance.com/api/v3/ticker/price', parser=BinanceParser()),
    PriceFetcher('https://api.bybit.com/v2/public/tickers', parser=BybitParser()),
)

app = fastapi.FastAPI()


@app.get("/")
async def root_redirect():
    return fastapi.responses.RedirectResponse("/docs")


@app.get("/api/prices/")
async def prices() -> list[AggregatedPrices]:
    return await get_all_prices(fetchers=FETCHERS)


@app.get("/api/prices/{coin_name}")
async def one_symbol_prices(coin_name: Symbol) -> AggregatedPrices:
    return await get_one_price(fetchers=FETCHERS, symbol=coin_name)


@app.get("/api/db")
async def db() -> str:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT NOW();')
        res: datetime.datetime = cur.fetchone()[0]
        logging.debug(res)
        return 'data base time is ' + res.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level=logging.DEBUG)
