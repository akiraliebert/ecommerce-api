from fastapi import Depends

from app.domain.repositories.order_repository import OrderRepository

from app.infrastructure.database.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.database.repositories.cart_repository_impl import CartRepositoryImpl
from app.infrastructure.database.repositories.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.database.repositories.inventory_repository_impl import InventoryRepositoryImpl
from app.infrastructure.external.mock_payment_service import MockPaymentService

from app.application.services.order.place_order import PlaceOrderService
from app.application.use_cases.order.process_payment import ProcessPaymentUseCase
from app.application.use_cases.order.get_my_orders import GetMyOrdersUseCase
from app.application.use_cases.order.get_order_by_id import GetOrderByIdUseCase
from app.application.use_cases.order.cancel_order import CancelOrderUseCase


from app.infrastructure.web.dependencies.common import get_db_session, get_uow


def get_place_order_service(
    uow=Depends(get_uow),
    session=Depends(get_db_session),
):
    return PlaceOrderService(
        uow=uow,
        cart_repo=CartRepositoryImpl(session),
        product_repo=ProductRepositoryImpl(session),
        inventory_repo=InventoryRepositoryImpl(session),
        order_repo=OrderRepositoryImpl(session),
    )


async def get_order_repository(session=Depends(get_db_session)) -> OrderRepository:
    return OrderRepositoryImpl(session)


def get_my_orders_uc(uow=Depends(get_uow), repo=Depends(get_order_repository)):
    return GetMyOrdersUseCase(uow, repo)


def get_order_by_id_uc(uow=Depends(get_uow), repo=Depends(get_order_repository)):
    return GetOrderByIdUseCase(uow, repo)


def get_cancel_order_uc(uow=Depends(get_uow), repo=Depends(get_order_repository)):
    return CancelOrderUseCase(uow, repo)


def get_payment_service():
    return MockPaymentService()


def get_process_payment_uc(
    uow=Depends(get_uow),
    session=Depends(get_db_session),
    payment_service=Depends(get_payment_service),  # Stripe/mock/etc
):
    return ProcessPaymentUseCase(
        uow=uow,
        order_repo=OrderRepositoryImpl(session),
        payment_service=payment_service,
    )

