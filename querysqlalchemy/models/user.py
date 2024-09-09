from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from querysqlalchemy.models.base import TimeStampedModel, Base


class User(TimeStampedModel, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(320), unique=True, nullable=True)
    father_name = Column(String(80))
    phone = Column(String(11))

    address = relationship(
        "Address", back_populates="user", passive_deletes=True, uselist=False
    )

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship(
        "Role", back_populates="users", uselist=False
    )  # Indicates one-to-one


class Address(TimeStampedModel):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    postcode = Column(String(80), nullable=True)
    city = Column(String(80), nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True
    )

    user = relationship("User", back_populates="address")


class Role(TimeStampedModel, Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(80), nullable=False)
    # one to many, one role have many users
    users = relationship("User", back_populates="role")
