from dataclasses import dataclass
from uuid import UUID
from typing import List


@dataclass
class CartItemDTO:
    product_id: UUID
    quantity: int


@dataclass
class CartDTO:
    id: UUID
    user_id: UUID
    items: List[CartItemDTO]
