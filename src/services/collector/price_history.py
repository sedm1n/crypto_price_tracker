import asyncio
import logging
from typing import Dict, List
from db.dao.price_history import PriceHistoryDao
from db.dao.ticker import TickerDao
from client.deribit_client import DeribitClient
from db.models.ticker import Ticker

logging.basicConfig(
    level=logging.DEBUG,)
logger = logging.getLogger(__name__)


async def fetch_prices(client: DeribitClient, tickers: List[dict]) -> List[dict]:
    """Получение цен с биржи для списка валют"""
    prices = []
    for ticker in tickers:
        try:
            price = await client.get_index_price(ticker.name)
            prices.append({"currency": ticker.name, "price": price})

            logger.info(f"Price for {ticker.name}: {price}")
        except Exception as e:
            logger.error(f"Error fetching price for {ticker.name}: {str(e)}")
    return prices


async def save_to_db(prices: List[Dict[Ticker, float]]):
    
    price_dao = PriceHistoryDao()
    tikcer_dao = TickerDao()

    for price_data in prices:
        
        ticker = await tikcer_dao.find_one_or_none(name=price_data["currency"])
        if not ticker:
            logger.error("Ticker %s not found", price_data["currency"])

            raise ValueError(f"Ticker {price_data['currency']} not found")
        try:
            await price_dao.add(ticker_id=ticker.id, price=price_data["price"])
            logger.info("Saved price for %s: %.2f", ticker, price_data['price'])
        except Exception as e:
            logger.exception("Error saving price to database", exc_info=e)


async def periodic_price_fetch(
    client: DeribitClient, tickers: List[Ticker], interval: int = 60
):
    
    save_tasks = []

    while True:
        try:
            prices = await fetch_prices(client, tickers)
            save_task = asyncio.create_task(save_to_db(prices))
            save_tasks.append(save_task)

            save_tasks = [t for t in save_tasks if not t.done()]

            if len(save_tasks) >= 10:
                await asyncio.wait(save_tasks[:5])

            await asyncio.sleep(interval)

        except Exception as e:
            logger.exception("Error in periodic fetch with queue:", exc_info=e)
            await asyncio.sleep(5)
