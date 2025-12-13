from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.entities.product import Product
from app.application.dto.product_dto import CreateProductDTO, ProductDTO


class CreateProductUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: CreateProductDTO) -> ProductDTO:
        async with self.uow:
            #  создаем доменную сущность
            product = Product.create(
                name=data.name,
                description=data.description,
                price=data.price,
                quantity=data.quantity
            )

            created = await self.uow.products.create(product)

            return ProductDTO(
                id=created.id,
                name=created.name,
                description=created.description,
                price=created.price,
                quantity=created.quantity,
            )