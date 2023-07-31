from sqlalchemy.ext.asyncio import create_async_engine
from src.settings import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)
