from uuid import UUID

from app.domain.repositories.cart_repository import CartRepository
from app.domain.uow.unit_of_work import UnitOfWork


class RemoveFromCartUseCase:
    def __init__(self, uow: UnitOfWork, cart_repo: CartRepository):
        self.uow = uow
        self.carts = cart_repo

    async def execute(self, user_id: UUID, product_id: UUID):
        async with self.uow:
            cart = await self.carts.get_by_user_id(user_id)

            if cart is None:
                raise ValueError("Cart not found")

            cart.remove_item(product_id=product_id)

            await self.carts.update(cart)
