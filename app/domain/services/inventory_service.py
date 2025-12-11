from uuid import UUID

from app.domain.repositories.product_repository import ProductRepository


class InventoryService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def reserve_product(self, product_id: UUID, amount: int):
        product = await self.product_repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")

        product.reserve(amount)

        await self.product_repo.update(product)
        return product
