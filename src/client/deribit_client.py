from typing import Any, Dict, Optional
from aiohttp import ClientSession, ClientError
from enum import Enum


class DeribitClientError(Exception):
    """Базовый класс для ошибок клиента Deribit"""

    pass



class DeribitClient:
    """Асинхронный клиент для работы с Deribit API"""

    BASE_URL = "https://www.deribit.com/api/v2"

    def __init__(self, session: Optional[ClientSession] = None):
        """
        Инициализация клиента

        Args:
            session: Опциональная aiohttp сессия
        """
        self._session = session
        self._own_session = False

    async def __aenter__(self):
        """Контекстный менеджер для создания сессии"""
        if self._session is None:
            self._session = ClientSession()
            self._own_session = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие сессии при выходе из контекстного менеджера"""
        if self._own_session and self._session is not None:
            await self._session.close()

    def _get_index_url(self, ticker: str) -> str:
        """
        Формирование URL для запроса индекса цены

        Args:
            tikcer: тикер , напр btc_usd 

        Returns:
            str: URL для запроса
        """
        return f"{self.BASE_URL}/public/get_index_price?index_name={ticker}"

    async def _make_request(self, url: str) -> Dict[str, Any]:
        """
        Выполнение HTTP запроса

        Args:
            url: URL для запроса

        Returns:
            Dict[str, Any]: Ответ от API

        Raises:
            DeribitClientError: При ошибках запроса
        """
        try:
            async with self._session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise DeribitClientError(
                        f"API request failed with status {response.status}: {error_text}"
                    )

                data = await response.json()
                if not data.get("result"):
                    raise DeribitClientError(f"Invalid API response: {data}")

                return data["result"]

        except ClientError as e:
            raise DeribitClientError(f"Request failed: {str(e)}") from e

    async def get_index_price(self, ticker: str) -> float:
        """
        Получение цены

        Args:
            ticker: Валюта

        Returns:
            float: цена
        """
        url = self._get_index_url(ticker)
        data = await self._make_request(url)

        return float(data["index_price"])

    