from uuid import UUID

from app.domain.repositories.cart_repository import CartRepository
from app.domain.uow.unit_of_work import UnitOfWork


class ClearCartUseCase:
    def __init__(self, uow: UnitOfWork, cart_repo: CartRepository):
        self.uow = uow
        self.carts = cart_repo

    async def execute(self, user_id: UUID):
        async with self.uow:
            cart = await self.carts.get_by_user_id(user_id)

            if cart is None:
                return

            cart.clear()
            await self.carts.update(cart)
