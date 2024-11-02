
from typing import List
from db.models.price_history import PriceHistory
from db.dao.base import BaseDao


class PriceHistoryDao(BaseDao):
    model = PriceHistory
    
