import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.db.database import Base, async_session, engine
from src.db.models.ticker import Ticker
from src.db.models.price_history import PriceHistory
from src.core.config import cfg
from app import app

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
      assert cfg.MODE == "TEST"

      async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
      
      def open_mock_json(model:str):
            with open(f"tests/fixtures/mock_{model}.json") as f:
                  
                  return json.load(f)
            
      
      tickers = open_mock_json("tickers")
      price_history = open_mock_json("price_history")
      

      async with async_session() as session:
            async with session.begin():
                  
                  add_tickers = insert(Ticker).values(tickers)
                  add_price_history = insert(PriceHistory).values(price_history)

                  for query in [add_tickers, add_price_history, ]:
                        await session.execute(query)

                  await session.commit()



@pytest.fixture(scope="session")
def event_loop(request):
      """ Create an instance of the default event loop for each test case """
      loop = asyncio.get_event_loop_policy().new_event_loop()
      yield loop
      loop.close()


@pytest.fixture(scope="function")
async def async_client():
      async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


