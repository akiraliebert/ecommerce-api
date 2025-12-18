from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List

from app.domain.entities.order import OrderStatus


class OrderItemResponse(BaseModel):
    product_id: UUID
    quantity: int
    price: Decimal


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: OrderStatus
    created_at: datetime
    total: Decimal
    items: List[OrderItemResponse]
