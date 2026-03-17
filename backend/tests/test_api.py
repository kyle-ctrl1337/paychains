"""Comprehensive API tests for PayChains."""

import pytest
from httpx import AsyncClient


# ─── Helper ─────────────────────────────────────────────────────

async def register_and_get_keys(client: AsyncClient, email: str = "sdk@test.com"):
    """Register a merchant and return (api_key_test, jwt_token)."""
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "testpass123", "company_name": "SDK Corp"},
    )
    assert reg.status_code == 201
    api_key = reg.json()["api_key_test"]

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "testpass123"},
    )
    token = login.json()["access_token"]
    return api_key, token


# ─── Auth ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_register_missing_email(client: AsyncClient):
    res = await client.post("/api/v1/auth/register", json={"password": "abc123"})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_login_nonexistent_email(client: AsyncClient):
    res = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "x"},
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    _, token = await register_and_get_keys(client, "refresh@test.com")
    res = await client.post(
        "/api/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


# ─── Merchant Profile ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_merchant_profile(client: AsyncClient):
    _, token = await register_and_get_keys(client, "update@test.com")
    res = await client.patch(
        "/api/v1/merchant/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"company_name": "Updated Corp"},
    )
    assert res.status_code == 200
    assert res.json()["company_name"] == "Updated Corp"


@pytest.mark.asyncio
async def test_roll_api_keys(client: AsyncClient):
    old_api_key, token = await register_and_get_keys(client, "roll@test.com")

    # Roll
    res = await client.post(
        "/api/v1/merchant/api-keys/roll",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "api_key_live" in data
    assert "api_key_test" in data


@pytest.mark.asyncio
async def test_auth_with_invalid_token(client: AsyncClient):
    res = await client.get(
        "/api/v1/merchant/me",
        headers={"Authorization": "Bearer invalid_token_here"},
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_auth_with_api_key(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "apikey@test.com")
    res = await client.get(
        "/api/v1/payments",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_auth_without_credentials(client: AsyncClient):
    res = await client.get("/api/v1/payments")
    assert res.status_code == 401


# ─── Payments ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_payments_empty(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "empty@test.com")
    res = await client.get(
        "/api/v1/payments",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_create_payment_missing_fields(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "missing@test.com")
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 10},  # Missing chain and token
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_payment_unsupported_chain(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "badchain@test.com")
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 10, "chain": "cardano", "token": "ADA"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_payment_coming_soon_chain(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "soon@test.com")
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 10, "chain": "solana", "token": "SOL"},
    )
    assert res.status_code == 400
    # Chain/token validation rejects before coming-soon check
    assert "unsupported chain" in res.json()["detail"].lower() or "coming soon" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_nonexistent_payment(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "noexist@test.com")
    res = await client.get(
        "/api/v1/payments/00000000-0000-0000-0000-000000000001",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 404


# ─── Payment Links ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_and_list_payment_links(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "links@test.com")

    # Create
    res = await client.post(
        "/api/v1/payment-links",
        headers={"X-API-Key": api_key},
        json={"title": "Test Product", "amount_usd": 29.99},
    )
    assert res.status_code == 201
    link = res.json()
    assert link["title"] == "Test Product"
    assert link["is_active"] is True

    # List
    res = await client.get(
        "/api/v1/payment-links",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_create_payment_link_no_title(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "notitle@test.com")
    res = await client.post(
        "/api/v1/payment-links",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 10},
    )
    assert res.status_code == 422


# ─── Subscriptions ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_subscriptions_empty(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "nosub@test.com")
    res = await client.get(
        "/api/v1/subscriptions",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert res.json() == []


# ─── Analytics ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_analytics_overview(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "analytics@test.com")
    res = await client.get(
        "/api/v1/analytics/overview",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    data = res.json()
    assert "total_volume_usd" in data
    assert "total_transactions" in data


@pytest.mark.asyncio
async def test_analytics_by_chain(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "bychain@test.com")
    res = await client.get(
        "/api/v1/analytics/by-chain",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_analytics_by_token(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "bytoken@test.com")
    res = await client.get(
        "/api/v1/analytics/by-token",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# ─── Webhooks ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_webhook_events_empty(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "webhooks@test.com")
    res = await client.get(
        "/api/v1/webhooks/events",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert res.json() == []


# ─── Payouts ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_payouts_empty(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "payouts@test.com")
    res = await client.get(
        "/api/v1/payouts",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 200
    assert res.json() == []


# ─── Checkout (public) ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_checkout_nonexistent_link(client: AsyncClient):
    res = await client.get("/api/v1/checkout/00000000-0000-0000-0000-000000000001")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_checkout_coming_soon_chain(client: AsyncClient):
    api_key, _ = await register_and_get_keys(client, "checkout@test.com")

    # Create a payment link
    link_res = await client.post(
        "/api/v1/payment-links",
        headers={"X-API-Key": api_key},
        json={"title": "Checkout Test", "amount_usd": 15.00},
    )
    link_id = link_res.json()["id"]

    # Try to initiate with a coming-soon chain
    res = await client.post(
        f"/api/v1/checkout/{link_id}/initiate",
        json={"chain": "bitcoin", "token": "BTC"},
    )
    assert res.status_code == 400
    # Chain/token validation rejects before coming-soon check
    assert "unsupported chain" in res.json()["detail"].lower() or "coming soon" in res.json()["detail"].lower()


# ─── Health ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_returns_version(client: AsyncClient):
    res = await client.get("/health")
    data = res.json()
    assert data["version"] == "0.1.0"


# ─── Non-Custodial Flow ──────────────────────────────────────

@pytest.mark.asyncio
async def test_create_payment_without_xpub(client: AsyncClient):
    """Payment creation without wallet configured should fail with 400."""
    api_key, _ = await register_and_get_keys(client, "noxpub@test.com")
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 10, "chain": "polygon", "token": "USDC"},
    )
    assert res.status_code == 400
    assert "wallet not configured" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_payment_with_xpub(client: AsyncClient):
    """Payment creation with xpub should derive address from merchant's key."""
    api_key, token = await register_and_get_keys(client, "xpub@test.com")

    # Set xpub via PATCH /merchant/me
    xpub_res = await client.patch(
        "/api/v1/merchant/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"xpub_key": "xpub6CUGRUonZSQ4TWtTMmzXdrXDtypWKiKrhko4egpiMZbpiaQL2jkwSB1icqYh2cfDfVxdx4df189oLKnC5fSwqPfgyP3hooxujYzAu3fDVmz"},
    )
    assert xpub_res.status_code == 200
    assert xpub_res.json()["xpub_key"] is not None

    # Create payment — address should be derived from xpub
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 25, "chain": "ethereum", "token": "USDC"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["deposit_address"].startswith("0x")


@pytest.mark.asyncio
async def test_zero_fees_on_payment(client: AsyncClient):
    """All payments should have zero fees (pure SaaS model)."""
    api_key, token = await register_and_get_keys(client, "zerofee@test.com")
    # Must set wallet address first
    await client.patch(
        "/api/v1/merchant/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"xpub_key": "0xE911c873b881D2d8a4540a710AbE9BE04597B7d4"},
    )
    res = await client.post(
        "/api/v1/payments/create",
        headers={"X-API-Key": api_key},
        json={"amount_usd": 100, "chain": "ethereum", "token": "USDC"},
    )
    assert res.status_code == 201
    data = res.json()
    assert float(data["fee_percentage"]) == 0
    assert float(data["fee_amount_usd"]) == 0


@pytest.mark.asyncio
async def test_payouts_not_needed(client: AsyncClient):
    """Payout request should return message about non-custodial model."""
    api_key, _ = await register_and_get_keys(client, "payouttest@test.com")
    res = await client.post(
        "/api/v1/payouts/request",
        headers={"X-API-Key": api_key},
    )
    assert res.status_code == 400
    assert "directly" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_xpub_in_merchant_response(client: AsyncClient):
    """Merchant response should include xpub_key field."""
    _, token = await register_and_get_keys(client, "xpubfield@test.com")
    res = await client.get(
        "/api/v1/merchant/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert "xpub_key" in res.json()


# ─── Billing ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_upgrade_requires_auth(client: AsyncClient):
    res = await client.post("/api/v1/billing/upgrade?plan=pro")
    assert res.status_code in (401, 403, 422)


@pytest.mark.asyncio
async def test_get_current_plan(client: AsyncClient):
    _, token = await register_and_get_keys(client, "plan@test.com")
    res = await client.get("/api/v1/billing/current-plan", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["plan"] == "free"
    assert data["payment_limit"] == 100
