import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True
    JSON_ARGUMENTS = ()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(
        DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now()
    )
    deleted_at = Column(DateTime, default=None)

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
