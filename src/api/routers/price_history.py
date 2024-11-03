from fastapi import APIRouter, HTTPException, status, Depends

from api.schemas.price_history import PriceHistoryResponseSchema
from db.dao.price_history import PriceHistoryDao
from db.dao.ticker import TickerDao


router = APIRouter(prefix="/api/price_history", tags=["price_history"])


@router.get("/")
async def get_price_history_all()->list[PriceHistoryResponseSchema]:
    prices = await PriceHistoryDao().get_all()
    if not prices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prices not found")
    
    return prices

@router.get("/{ticker}")
async def get_price_history(ticker: str)->list[PriceHistoryResponseSchema]:
    exist_ticker = await TickerDao.find_by_id(ticker)
    if not exist_ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    
    prices = await PriceHistoryDao().get_all(tiker_id=exist_ticker.id)

    if not prices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prices not found")
    
    return prices


 