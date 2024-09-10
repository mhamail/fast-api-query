from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, FieldValidationInfo


class AuthBase(BaseModel):
    username: str = Field(min_length=3)
    email: Optional[str] = Field(EmailStr)
    password: str


class Login(BaseModel):
    email: str
    password: str


class AuthUserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True
