import uvicorn
import logging.config
from fastapi import FastAPI

from api.routers import price_history, tickers
from core.logging_config import logging_config


logging.config.dictConfig(logging_config)

app = FastAPI()


app.include_router(price_history.router)
app.include_router(tickers.router)



if __name__ == "__main__":  
    uvicorn.run(app, host="localhost", port=8000)
