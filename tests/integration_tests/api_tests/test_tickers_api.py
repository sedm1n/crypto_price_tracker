import pytest

from httpx import AsyncClient


@pytest.mark.parametrize(
        "status_code,expected", 
        [(200,True), ]
        )
async def test_get_tickers(status_code: int, expected: bool, async_client: AsyncClient):
    
    response = await async_client.get(f"/api/tickers/")
    
    assert response.status_code == status_code
    assert response.json() == expected
    
