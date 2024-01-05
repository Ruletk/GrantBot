from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON

from src.db.models.Base import ModelBase


class User(ModelBase):
    __tablename__ = "users"
    JSON_ARGUMENTS = ("telegram_id", "iin", "ikt", "year", "type")

    telegram_id = Column(Integer, unique=True, nullable=False)
    iin = Column(String)
    ikt = Column(String)
    year = Column(Integer)
    type = Column(Integer)  # 1=ENT/KT, 2=Mag/Doct, 3=NKT
    language = Column(String(2), default="ru")
    last_request = Column(JSON(False))
    policy_confirm = Column(Boolean, default=False)
