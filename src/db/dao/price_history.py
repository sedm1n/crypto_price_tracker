from datetime import datetime
from typing import List, Optional
from src.db.dao.ticker import TickerDao
from src.db.models.price_history import PriceHistory
from src.db.dao.base import BaseDao
from src.core.exeptions import TickerNotFoundError, PricesNotFoundError


def get_unix_timestamp(date_str: str) -> int:
    
    dt = datetime.strptime(date_str, "%d-%m-%Y")  
    
    return int(dt.timestamp())

class PriceHistoryDao(BaseDao):
    model = PriceHistory

    async def get_all_by_ticker(self, ticker: str) -> List[PriceHistory]:

        ticker = await TickerDao().get_by_ticker(name=ticker)

        prices = await PriceHistoryDao().get_all(ticker_id=ticker.id)

        if not prices:

            raise PricesNotFoundError("Prices not found")

        return prices

    async def get_latest_by_ticker(self, ticker: str) -> Optional[PriceHistory]:

        ticker = await TickerDao().get_by_ticker(name=ticker)

        prices = await PriceHistoryDao().get_all(ticker_id=ticker.id)

        if not prices:
            raise PricesNotFoundError("Prices not found")
        sorted_prices = sorted(prices, key=lambda price: price.created_at, reverse=True)

        return sorted_prices[0]
    async def get_by_ticker_and_date(self, ticker: str, start_date: str, end_date: str) -> Optional[PriceHistory]:

        ticker = await TickerDao().get_by_ticker(name=ticker)

        if not ticker:
            raise TickerNotFoundError(f"Ticker {ticker} not found")

        start_timestamp = get_unix_timestamp(start_date)
        end_timestamp = get_unix_timestamp(end_date)

        prices = await PriceHistoryDao().get_all(ticker_id=ticker.id, created_at__gte=start_timestamp, created_at__lte=end_timestamp)
        

        if not prices:
            raise PricesNotFoundError("Prices not found")

        
        return prices