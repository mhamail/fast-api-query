from querysqlalchemy.models.base import TimeStampedModel, Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class AuthUser(TimeStampedModel, Base):
    __tablename__ = "authusers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False)
    email = Column(String(320), unique=True, nullable=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
