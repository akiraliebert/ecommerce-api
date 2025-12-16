from app.domain.uow.unit_of_work import UnitOfWork
from app.application.dto.product_dto import ProductDTO
from app.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, uow: UnitOfWork, product_repo: ProductRepository):
        self.uow = uow
        self.products = product_repo

    async def execute(self) -> list[ProductDTO]:
        async with self.uow:
            products = await self.products.list()

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
