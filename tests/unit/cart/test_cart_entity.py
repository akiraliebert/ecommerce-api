from uuid import uuid4
import pytest

from app.domain.entities.cart import Cart, CartItem


def test_create_cart_success():
    user_id = uuid4()
    cart = Cart.create(user_id=user_id)


    assert cart.items == []
    assert cart.user_id == user_id


def test_every_cart_is_unique():
    cart1 = Cart.create(user_id=uuid4())
    cart2 = Cart.create(user_id=uuid4())

    cart1.add_item(product_id=uuid4(), quantity=3)


    assert cart1.items != cart2.items


def test_add_same_product_increases_quantity():
    cart = Cart.create(user_id=uuid4())
    product_id = uuid4()

    cart.add_item(product_id=product_id, quantity=3)
    cart.add_item(product_id=product_id, quantity=2)

    assert len(cart.items) == 1
    assert cart.items[0].quantity == 5


def test_add_update_cart_item_negative_quantity():
    cart = Cart.create(user_id=uuid4())


    with pytest.raises(ValueError, match='Quantity must be positive'):
        cart.add_item(product_id=uuid4(), quantity=-5)

    with pytest.raises(ValueError, match='Quantity must be positive'):
        cart.add_item(product_id=uuid4(), quantity=0)

    with pytest.raises(ValueError, match='Quantity must be positive'):
        cart.update_item(product_id=uuid4(), quantity=-10)


    assert cart.items == []


def test_update_cart_item_success():
    cart = Cart.create(user_id=uuid4())
    product_id = uuid4()

    cart.add_item(product_id=product_id, quantity=5)

    cart.update_item(product_id=product_id, quantity=10)

    assert cart.items[0].quantity == 10


def test_update_cart_item_not_found():
    cart = Cart.create(user_id=uuid4())

    with pytest.raises(ValueError, match='Product not found in cart'):
        cart.update_item(product_id=uuid4(), quantity=3)


def test_remove_cart_item_success():
    cart = Cart.create(user_id=uuid4())
    product_id = uuid4()

    cart.add_item(product_id=product_id, quantity=5)

    cart.remove_item(product_id=product_id)

    assert cart.items == []


def test_remove_cart_item_not_found():
    cart = Cart.create(user_id=uuid4())

    with pytest.raises(ValueError, match='Product not found in cart'):
        cart.remove_item(product_id=uuid4())


def test_clear_cart_success():
    cart = Cart.create(user_id=uuid4())

    cart.add_item(product_id=uuid4(), quantity=5)
    cart.add_item(product_id=uuid4(), quantity=10)
    cart.add_item(product_id=uuid4(), quantity=15)

    cart.clear()


    assert cart.items == []


def test_cartitem_increase_decrease_negative_amount():
    cart_item = CartItem(product_id=uuid4(), quantity=5)

    with pytest.raises(ValueError, match='Amount must be positive'):
        cart_item.increase(amount=-5)

    with pytest.raises(ValueError, match='Amount must be positive'):
        cart_item.decrease(amount=-5)


def test_cartitem_prevents_quantity_less_than_one():
    cart_item = CartItem(product_id=uuid4(), quantity=2)

    with pytest.raises(ValueError, match='Cart item quantity cannot be less than 1'):
        cart_item.decrease(amount=2)
