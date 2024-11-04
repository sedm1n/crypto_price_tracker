import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.core.exeptions import PricesNotFoundError, TickerNotFoundError
from src.db.dao.base import BaseDao
from src.db.dao.ticker import TickerDao
from src.db.database import get_async_session
from src.db.models.price_history import PriceHistory

logger = logging.getLogger(__name__)


def get_unix_timestamp(date_str: str) -> int:

    dt = datetime.strptime(date_str, "%d-%m-%Y")

    return int(dt.timestamp())


class PriceHistoryDao(BaseDao):
    model = PriceHistory

    @classmethod
    async def get_all(
        cls,
        ticker_id: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
        **filter_by,
    ):
        async with get_async_session() as session:

            query = select(cls.model).filter_by(**filter_by)
            if ticker_id:
                query = query.filter(cls.model.ticker_id == ticker_id)

            if start_timestamp and end_timestamp:
                query = query.filter(
                    cls.model.created_at >= start_timestamp, cls.model.created_at < end_timestamp
                )
            try:
                result = await session.execute(query)
                return result.scalars().all()
            except SQLAlchemyError as e:
                logger.error(e, extra={"filter": filter_by}, exc_info=True)
                return None

    async def get_all_by_ticker(self, ticker: str) -> list[PriceHistory]:

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

    async def get_by_ticker_and_date(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[PriceHistory]:

        ticker = await TickerDao().get_by_ticker(name=ticker)

        if not ticker:
            raise TickerNotFoundError(f"Ticker {ticker} not found")

        start_timestamp = get_unix_timestamp(start_date)
        end_timestamp = get_unix_timestamp(end_date)

        prices = await self.get_all(
            ticker_id=ticker.id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

        if not prices:
            raise PricesNotFoundError("Prices not found")

        return prices
