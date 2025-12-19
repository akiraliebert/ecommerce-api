from pydantic import BaseModel
from uuid import UUID
from typing import List


class CartItemSchema(BaseModel):
    product_id: UUID
    quantity: int


class CartSchema(BaseModel):
    user_id: UUID
    items: List[CartItemSchema]


class AddCartItemRequest(BaseModel):
    product_id: UUID
    quantity: int


class UpdateCartItemRequest(BaseModel):
    quantity: int
