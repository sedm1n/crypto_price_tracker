import asyncio

from client.deribit_client import DeribitClient, Currency
from db.dao.price_history import PriceHistoryDao
from db.dao.ticker import TickerDao
from services.collector.price_history import periodic_price_fetch_with_queue

async def main( ):
    async with DeribitClient() as client:

        ticker_dao = TickerDao()
        price_history_dao = PriceHistoryDao()

        tickers = await ticker_dao.get_all()
        print(tickers)
        await periodic_price_fetch_with_queue(client,tickers, interval=60 )


if __name__ == "__main__":
    asyncio.run(main())