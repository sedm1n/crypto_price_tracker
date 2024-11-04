from datetime import datetime
from typing import List, Optional

from sqlalchemy import (BigInteger, Column, ForeignKey, Integer, Numeric,
                        String, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tickers.id", ondelete="CASCADE"),
        nullable=False,
    )
    price: Mapped[Numeric] = mapped_column(
        Numeric(precision=18, scale=8), nullable=False
    )

    created_at: Mapped[int] = mapped_column(
        BigInteger, default=lambda: int(datetime.now().timestamp())
    )

    ticker: Mapped["Ticker"] = relationship("Ticker", back_populates="price_history")

    def __repr__(self) -> str:
        return f"PriceHistory(id={self.id}, Ticker_id={self.Ticker_id}, price={self.price}, timestamp={self.created_at})"
