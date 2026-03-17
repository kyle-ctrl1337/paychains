import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "paychains-api"


@pytest.mark.asyncio
async def test_register_merchant(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "company_name": "Test Corp",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["company_name"] == "Test Corp"
    assert "api_key_live" in data
    assert data["api_key_live"].startswith("pc_live_")
    assert data["api_key_test"].startswith("pc_test_")


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@example.com", "password": "pass123"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@example.com", "password": "pass456"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "mypassword"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["merchant"]["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrong@example.com", "password": "correctpass"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_merchant_profile(client: AsyncClient):
    # Register
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "profile@example.com", "password": "pass123"},
    )
    # Login to get JWT
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "profile@example.com", "password": "pass123"},
    )
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/merchant/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "profile@example.com"
