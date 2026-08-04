"""Product request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=50, examples=["바지"])
    price: int = Field(ge=0, examples=[10000])


class ProductUpdate(BaseModel):
    product_name: str = Field(min_length=1, max_length=50, examples=["청바지"])
    price: int = Field(ge=0, examples=[20000])


class ProductPublic(BaseModel):
    id: UUID
    product_name: str
    price: int
    created_at: datetime
    updated_at: datetime
