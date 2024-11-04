from src.core.exeptions import TickerNotFoundError
from src.db.models.ticker import Ticker
from src.db.dao.base import BaseDao

class TickerDao(BaseDao):
    model = Ticker

    async def get_by_ticker(self, **filter_by) -> Ticker:
        
        if filter_by:
            ticker = await TickerDao.find_one_or_none(**filter_by)

        if not ticker:
            raise TickerNotFoundError(
                f"Ticker {ticker} not found"
            )

        return ticker