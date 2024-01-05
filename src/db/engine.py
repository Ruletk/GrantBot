from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.injector.injector import injector
from src.settings import DATABASE_URL


def init_engine():
    if injector.get("engine"):
        return
    engine = create_async_engine(url=DATABASE_URL)
    injector.register(engine, "engine")


def init_session():
    if injector.get("session"):
        return
    session = async_sessionmaker(
        injector.get("engine"), expire_on_commit=False, class_=AsyncSession
    )
    injector.register(session, "session")


def initialize():
    init_engine()
    init_session()
