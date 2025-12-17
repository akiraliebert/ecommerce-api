from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List


@dataclass
class CartItem:
    product_id: UUID
    quantity: int

    def increase(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.quantity += amount

    def decrease(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.quantity - amount < 1:
            raise ValueError("Cart item quantity cannot be less than 1")
        self.quantity -= amount


@dataclass
class Cart:
    id: UUID
    user_id: UUID
    items: List[CartItem] = field(default_factory=list)

    @staticmethod
    def create(user_id: UUID) -> "Cart":
        return Cart(
            id=uuid4(),
            user_id=user_id,
            items=[]
        )

    def add_item(self, product_id: UUID, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        for item in self.items:
            if item.product_id == product_id:
                item.increase(quantity)
                return

        self.items.append(
            CartItem(
                product_id=product_id,
                quantity=quantity
            )
        )

    def update_item(self, product_id: UUID, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        for item in self.items:
            if item.product_id == product_id:
                item.quantity = quantity
                return

        raise ValueError("Product not found in cart")

    def remove_item(self, product_id: UUID):
        for item in self.items:
            if item.product_id == product_id:
                self.items.remove(item)
                return

        raise ValueError("Product not found in cart")

    def clear(self):
        self.items.clear()
