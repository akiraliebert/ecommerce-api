from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from typing import List
from datetime import datetime

from app.domain.entities.order import OrderStatus, Order


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

    @staticmethod
    def from_domain(order: Order):
        return OrderDTO(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            created_at=order.created_at,
            items=[
                OrderItemDTO(
                    product_id=i.product_id,
                    quantity=i.quantity,
                    price=i.price
                )
                for i in order.items
            ],
            total=order.total_amount()
        )




@dataclass(frozen=True)
class PlaceOrderDTO:
    user_id: UUID
