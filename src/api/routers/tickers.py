from fastapi import APIRouter, HTTPException, status, Depends

from src.api.schemas.tikcker import TickerSchema
from src.db.dao.ticker import TickerDao


router = APIRouter(prefix="/api/tickers", tags=["tickers"])


@router.get("/")
async def get_tickers():
    tickers = await TickerDao().get_all()
    if not tickers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tickers not found")
    
    return tickers

@router.post("/add_ticker", status_code=status.HTTP_201_CREATED)
async def add_ticker(ticker:TickerSchema):
    exist_ticker = await TickerDao.find_one_or_none(name=ticker.name)
    
    if exist_ticker:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticker already exists")
    await TickerDao().add(name=ticker.name)
    
    
    return {"message": f"Ticker {ticker.name} added"}

@router.post("/delete")
async def delete_ticker(ticker:TickerSchema):
    exist_ticker = await TickerDao.find_one_or_none(name=ticker.name)
    print(ticker)
    
    if not exist_ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    
    await TickerDao().delete(exist_ticker.id)
    
    return {"message": f"Ticker {ticker.name} deleted"}

