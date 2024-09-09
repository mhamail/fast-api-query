from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, FieldValidationInfo
from typing import List, Optional

from querysqlalchemy.baseClass.role import RoleDisplay

from querysqlalchemy.baseClass.address import AddressBase, AddressDisplay


class UserBase(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    email: Optional[str] = Field(EmailStr)
    father_name: str = Field(min_length=3)
    role_id: int = Field(gt=0)
    phone: Optional[str] = None
    address: Optional[AddressBase] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if v is not None and len(v) < 11:
            raise ValueError("Phone number must be at least 11 characters long")
        return v


class UserCreate(UserBase):
    pass


class UserDisplay(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: Optional[str]
    father_name: Optional[str]
    phone: Optional[str]
    role_id: int
    role: Optional[RoleDisplay]  # Role information is optional
    address: Optional[AddressDisplay]
    created_at: datetime  # Use Optional for fields that can be null
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
