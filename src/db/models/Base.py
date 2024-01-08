import datetime
from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class ModelBase(DeclarativeBase):
    __abstract__ = True
    JSON_ARGUMENTS = ()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        insert_default=datetime.datetime.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        insert_default=datetime.datetime.now(), onupdate=datetime.datetime.now()
    )
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def to_json(self):
        """Transforming object to json.
        Keys are taken from JSON_ARGUMENTS tuple."""
        return {key: getattr(self, key) for key in self.JSON_ARGUMENTS}
