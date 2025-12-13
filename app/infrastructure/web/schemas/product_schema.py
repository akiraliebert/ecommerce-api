from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    quantity: int
