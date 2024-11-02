import asyncio

from client.deribit_client import DeribitClient, Currency
from db.dao.price_history import PriceHistoryDao

async def main( ):
    async with DeribitClient() as client:
        btc_index = await client.get_index_price(Currency.BTC)
        eth_index = await client.get_index_price(Currency.ETH)

        dao = PriceHistoryDao()
        await dao.add()
        


if __name__ == "__main__":
    asyncio.run(main())