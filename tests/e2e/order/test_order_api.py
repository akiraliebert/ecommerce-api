import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_order_workflow(client: AsyncClient, auth_headers, product):
    # --- add product to cart ---
    await client.post(
        "/cart/items",
        json={"product_id": product["id"], "quantity": 2},
        headers=auth_headers
    )

    # --- create order ---
    response = await client.post(
        "/orders/",
        headers=auth_headers
    )

    assert response.status_code == 201
    order = response.json()

    order_id = order["id"]
    assert order["status"] == "created"
    assert len(order["items"]) == 1

    # --- get my orders ---
    response = await client.get(
        "/orders/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    orders = response.json()

    assert len(orders) == 1
    assert orders[0]["id"] == order_id

    # --- get order by id ---
    response = await client.get(
        f"/orders/{order_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    order_detail = response.json()

    assert order_detail["id"] == order_id
    assert order_detail["status"] == "created"

    # --- pay order ---
    response = await client.post(
        f"/orders/{order_id}/pay",
        headers=auth_headers
    )

    assert response.status_code == 200

    # --- check paid status ---
    response = await client.get(
        f"/orders/{order_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "paid"


@pytest.mark.asyncio
async def test_pay_nonexistent_order(client, auth_headers):
    response = await client.post(
        f"/orders/{uuid4()}/pay",
        headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_cancel_paid_order(client, auth_headers, product):
    # add to cart
    await client.post(
        "/cart/items",
        json={"product_id": product["id"], "quantity": 1},
        headers=auth_headers
    )

    # create order
    response = await client.post("/orders/", headers=auth_headers)
    order_id = response.json()["id"]

    # pay
    await client.post(f"/orders/{order_id}/pay", headers=auth_headers)

    # cancel
    response = await client.post(
        f"/orders/{order_id}/cancel",
        headers=auth_headers
    )

    assert response.status_code == 400
