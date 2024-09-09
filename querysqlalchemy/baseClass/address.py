from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    postcode: str = Field(min_length=2)
    city: str = Field(min_length=3)


class AddressDisplay(BaseModel):
    postcode: str
    city: str

    class Config:
        from_attributes = True
