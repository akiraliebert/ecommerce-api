from uuid import UUID

from app.domain.repositories.cart_repository import CartRepository
from app.domain.uow.unit_of_work import UnitOfWork


class UpdateCartItemUseCase:
    def __init__(self, uow: UnitOfWork, cart_repo: CartRepository):
        self.uow = uow
        self.carts = cart_repo

    async def execute(self, user_id: UUID, product_id: UUID, quantity: int):
        async with self.uow:
            cart = await self.carts.get_by_user_id(user_id)

            if cart is None:
                raise ValueError("Cart not found")

            cart.update_item(product_id=product_id, quantity=quantity)

            await self.carts.update(cart)
