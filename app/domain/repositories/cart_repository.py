from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.cart import Cart


class CartRepository(ABC):
    """Абстрактный контракт работы с Cart"""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        pass

    @abstractmethod
    async def create(self, cart: Cart) -> None:
        pass

    @abstractmethod
    async def update(self, cart: Cart) -> None:
        pass

    @abstractmethod
    async def delete(self, cart: Cart) -> None:
        pass
