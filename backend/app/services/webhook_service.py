"""Service for creating and dispatching webhook events."""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent


async def create_webhook_event(
    db: AsyncSession,
    merchant_id: uuid.UUID,
    event_type: str,
    payload: dict,
) -> WebhookEvent:
    """Create a webhook event and dispatch it for delivery."""
    event = WebhookEvent(
        merchant_id=merchant_id,
        event_type=event_type,
        payload={
            "event": event_type,
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)

    # Dispatch to Celery for async delivery
    from app.workers.webhook_tasks import deliver_webhook
    deliver_webhook.delay(str(event.id))

    return event
