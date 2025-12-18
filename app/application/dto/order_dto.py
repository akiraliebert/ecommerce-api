from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from typing import List
from datetime import datetime

from app.domain.entities.order import OrderStatus


@dataclass
class CreateOrderDTO:
    user_id: UUID


@dataclass
class OrderItemDTO:
    product_id: UUID
    quantity: int
    price: Decimal


@dataclass
class OrderDTO:
    id: UUID
    user_id: UUID
    items: List[OrderItemDTO]
    total: Decimal
    status: OrderStatus
    created_at: datetime



@dataclass(frozen=True)
class PlaceOrderDTO:
    user_id: UUID
