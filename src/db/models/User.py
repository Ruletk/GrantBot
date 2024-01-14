from typing import List

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.models.Base import ModelBase


class User(ModelBase):
    __tablename__ = "users"
    JSON_ARGUMENTS = ("id", "telegram_id", "language", "grants")

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger, primary_key=True, index=True
    )
    chat_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(2), default="ru")
    policy_confirm: Mapped[bool] = mapped_column(Boolean, default=False)

    grants: Mapped[List["Grant"]] = relationship(back_populates="user")  # noqa F821

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, language={self.language})>"

    def __str__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, language={self.language})>"
