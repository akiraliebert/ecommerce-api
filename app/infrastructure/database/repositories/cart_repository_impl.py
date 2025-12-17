from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.entities.cart import Cart, CartItem
from app.domain.repositories.cart_repository import CartRepository
from app.infrastructure.database.models.cart_model import CartModel
from app.infrastructure.database.models.cart_item_model import CartItemModel


class CartRepositoryImpl(CartRepository):
    def __init__(self, session):
        self.session = session


    # -------------------------
    # MAPPERS
    # -------------------------

    def _to_domain(self, model: CartModel) -> Cart:
        cart = Cart(
            id=model.id,
            user_id=model.user_id,
            items=[]
        )

        for item in model.items:
            cart.items.append(
                CartItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        return cart

    def _to_model(self, cart: Cart) -> CartModel:
        model = CartModel(
            id=cart.id,
            user_id=cart.user_id,
            items=[]
        )

        for item in cart.items:
            model.items.append(
                CartItemModel(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

        return model

    async def _get_model(self, cart_id: UUID) -> CartModel:
        result = await self.session.execute(
            select(CartModel)
            .where(CartModel.id == cart_id)
            .options(selectinload(CartModel.items))
        )
        return result.scalar_one()

    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        result = await self.session.execute(
            select(CartModel)
            .where(CartModel.user_id == user_id)
            .options(selectinload(CartModel.items))
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._to_domain(model)


    async def create(self, cart: Cart) -> None:
        self.session.add(self._to_model(cart))

    async def update(self, cart: Cart) -> None:
        model = await self._get_model(cart.id)
        model.items.clear()

        for item in cart.items:
            model.items.append(
                CartItemModel(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
            )

    async def delete(self, cart: Cart) -> None:
        model = await self._get_model(cart.id)
        await self.session.delete(model)
