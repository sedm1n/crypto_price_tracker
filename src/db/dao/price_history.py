
from typing import List
from src.db.models.price_history import PriceHistory
from src.db.dao.base import BaseDao


class PriceHistoryDao(BaseDao):
    model = PriceHistory
    
