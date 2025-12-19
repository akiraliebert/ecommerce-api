import pytest
from httpx import AsyncClient
from decimal import Decimal


@pytest.mark.asyncio
async def test_full_order_flow(
    client: AsyncClient,
    auth_headers,
    product,
):
    """
    Full business flow:
    product -> cart -> order -> payment -> consistency checks
    """

    product_id = product["id"]
    initial_quantity = product["quantity"]

    # --- add product to cart ---
    response = await client.post(
        "/cart/items",
        json={
            "product_id": product_id,
            "quantity": 2,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200


    # --- create order ---
    response = await client.post(
        "/orders/",
        headers=auth_headers,
    )

    assert response.status_code == 201
    order = response.json()

    order_id = order["id"]
    assert order["status"] == "created"
    price = Decimal(product["price"])
    total = price * 2
    assert order["total"] == str(total)


    # --- cart must be cleared after order creation ---
    response = await client.get(
        "/cart/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    cart = response.json()
    assert cart["items"] == []


    # --- pay order ---
    response = await client.post(
        f"/orders/{order_id}/pay",
        headers=auth_headers,
    )

    assert response.status_code == 200

    # --- check order status ---
    response = await client.get(
        f"/orders/{order_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    order = response.json()

    assert order["status"] == "paid"

    # --- check product quantity decreased ---
    response = await client.get(
        f"/products/{product_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    product_after = response.json()

    assert product_after["quantity"] == initial_quantity - 2
