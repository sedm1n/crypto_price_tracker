from db.models.ticker import Ticker
from src.db.dao.base import BaseDao

class TickerDao(BaseDao):
    model = Ticker