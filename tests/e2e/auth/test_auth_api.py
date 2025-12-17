import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "register@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "register@gmail.com"


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/auth/register",
        json={
            "email": "login@gmail.com",
            "password": "password123"
        }
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "login@gmail.com",
            "password": "password123"
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    response = await client.post("/products/")

    assert response.status_code == 401
