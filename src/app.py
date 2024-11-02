import uvicorn
from fastapi import FastAPI

from api.routers import price_history, tickers

app = FastAPI()


app.include_router(price_history.router)




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
