import pytest

from httpx import AsyncClient


@pytest.mark.parametrize(
    "status_code,expected",
    [
        (200, True),
    ],
)
async def test_get_tickers(status_code: int, expected: bool, async_client: AsyncClient):

    response = await async_client.get(f"/api/tickers/")

    assert response.status_code == status_code
    assert response.json()


@pytest.mark.parametrize(
    "name, status_code, expected",
    [
        ("btc_aux", 201, True),
        ("btc_aux", 409, False),
        ("", 422, False),
        ("  ", 422, False),
    ],
)
async def test_add_ticker(
    name: str, status_code: int, expected: bool, async_client: AsyncClient
):

    response = await async_client.post(f"/api/tickers/add_ticker", json={"name": name})
    assert response.status_code == status_code
    if expected:
        assert response.json() == {"message": f"Ticker {name} added"}
     
