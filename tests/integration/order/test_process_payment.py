import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from uuid import uuid4

from app.application.use_cases.order.process_payment import ProcessPaymentUseCase
from app.domain.entities.order import Order, OrderItem, OrderStatus
from app.domain.services.payment_service import PaymentResult


@pytest.mark.asyncio
async def test_process_payment_success(uow, db_session, orders):
    user_id = uuid4()

    order = Order.create(
        user_id=user_id,
        items=[
            OrderItem(
                product_id=uuid4(),
                quantity=2,
                price=Decimal("10.00"),
            )
        ],
    )

    async with db_session.begin():
        await orders.create(order)

    payment_service = AsyncMock()
    payment_service.pay.return_value = PaymentResult.SUCCESS

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment_service,
    )

    result = await uc.execute(order.id)

    assert result.status == OrderStatus.PAID

    order_from_db = await orders.get_by_id(order.id)
    assert order_from_db.status == OrderStatus.PAID


@pytest.mark.asyncio
async def test_process_payment_order_not_found(uow, orders):
    payment_service = AsyncMock()

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment_service,
    )

    with pytest.raises(ValueError, match="Order not found"):
        await uc.execute(uuid4())

    payment_service.pay.assert_not_called()


@pytest.mark.asyncio
async def test_process_payment_failed(uow, db_session, orders):
    order = Order.create(
        user_id=uuid4(),
        items=[
            OrderItem(
                product_id=uuid4(),
                quantity=1,
                price=Decimal("50.00"),
            )
        ],
    )

    async with db_session.begin():
        await orders.create(order)

    payment_service = AsyncMock()
    payment_service.pay.return_value = PaymentResult.FAILED

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment_service,
    )

    result = await uc.execute(order.id)

    assert result.status == OrderStatus.CREATED

    order_from_db = await orders.get_by_id(order.id)
    assert order_from_db.status == OrderStatus.CREATED
