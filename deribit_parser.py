import asyncio
import logging.config

from client.deribit_client import DeribitClient
from core.logging_config import logging_config
from db.dao.ticker import TickerDao
from services.collector.price_history import periodic_price_fetch

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)


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
