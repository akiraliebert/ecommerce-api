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
async def test_refresh_token_flow(client):
    # register
    await client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123456",
    })

    # login
    response = await client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "123456",
    })

    tokens = response.json()

    # refresh
    response = await client.post("/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })

    assert response.status_code == 200
    new_tokens = response.json()

    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    # assert tokens["access_token"] != new_tokens["access_token"]  # при добавлении jti
    # assert tokens["refresh_token"] != new_tokens["refresh_token"]


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    response = await client.post("/products/")

    assert response.status_code == 401
