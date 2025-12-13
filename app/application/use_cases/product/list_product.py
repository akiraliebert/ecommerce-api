from app.domain.uow.unit_of_work import UnitOfWork
from app.application.dto.product_dto import ProductDTO


class ListProductsUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self) -> list[ProductDTO]:
        async with self.uow:
            products = await self.uow.products.list()

            return [
                ProductDTO(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    quantity=p.quantity,
                )
                for p in products
            ]
