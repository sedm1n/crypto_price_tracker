from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Ticker(Base):
    __tablename__ = "tickers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(120), index=True, nullable=False, unique=True
    )

    created_at: Mapped[int] = mapped_column(
        BigInteger, default=lambda: int(datetime.now().timestamp())
    )

    price_history: Mapped[List["PriceHistory"]] = relationship(
        "PriceHistory", back_populates="ticker", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Ticker(id={self.id}, name={self.name})"


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Tickers.id", ondelete="CASCADE"),
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
