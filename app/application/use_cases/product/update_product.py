from uuid import UUID

from app.domain.uow.unit_of_work import UnitOfWork
from app.application.dto.product_dto import UpdateProductDTO, ProductDTO


class UpdateProductUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, product_id: UUID, data: UpdateProductDTO) -> ProductDTO:
        if not any([
            data.name,
            data.description,
            data.price,
            data.quantity,
        ]):
            raise ValueError("No fields provided for update")

        async with self.uow:
            product = await self.uow.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            # частичное обновление
            if data.name is not None:
                product.name = data.name

            if data.description is not None:
                product.description = data.description

            if data.price is not None:
                product.price = data.price

            if data.quantity is not None:
                product.quantity = data.quantity

            updated = await self.uow.products.update(product)

            return ProductDTO(
                id=updated.id,
                name=updated.name,
                description=updated.description,
                price=updated.price,
                quantity=updated.quantity,
            )