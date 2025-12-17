from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.database.models.product_model import ProductModel


class ProductRepositoryImpl(ProductRepository):
    """Реализация репозитория через SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------------------------
    #   Helpers (private)
    # ---------------------------

    @staticmethod
    def _to_entity(model: ProductModel) -> Product:
        """Преобразование SQLAlchemy модели в доменную сущность."""
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            quantity=model.quantity
        )

    @staticmethod
    def _to_model(entity: Product) -> ProductModel:
        """Преобразование domain сущности в SQLAlchemy модель."""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            quantity=entity.quantity,
        )

    # ---------------------------
    #   CRUD
    # ---------------------------

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return self._to_entity(model)
        return None

    async def list(self) -> List[Product]:
        stmt = select(ProductModel)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._to_entity(m) for m in models]

    async def create(self, product: Product) -> Product:
        model = self._to_model(product)
        self.session.add(model)
        return product

    async def update(self, product: Product) -> Product:
        """Обновляет существующую запись"""
        stmt = select(ProductModel).where(ProductModel.id == product.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        model.name = product.name
        model.description = product.description
        model.price = product.price
        model.quantity = product.quantity

        await self.session.flush()
        return self._to_entity(model)

    async def delete(self, product_id: UUID) -> None:
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one()

        await self.session.delete(model)
        await self.session.flush()
