import pytest

from httpx import AsyncClient

@pytest.mark.parametrize("ticker_name","statuc_code","expected", [("btc_usd",200,True), ("eth_usd",404,False)])
async def test_get_ticker(ticker_name: str, status_code: int, expected: bool, asycn_client: AsyncClient):
    
    response = await asycn_client.get(f"/api/tickers/{ticker_name}")
    assert response.status_code == status_code
    assert response.json() == expected