from app.application.dto.inventory_dto import ReleaseInventoryDTO
from app.domain.repositories.inventory_repository import InventoryRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.uow.unit_of_work import UnitOfWork


class ReleaseInventoryUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        inventory_repo: InventoryRepository,
        product_repo: ProductRepository,
    ):
        self.uow = uow
        self.inventory = inventory_repo
        self.products = product_repo

    async def execute(self, dto: ReleaseInventoryDTO) -> None:
        async with self.uow:
            reservation = await self.inventory.get_by_id(dto.reservation_id)

            if not reservation:
                raise ValueError("Inventory reservation not found")

            if not reservation.is_active:
                raise ValueError("Inventory reservation already canceled")

            product = await self.products.get_by_id(reservation.product_id)

            if not product:
                raise ValueError("Product not found")

            product.release(reservation.quantity)
            reservation.cancel()

            await self.products.update(product)
            await self.inventory.update(reservation)
