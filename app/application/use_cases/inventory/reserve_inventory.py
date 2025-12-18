from uuid import UUID

from app.domain.entities.inventory import InventoryReservation
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.uow.unit_of_work import UnitOfWork


class ReserveInventoryUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        product_repo: ProductRepository,
        inventory_repo: InventoryRepository,
    ):
        self.uow = uow
        self.products = product_repo
        self.inventory = inventory_repo

    async def execute(self, product_id: UUID, quantity: int) -> InventoryReservation:
        async with self.uow:
            product = await self.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            # доменная логика
            product.reserve(quantity)

            reservation = InventoryReservation.create(
                product_id=product_id,
                quantity=quantity
            )

            await self.inventory.create(reservation)
            await self.products.update(product)

            return reservation