import pytest
from uuid import uuid4, UUID

from app.domain.entities.inventory import InventoryReservation


def test_create_inventory_success():
    product_id = uuid4()
    inventory = InventoryReservation.create(product_id=product_id, quantity=10)


    assert isinstance(inventory.id, UUID)
    assert inventory.product_id == product_id
    assert inventory.is_active is True
    assert inventory.quantity == 10


def test_create_inventory_negative_quantity():
    with pytest.raises(ValueError, match="Quantity must be positive"):
        InventoryReservation.create(product_id=uuid4(), quantity=0)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        InventoryReservation.create(product_id=uuid4(), quantity=-5)


def test_inventory_cancel_success():
    inventory = InventoryReservation.create(product_id=uuid4(), quantity=10)

    assert inventory.is_active is True

    inventory.cancel()

    assert inventory.is_active is False


def test_inventory_cancel_already():
    inventory = InventoryReservation.create(product_id=uuid4(), quantity=10)

    inventory.cancel()

    with pytest.raises(ValueError, match="Reservation already canceled"):
        inventory.cancel()
