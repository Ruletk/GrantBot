from typing import Generator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.settings import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_db() -> Generator:
    async with async_session() as session:
        yield session
