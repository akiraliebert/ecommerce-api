from uuid import UUID

from app.domain.uow.unit_of_work import UnitOfWork
from app.application.dto.product_dto import ProductDTO
from app.domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    def __init__(self, uow: UnitOfWork, product_repo: ProductRepository):
        self.uow = uow
        self.products = product_repo

    async def execute(self, product_id: UUID) -> ProductDTO:
        async with self.uow:
            product = await self.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            return ProductDTO(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
            )