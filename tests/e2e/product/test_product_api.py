import pytest


@pytest.mark.asyncio
async def test_create_product(client):
    payload = {
        "name": "API Product",
        "description": "From API",
        "price": "12.50",
        "quantity": 5,
    }

    response = await client.post("/products/", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "API Product"


@pytest.mark.asyncio
async def test_get_product(client):
    payload = {
            "name": "Get test",
            "price": "10.00",
            "quantity": 1,
    }

    create = await client.post("/products/", json=payload)

    product_id = create.json()["id"]

    response = await client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["id"] == product_id


@pytest.mark.asyncio
async def test_list_products(client):
    response = await client.get("/products/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_product(client):
    payload = {"name": "test update",
               "price": "50.00",
               "quantity": 3}

    create = await client.post("/products/", json=payload)

    update_payload = {"description": "new desc", "quantity": 10}

    response = await client.put(f"/products/{create.json()["id"]}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["description"] == "new desc"
    assert response.json()["quantity"] == 10


@pytest.mark.asyncio
async def test_delete_product(client):
    create = await client.post(
        "/products/",
        json={
            "name": "Delete me",
            "price": "5.00",
            "quantity": 1,
        },
    )

    product_id = create.json()["id"]

    delete_response = await client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
