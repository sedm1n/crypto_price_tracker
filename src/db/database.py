from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import cfg


class Base(DeclarativeBase):
    pass


engine = create_async_engine(cfg.get_db_url())
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
