from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Product:
    id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    quantity: int

    def reserve(self, amount: int):
        """Резервирование товара перед оплатой"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > self.quantity:
            raise ValueError("Not enough product in stock")

        self.quantity -= amount

    def release(self, amount: int):
        """Вернуть резерв (в случае отмены)"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.quantity += amount

    @staticmethod
    def create(name: str, price: Decimal, quantity: int, description: Optional[str] = None) -> "Product":
        if price <= Decimal("0"):
            raise ValueError("Price must be positive")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        return Product(
            id=uuid4(),
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )

