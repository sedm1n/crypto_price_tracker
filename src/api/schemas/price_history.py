from pydantic import BaseModel

class PriceHistorySchema(BaseModel):
    
    ticker_id: int
    price: float
    
class PriceHistoryResponse(PriceHistorySchema):
    id: int
    created_at: int