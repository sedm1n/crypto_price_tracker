import asyncio

from client.deribit_client import Currency, DeribitClient
from db.dao.ticker import TickerDao
from services.collector.price_history import periodic_price_fetch


async def main():
    async with DeribitClient() as client:

        ticker_dao = TickerDao()

        tickers = await ticker_dao.get_all()

        if not tickers:
            logger.error("Tickers not found")
            raise ValueError("Tickers not found")

        await periodic_price_fetch(client, tickers, interval=60)


if __name__ == "__main__":
    asyncio.run(main())
