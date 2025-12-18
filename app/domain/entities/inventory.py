from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class InventoryReservation:
    id: UUID
    product_id: UUID
    quantity: int
    is_active: bool = True

    @staticmethod
    def create(product_id: UUID, quantity: int) -> "InventoryReservation":
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        return InventoryReservation(
            id=uuid4(),
            product_id=product_id,
            quantity=quantity
        )

    def cancel(self):
        if not self.is_active:
            raise ValueError("Reservation already canceled")
        self.is_active = False
