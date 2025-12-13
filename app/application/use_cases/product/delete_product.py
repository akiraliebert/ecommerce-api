from uuid import UUID

from app.domain.uow.unit_of_work import UnitOfWork


class DeleteProductUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, product_id: UUID) -> None:
        async with self.uow:
            product = await self.uow.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            await self.uow.products.delete(product_id)
