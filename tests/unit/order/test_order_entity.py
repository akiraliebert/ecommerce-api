import pytest
from uuid import uuid4
from decimal import Decimal

from app.domain.entities.order import Order, OrderItem, OrderStatus


def test_create_order_success():
    item = OrderItem(
        product_id=uuid4(),
        quantity=2,
        price=Decimal("10.00")
    )

    order = Order.create(
        user_id=uuid4(),
        items=[item]
    )

    assert order.status == OrderStatus.CREATED
    assert order.total_amount() == Decimal("20.00")


def test_create_order_without_items():
    with pytest.raises(ValueError, match="Order must contain at least one item"):
        Order.create(user_id=uuid4(), items=[])


def test_order_mark_paid():
    item = OrderItem(product_id=uuid4(), quantity=1, price=Decimal("5.00"))
    order = Order.create(user_id=uuid4(), items=[item])

    order.mark_paid()

    assert order.status == OrderStatus.PAID


def test_cancel_paid_order_forbidden():
    item = OrderItem(product_id=uuid4(), quantity=1, price=Decimal("5.00"))
    order = Order.create(user_id=uuid4(), items=[item])
    order.mark_paid()

    with pytest.raises(ValueError, match="Paid order cannot be canceled"):
        order.cancel()


