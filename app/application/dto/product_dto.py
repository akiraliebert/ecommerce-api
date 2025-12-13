from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal


class CreateProductDTO(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class UpdateProductDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ProductDTO(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    quantity: int
