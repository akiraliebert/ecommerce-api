import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cart_workflow(client: AsyncClient, auth_headers, product):
    #  test get empty cart
    response = await client.get(
        "/cart/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["items"] == []


    #  test add item to cart and get it
    response = await client.post(
        "/cart/items",
        json={
            "product_id": product["id"],
            "quantity": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    response = await client.get(
        "/cart/",
        headers=auth_headers
    )

    cart = response.json()
    assert len(cart["items"]) == 1

    item = cart["items"][0]
    assert item["product_id"] == product["id"]
    assert item["quantity"] == 3


    #  test update item and check it
    response = await client.put(
        f"/cart/items/{product['id']}",
        json={"quantity": 5},
        headers=auth_headers
    )

    assert response.status_code == 200

    response = await client.get(
        "/cart/",
        headers=auth_headers
    )

    cart = response.json()

    assert cart["items"][0]["quantity"] == 5


    #  test remove item from cart and check it
    response = await client.delete(
        f"/cart/items/{product['id']}",
        headers=auth_headers
    )

    assert response.status_code == 204

    response = await client.get(
        "/cart/",
        headers=auth_headers
    )

    cart = response.json()
    assert cart["items"] == []


    #  test clear cart and check it
    await client.post(
        "/cart/items",
        json={"product_id": product["id"], "quantity": 2},
        headers=auth_headers
    )

    await client.post(
        "/cart/items",
        json={"product_id": product["id"], "quantity": 3},
        headers=auth_headers
    )

    response = await client.delete("/cart/", headers=auth_headers)

    assert response.status_code == 204

    response = await client.get(
        "/cart/",
        headers=auth_headers
    )

    cart = response.json()
    assert cart["items"] == []


@pytest.mark.asyncio
async def test_add_item_negative_quantity(client, auth_headers, product):
    response = await client.post(
        "/cart/items",
        json={
            "product_id": product["id"],
            "quantity": -1
        },
        headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_cart_item_zero_quantity(client, auth_headers, product):
    response = await client.put(
        f"/cart/items/{product['id']}",
        json={"quantity": 0},
        headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_remove_nonexistent_item(client, auth_headers):
    response = await client.delete(
        "/cart/items/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_cart_unauthorized(client: AsyncClient):
    response = await client.get("/cart/")

    assert response.status_code == 401

