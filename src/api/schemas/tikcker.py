from pydantic import BaseModel


class TickerSchema(BaseModel):
    id: int
    name: str