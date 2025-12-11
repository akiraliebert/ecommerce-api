from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from app.domain.entities.product import Product

class ProductRepository(ABC):
    """Абстрактный контракт работы с Product"""

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    async def list(self) -> List[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: UUID) -> None:
        pass