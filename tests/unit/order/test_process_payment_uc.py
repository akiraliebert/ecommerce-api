import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.order.process_payment import ProcessPaymentUseCase
from app.domain.entities.order import Order, OrderItem, OrderStatus
from app.domain.services.payment_service import PaymentResult


@pytest.mark.asyncio
async def test_process_payment_success():
    order = Order.create(
        user_id=uuid4(),
        items=[
            OrderItem(
                product_id=uuid4(),
                quantity=2,
                price=Decimal("10.00"),
            )
        ]
    )

    uow = AsyncMock()
    uow.__aenter__.return_value = uow

    orders = AsyncMock()
    orders.get_by_id.return_value = order

    payment = AsyncMock()
    payment.pay.return_value = PaymentResult.SUCCESS

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment,
    )

    result = await uc.execute(order.id)

    assert result.status == OrderStatus.PAID
    orders.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_payment_order_not_found():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow

    orders = AsyncMock()
    orders.get_by_id.return_value = None

    payment = AsyncMock()

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment,
    )

    with pytest.raises(ValueError, match="Order not found"):
        await uc.execute(uuid4())

    payment.pay.assert_not_called()


@pytest.mark.asyncio
async def test_process_payment_failed():
    order = Order.create(
        user_id=uuid4(),
        items=[
            OrderItem(
                product_id=uuid4(),
                quantity=1,
                price=Decimal("20.00"),
            )
        ]
    )

    uow = AsyncMock()
    uow.__aenter__.return_value = uow

    orders = AsyncMock()
    orders.get_by_id.return_value = order

    payment = AsyncMock()
    payment.pay.return_value = PaymentResult.FAILED

    uc = ProcessPaymentUseCase(
        uow=uow,
        order_repo=orders,
        payment_service=payment,
    )

    result = await uc.execute(order.id)

    assert result.status == OrderStatus.CREATED
    orders.update.assert_awaited_once()
