import logging
from typing import Optional

from fastapi import APIRouter, Query, HTTPException, status

from src.api.schemas.tikcker import TickerSchema
from src.core.exeptions import PricesNotFoundError, TickerNotFoundError
from src.api.schemas.price_history import PriceHistoryResponseSchema
from src.db.dao.price_history import PriceHistoryDao
from src.db.dao.ticker import TickerDao

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/price_history", tags=["price_history"])


@router.get("/")
async def get_price_history_all(
    ticker: str = Query(...),
) -> list[PriceHistoryResponseSchema]:

    try:
        prices = await PriceHistoryDao().get_all_by_ticker(ticker)
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PricesNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return prices


@router.get("/latest")
async def get_latest_price(ticker: str = Query(...)) -> PriceHistoryResponseSchema:

    latest_price = await PriceHistoryDao().get_latest_by_ticker(ticker)

    if not latest_price:
        logger.error(f"No latest price found for ticker: {ticker}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Latest price not found"
        )

    return latest_price


@router.get("/prices/date")
async def get_price_by_date(
    ticker: str = Query(...), start_date: str = Query(...), end_date: Optional[str] = Query(None)) -> list[PriceHistoryResponseSchema]:
    prices = await PriceHistoryDao().get_by_ticker_and_date(ticker, start_date, end_date)

    if not prices:
        logger.error(f"No prices found for ticker: {ticker} on date: {start_date}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prices not found for the given date",
        )

    return prices
