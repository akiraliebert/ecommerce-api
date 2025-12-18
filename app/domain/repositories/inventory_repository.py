from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.inventory import InventoryReservation


class InventoryRepository(ABC):
    """Абстрактный контракт работы с Inventory"""

    @abstractmethod
    async def get_by_id(self, reservation_id: UUID) -> Optional[InventoryReservation]:
        pass

    @abstractmethod
    async def get_active_by_product_id(
        self,
        product_id: UUID
    ) -> list[InventoryReservation]:
        pass

    @abstractmethod
    async def create(self, reservation: InventoryReservation) -> None:
        pass

    @abstractmethod
    async def update(self, reservation: InventoryReservation) -> None:
        pass