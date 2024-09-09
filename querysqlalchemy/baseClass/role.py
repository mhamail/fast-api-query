from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class roleBase(BaseModel):
    name: str


class RoleCreate(roleBase):
    pass


class RoleDisplay(BaseModel):
    id: int
    name: str
    created_at: datetime  # Use Optional for fields that can be null
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ResponseRole(BaseModel):
    message: str
    data: RoleDisplay

    class Config:
        from_attributes = True
