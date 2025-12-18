from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import List


class OrderStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    CANCELED = "canceled"


@dataclass(frozen=True)
class OrderItem:
    product_id: UUID
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


@dataclass
class Order:
    id: UUID
    user_id: UUID
    items: List[OrderItem]
    status: OrderStatus
    created_at: datetime

    @staticmethod
    def create(user_id: UUID, items: List[OrderItem]) -> "Order":
        if not items:
            raise ValueError("Order must contain at least one item")

        return Order(
            id=uuid4(),
            user_id=user_id,
            items=items,
            status=OrderStatus.CREATED,
            created_at=datetime.now(timezone.utc)
        )

    def total_amount(self) -> Decimal:
        # 2 параметр задает тип результата, чтобы избежать ошибок округления
        return sum((item.total() for item in self.items), Decimal("0"))

    def mark_paid(self):
        if self.status != OrderStatus.CREATED:
            raise ValueError("Order cannot be paid")

        self.status = OrderStatus.PAID

    def cancel(self):
        if self.status == OrderStatus.PAID:
            raise ValueError("Paid order cannot be canceled")

        self.status = OrderStatus.CANCELED
