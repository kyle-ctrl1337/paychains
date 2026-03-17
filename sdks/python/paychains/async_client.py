"""Asynchronous PayChains API client."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any, Optional

import httpx

from .exceptions import (
    AuthenticationError,
    NotFoundError,
    PayChainsError,
    RateLimitError,
    ValidationError,
)

_STATUS_EXCEPTION_MAP: dict[int, type[PayChainsError]] = {
    401: AuthenticationError,
    404: NotFoundError,
    422: ValidationError,
    429: RateLimitError,
}


class AsyncPayChains:
    """Asynchronous client for the PayChains API.

    Usage::

        from paychains import AsyncPayChains

        async with AsyncPayChains("sk_live_...") as pc:
            payment = await pc.payments.create(amount_usd=25.00, token="USDC", chain="solana")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.paychains.dev/api/v1",
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            timeout=timeout,
        )

        self.payments = self._Payments(self)
        self.payment_links = self._PaymentLinks(self)
        self.subscriptions = self._Subscriptions(self)
        self.webhooks = self._Webhooks(self)
        self.payouts = self._Payouts(self)
        self.analytics = self._Analytics(self)

    # -- HTTP helpers --------------------------------------------------------

    async def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """Send an HTTP request and return the parsed JSON response."""
        resp = await self._client.request(method, endpoint, **kwargs)
        if resp.status_code >= 400:
            body = resp.json() if resp.content else {}
            message = body.get("message", resp.reason_phrase or "Unknown error")
            exc_cls = _STATUS_EXCEPTION_MAP.get(resp.status_code, PayChainsError)
            raise exc_cls(message=message, status_code=resp.status_code, response=body)
        if resp.status_code == 204:
            return None
        return resp.json()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncPayChains:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -- Webhook verification ------------------------------------------------

    @staticmethod
    def verify_webhook(payload: str, signature: str, secret: str) -> bool:
        """Verify an incoming webhook signature.

        Args:
            payload: The raw request body as a string.
            signature: The ``X-PayChains-Signature`` header value.
            secret: Your webhook signing secret.

        Returns:
            ``True`` if the signature is valid.
        """
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    # -- Resource classes ----------------------------------------------------

    class _Payments:
        """Operations on ``/payments``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def create(
            self,
            amount_usd: float,
            token: str,
            chain: str,
            *,
            metadata: Optional[dict[str, Any]] = None,
            redirect_url: Optional[str] = None,
            **kwargs: Any,
        ) -> dict[str, Any]:
            """Create a new payment."""
            body: dict[str, Any] = {
                "amount_usd": amount_usd,
                "token": token,
                "chain": chain,
            }
            if metadata is not None:
                body["metadata"] = metadata
            if redirect_url is not None:
                body["redirect_url"] = redirect_url
            body.update(kwargs)
            return await self._client._request("POST", "/payments", json=body)

        async def get(self, payment_id: str) -> dict[str, Any]:
            """Retrieve a payment by ID."""
            return await self._client._request("GET", f"/payments/{payment_id}")

        async def list(
            self,
            *,
            page: int = 1,
            per_page: int = 20,
            status: Optional[str] = None,
            chain: Optional[str] = None,
        ) -> dict[str, Any]:
            """List payments with optional filters."""
            params: dict[str, Any] = {"page": page, "per_page": per_page}
            if status is not None:
                params["status"] = status
            if chain is not None:
                params["chain"] = chain
            return await self._client._request("GET", "/payments", params=params)

        async def refund(self, payment_id: str) -> dict[str, Any]:
            """Refund a payment."""
            return await self._client._request("POST", f"/payments/{payment_id}/refund")

    class _PaymentLinks:
        """Operations on ``/payment-links``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def create(
            self,
            title: str,
            *,
            amount_usd: Optional[float] = None,
            description: Optional[str] = None,
            **kwargs: Any,
        ) -> dict[str, Any]:
            """Create a payment link."""
            body: dict[str, Any] = {"title": title}
            if amount_usd is not None:
                body["amount_usd"] = amount_usd
            if description is not None:
                body["description"] = description
            body.update(kwargs)
            return await self._client._request("POST", "/payment-links", json=body)

        async def get(self, link_id: str) -> dict[str, Any]:
            """Retrieve a payment link by ID."""
            return await self._client._request("GET", f"/payment-links/{link_id}")

        async def list(self) -> dict[str, Any]:
            """List all payment links."""
            return await self._client._request("GET", "/payment-links")

        async def delete(self, link_id: str) -> None:
            """Delete a payment link."""
            return await self._client._request("DELETE", f"/payment-links/{link_id}")

    class _Subscriptions:
        """Operations on ``/subscriptions``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def create(
            self,
            plan_id: str,
            token: str,
            chain: str,
            *,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
        ) -> dict[str, Any]:
            """Create a subscription."""
            body: dict[str, Any] = {"plan_id": plan_id, "token": token, "chain": chain}
            if metadata is not None:
                body["metadata"] = metadata
            body.update(kwargs)
            return await self._client._request("POST", "/subscriptions", json=body)

        async def get(self, subscription_id: str) -> dict[str, Any]:
            """Retrieve a subscription by ID."""
            return await self._client._request("GET", f"/subscriptions/{subscription_id}")

        async def list(self, *, page: int = 1, per_page: int = 20) -> dict[str, Any]:
            """List subscriptions."""
            return await self._client._request(
                "GET", "/subscriptions", params={"page": page, "per_page": per_page}
            )

        async def cancel(self, subscription_id: str) -> dict[str, Any]:
            """Cancel a subscription."""
            return await self._client._request(
                "POST", f"/subscriptions/{subscription_id}/cancel"
            )

    class _Webhooks:
        """Operations on ``/webhooks``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def create(
            self,
            url: str,
            events: list[str],
            **kwargs: Any,
        ) -> dict[str, Any]:
            """Register a webhook endpoint."""
            body: dict[str, Any] = {"url": url, "events": events}
            body.update(kwargs)
            return await self._client._request("POST", "/webhooks", json=body)

        async def get(self, webhook_id: str) -> dict[str, Any]:
            """Retrieve a webhook by ID."""
            return await self._client._request("GET", f"/webhooks/{webhook_id}")

        async def list(self) -> dict[str, Any]:
            """List all webhooks."""
            return await self._client._request("GET", "/webhooks")

        async def delete(self, webhook_id: str) -> None:
            """Delete a webhook."""
            return await self._client._request("DELETE", f"/webhooks/{webhook_id}")

    class _Payouts:
        """Operations on ``/payouts``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def create(
            self,
            amount_usd: float,
            token: str,
            chain: str,
            destination: str,
            **kwargs: Any,
        ) -> dict[str, Any]:
            """Create a payout."""
            body: dict[str, Any] = {
                "amount_usd": amount_usd,
                "token": token,
                "chain": chain,
                "destination": destination,
            }
            body.update(kwargs)
            return await self._client._request("POST", "/payouts", json=body)

        async def get(self, payout_id: str) -> dict[str, Any]:
            """Retrieve a payout by ID."""
            return await self._client._request("GET", f"/payouts/{payout_id}")

        async def list(self, *, page: int = 1, per_page: int = 20) -> dict[str, Any]:
            """List payouts."""
            return await self._client._request(
                "GET", "/payouts", params={"page": page, "per_page": per_page}
            )

    class _Analytics:
        """Operations on ``/analytics``."""

        def __init__(self, client: AsyncPayChains) -> None:
            self._client = client

        async def summary(self, *, period: str = "30d") -> dict[str, Any]:
            """Get an analytics summary."""
            return await self._client._request(
                "GET", "/analytics/summary", params={"period": period}
            )

        async def revenue(
            self, *, period: str = "30d", group_by: str = "day"
        ) -> dict[str, Any]:
            """Get revenue analytics."""
            return await self._client._request(
                "GET", "/analytics/revenue", params={"period": period, "group_by": group_by}
            )
