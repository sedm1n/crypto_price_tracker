import uvicorn
import logging.config
from fastapi import FastAPI

from src.api.routers import price_history, tickers
from src.core.logging_config import logging_config


logging.config.dictConfig(logging_config)

app = FastAPI()


app.include_router(tickers.router)
app.include_router(price_history.router)



if __name__ == "__main__":  
    uvicorn.run(app, host="localhost", port=8000)
