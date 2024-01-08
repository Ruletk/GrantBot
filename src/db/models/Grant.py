from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db.models.Base import ModelBase
from src.db.models.User import User


class Grant(ModelBase):
    __tablename__ = "grants"
    JSON_ARGUMENTS = ("iin", "ikt", "year", "type", "last_request", "is_active")

    ikt: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # 1=ENT/KT, 2=Mag/Doct, 3=NKT
    iin: Mapped[str] = mapped_column(String, nullable=False)
    last_request: Mapped[Optional[dict]] = mapped_column(JSON(False))
    is_active: Mapped[int] = mapped_column(Integer, default=1)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="grants")  # noqa F821

    def __repr__(self):
        return (
            f"<Grant("
            f"id={self.id}, "
            f"iin={self.iin}, "
            f"ikt={self.ikt}, "
            f"year={self.year}, "
            f"type={self.type}, "
            f"user={self.user_id})>"
        )

    def __str__(self):
        return (
            f"<Grant(id={self.id}, ikt={'*' * 6}{self.ikt[-3:]}, user={self.user_id})"
        )
