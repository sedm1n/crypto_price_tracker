import asyncio
import logging
from typing import Dict, List
from db.dao.price_history import PriceHistoryDao
from db.dao.ticker import TickerDao
from client.deribit_client import DeribitClient
from db.models.ticker import Ticker

logging.basicConfig(level=logging.DEBUG, )
logger = logging.getLogger(__name__)


async def fetch_prices(client: DeribitClient, currencies: List[Ticker]) -> List[dict]:
    """Получение цен с биржи для списка валют"""
    prices = []
    for currency in currencies:
        try:
            price = await client.get_index_price(currency.name)
            prices.append({"currency": currency.name, "price": price})

            logger.info(f"Price for {currency}: {price}")
        except Exception as e:
            logger.error(f"Error fetching price for {currency}: {str(e)}")
    return prices


async def save_to_db(prices: List[Dict[Ticker, float]]):
    price_dao = PriceHistoryDao()
    tikcer_dao = TickerDao()
   

    for price_data in prices:
        print(price_data)
        ticker = await tikcer_dao.find_one_or_none(name=price_data['currency'])
        if not ticker:
            logger.error("Ticker %s not found", price_data['currency'])

            raise ValueError(f"Ticker {price_data['currency']} not found")
        try:
            await price_dao.add(ticker_id=ticker.id, price=price_data['price'])
            logger.info(f"Saved price for {ticker}: {price_data['price']}")
        except Exception as e:
            logger.exception("Error saving price to database", exc_info=e)
        


    

async def periodic_price_fetch_with_queue(client: DeribitClient, currencies: List[Ticker], interval: int = 60):
    """Организация очереди задач для контроля количества сохранений"""
    save_tasks = []
    
    while True:
        try:
            prices = await fetch_prices(client, currencies)
            save_task = asyncio.create_task(save_to_db(prices))
            save_tasks.append(save_task)
            
            # Удаляем завершённые задачи, чтобы не накапливать завершенные объекты
            save_tasks = [t for t in save_tasks if not t.done()]
            
            # Ограничение на количество задач
            if len(save_tasks) >= 10:
                await asyncio.wait(save_tasks[:5])  # Дожидаемся завершения первых пяти задач

            await asyncio.sleep(interval)
            
        except Exception as e:
            logger.error(f"Error in periodic fetch with queue: {str(e)}")
            await asyncio.sleep(5)

