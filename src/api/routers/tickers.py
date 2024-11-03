from fastapi import APIRouter, HTTPException, status, Depends

from api.schemas.tikcker import TickerSchema
from db.dao.ticker import TickerDao


router = APIRouter(prefix="/api/tickers", tags=["tickers"])


@router.get("/")
async def get_tickers():
    tickers = await TickerDao().get_all()
    if not tickers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tickers not found")
    
    return tickers

@router.post("/{ticker}")
async def add_ticker(ticker:TickerSchema):
    exist_ticker = await TickerDao.find_one_or_none(name=ticker.name)
    if exist_ticker:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticker already exists")
    await TickerDao().add(name=ticker.name)
    return {"message": f"Ticker {ticker.name} added"}

@router.delete("/{ticker}")
async def delete_ticker(ticker:str):
    exist_ticker = await TickerDao.find_one_or_none(name=ticker)
    if not exist_ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    await TickerDao().delete(name=ticker)
    return {"message": f"Ticker {ticker} deleted"}

