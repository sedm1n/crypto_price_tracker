from typing import Optional
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "ticker, status_code, expected",
    [
        ("btc_usd", 200, True),
        ("none_ticker", 404, False), 
    ],
)
async def test_get_price_history_all(ticker: str, status_code: int, expected: bool, async_client: AsyncClient):
    response = await async_client.get(f"/api/price_history/?ticker={ticker}")
    assert response.status_code == status_code
    if expected:
        assert isinstance(response.json(), list) 
    else:
        assert response.json() == {"detail": f"Ticker {ticker} not found"} 


@pytest.mark.parametrize(
    "ticker, status_code, expected",
    [
        ("btc_usd", 200, True),  
        ("non_ticker", 404, False), 
    ],
)
async def test_get_latest_price(ticker: str, status_code: int, expected: bool, async_client: AsyncClient):
    response = await async_client.get(f"/api/price_history/latest?ticker={ticker}")
    assert response.status_code == status_code
    if expected:
        assert "price" in response.json()  
    else:
        assert response.json() == {"detail": f"Ticker {ticker} not found"} 


@pytest.mark.parametrize(
    "ticker, start_date, end_date, status_code, expected",
    [
        ("btc_usd", "01-11-2024", "04-11-2024", 200, True), 
        ("btc_usd", "01-11-2024", None, 200, True), 
        ("non_ticker", "01-11-2024", "01-11-2024", 404, False), 
    ],
)
async def test_get_price_by_date(
    ticker: str, start_date: str, end_date: Optional[str], status_code: int, expected: bool, async_client: AsyncClient
):
    params = {"ticker": ticker, "start_date": start_date}
    if end_date:
        params["end_date"] = end_date

    response = await async_client.get("/api/price_history/prices/date", params=params)
    assert response.status_code == status_code
    if expected:
        assert isinstance(response.json(), list) 
    else:
        assert response.json() == {"detail": f"Ticker {ticker} not found"}  
