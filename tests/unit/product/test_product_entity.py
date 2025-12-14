import pytest
from decimal import Decimal

from app.domain.entities.product import Product


def test_create_product_success():
    product = Product.create(
        name="Test",
        description="Test desc",
        price=Decimal("12.90"),
        quantity=5000
    )

    assert product.name == "Test"
    assert product.price == Decimal("12.90")
    assert product.quantity == 5000


def test_create_product_negative_price():
    with pytest.raises(ValueError):
        Product.create(
            name="Test",
            description="Test desc",
            price=Decimal("-1"),
            quantity=5,
        )

def test_create_product_negative_quantity():
    with pytest.raises(ValueError):
        Product.create(
            name="Test",
            description="Test desc",
            price=Decimal("10"),
            quantity=-1,
        )
