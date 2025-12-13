from uuid import UUID
from app.domain.uow.unit_of_work import UnitOfWork
from app.application.dto.product_dto import ProductDTO


class GetProductUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, product_id: UUID) -> ProductDTO:
        async with self.uow:
            product = await self.uow.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            return ProductDTO(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
            )