from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TimeStampedModel(Base):
    __abstract__ = True  # can't create table itself,share among multiple models

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=datetime.now(timezone.utc))


# class User(TimeStampedModel):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(80), nullable=False)
#     last_name = Column(String(80), nullable=False)
