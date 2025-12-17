from uuid import UUID

from app.domain.repositories.cart_repository import CartRepository
from app.domain.entities.cart import Cart
from app.application.dto.cart_dto import CartDTO, CartItemDTO
from app.domain.uow.unit_of_work import UnitOfWork


class GetCartUseCase:
    def __init__(self, uow: UnitOfWork, cart_repo: CartRepository):
        self.uow = uow
        self.carts = cart_repo

    async def execute(self, user_id: UUID) -> CartDTO:
        async with self.uow:
            cart = await self.carts.get_by_user_id(user_id)

            if cart is None:
                cart = Cart.create(user_id=user_id)
                await self.carts.create(cart)

            return CartDTO(
                id=cart.id,
                user_id=cart.user_id,
                items=[
                    CartItemDTO(
                        product_id=item.product_id,
                        quantity=item.quantity
                    )
                    for item in cart.items
                ]
            )
