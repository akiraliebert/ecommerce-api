from fastapi import Depends

from app.domain.repositories.cart_repository import CartRepository

from app.application.use_cases.cart.add_to_cart import AddToCartUseCase
from app.application.use_cases.cart.update_cart_item import UpdateCartItemUseCase
from app.application.use_cases.cart.remove_from_cart import RemoveFromCartUseCase
from app.application.use_cases.cart.clear_cart import ClearCartUseCase
from app.application.use_cases.cart.get_cart import GetCartUseCase

from app.infrastructure.database.repositories.cart_repository_impl import CartRepositoryImpl
from app.infrastructure.web.dependencies.common import get_db_session, get_uow


async def get_cart_repository(session=Depends(get_db_session)) -> CartRepository:
    return CartRepositoryImpl(session)


def get_add_item_uc(uow=Depends(get_uow), repo=Depends(get_cart_repository),):
    return AddToCartUseCase(uow, repo)


def get_update_item_uc(uow=Depends(get_uow), repo=Depends(get_cart_repository)):
    return UpdateCartItemUseCase(uow, repo)


def get_remove_item_uc(uow=Depends(get_uow), repo=Depends(get_cart_repository)):
    return RemoveFromCartUseCase(uow, repo)


def get_clear_cart_uc(uow=Depends(get_uow), repo=Depends(get_cart_repository)):
    return ClearCartUseCase(uow, repo)


def get_get_cart_uc(uow=Depends(get_uow), repo=Depends(get_cart_repository)):
    return GetCartUseCase(uow, repo)
