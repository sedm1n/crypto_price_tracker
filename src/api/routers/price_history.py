import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from src.api.schemas.price_history import PriceHistoryResponseSchema
from src.api.schemas.tikcker import TickerSchema
from src.core.exeptions import PricesNotFoundError, TickerNotFoundError
from src.db.dao.price_history import PriceHistoryDao
from src.db.dao.ticker import TickerDao

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/price_history", tags=["price_history"])


@router.get("/")
async def get_price_history_all(
    ticker: str = Query(...),
) -> list[PriceHistoryResponseSchema]:

    """
    Get a list of prices for a given ticker.

    Args:
    - ticker (str): The ticker symbol

    Returns:
    - list[PriceHistoryResponseSchema]: A list of prices

    Raises:
    - HTTPException: If the ticker is not found
    - HTTPException: If no prices are found for the given ticker
    """
    try:
        prices = await PriceHistoryDao().get_all_by_ticker(ticker)
    except TickerNotFoundError as e:
        logger.error("No prices found for ticker: %s", ticker)
        raise HTTPException(status_code=404, detail=str(e))
    except PricesNotFoundError as e:
        logger.error("No prices found for ticker: %s", ticker)
        raise HTTPException(status_code=404, detail=str(e))

    return prices


@router.get("/latest")
async def get_latest_price(ticker: str = Query(...)) -> PriceHistoryResponseSchema:

    """
    Get the latest price for a given ticker.

    Args:
    - ticker (str): The ticker symbol

    Returns:
    - PriceHistoryResponseSchema: The latest price

    Raises:
    - HTTPException: If the ticker is not found
    """
    try:
        latest_price = await PriceHistoryDao().get_latest_by_ticker(ticker)
    except TickerNotFoundError as e:
        logger.error("No latest price found for ticker: %s", ticker)
        raise HTTPException(status_code=404, detail=str(e))
    except PricesNotFoundError as e:
        logger.error("No latest price found for ticker: %s", ticker)
        raise HTTPException(status_code=404, detail=str(e))

    return latest_price


@router.get("/prices/date")
async def get_price_by_date(
    ticker: str = Query(...),
    start_date: str = Query(...),
    end_date: Optional[str] = Query(None),
) -> list[PriceHistoryResponseSchema]:

    """
    Get a list of prices for a given ticker and date range.

    Args:
    - ticker (str): The ticker symbol
    - start_date (str): The start date in ISO format
    - end_date (Optional[str]): The end date in ISO format (default is None)

    Returns:
    - list[PriceHistoryResponseSchema]: A list of prices

    Raises:
    - HTTPException: If the ticker is not found
    - HTTPException: If no prices are found for the given ticker and date range
    """
    try:
        prices = await PriceHistoryDao().get_by_ticker_and_date(
            ticker, start_date, end_date
        )
    except TickerNotFoundError as e:
        logger.error("No prices found for ticker: %s on date: %s", ticker, start_date)
        raise HTTPException(status_code=404, detail=str(e))
    except PricesNotFoundError as e:
        logger.error("No prices found for ticker: %s on date: %s", ticker, start_date)
        raise HTTPException(status_code=404, detail=str(e))

    return prices
