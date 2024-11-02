from datetime import datetime
from typing import List, Optional

from sqlalchemy import (BigInteger, Column, ForeignKey, Integer, Numeric,
                        String, UniqueConstraint)
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


