from fastapi import APIRouter, HTTPException, status, Depends

from db.dao.price_history import PriceHistoryDao


router = APIRouter(prefix="/api/price_history", tags=["price_history"])


@router.get("/")
async def get_price_history_all():
    prices = await PriceHistoryDao().get_all()
    if not prices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prices not found")
    
    return prices