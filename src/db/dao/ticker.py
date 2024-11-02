from db.models.ticker import Ticker
from db.dao.base import BaseDao

class TickerDao(BaseDao):
    model = Ticker