from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from app.domain.entities.order import Order


class OrderRepository(ABC):
    """Абстрактный контракт работы с Order"""

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Order]:
        pass

    @abstractmethod
    async def create(self, order: Order) -> None:
        """
        Persist new Order aggregate
        """
        pass

    @abstractmethod
    async def update(self, order: Order) -> None:
        """
        Persist changes in Order aggregate
        """
        pass
