from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True
    json_arguments = ()

    async def save(self, async_session: AsyncSession) -> None:
        async_session.add(self)
        await async_session.commit()

    async def delete(self, async_session: AsyncSession) -> None:
        async_session.delete(self)
        await async_session.commit()

    async def update(self, async_session: AsyncSession, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await self.save(async_session)

    async def jsonify(self) -> dict:
        return {key: getattr(self, key, None) for key in self.json_attributes}


class User(ModelBase):
    __tablename__ = "users"
    json_arguments = ("telegram_id", "iin", "ikt", "year")

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    iin = Column(String)
    ikt = Column(String)
    year = Column(Integer)
    type = Column(Integer)  # 1=ENT/KT, 2=Mag/Doct, 3=NKT
    language = Column(String(2), default="ru")
    last_request = Column(JSON(False))
