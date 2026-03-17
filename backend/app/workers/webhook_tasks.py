import json
import logging
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from app.workers.celery_app import celery_app
from app.models.webhook_event import WebhookEvent
from app.models.merchant import Merchant
from app.utils.crypto import sign_webhook_payload
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

RETRY_DELAYS = [60, 300, 1800, 7200, 86400]  # 1min, 5min, 30min, 2hr, 24hr


def _get_sync_session():
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(db_url)
    return Session(engine)


@celery_app.task(bind=True, max_retries=5)
def deliver_webhook(self, event_id: str):
    """Deliver a single webhook event to the merchant's URL."""
    with _get_sync_session() as session:
        event = session.get(WebhookEvent, event_id)
        if not event:
            logger.error(f"Webhook event {event_id} not found")
            return

        merchant = session.get(Merchant, event.merchant_id)
        if not merchant or not merchant.webhook_url:
            logger.warning(f"No webhook URL for merchant {event.merchant_id}")
            event.status = "failed"
            event.last_error = "No webhook URL configured"
            session.commit()
            return

        payload = json.dumps(event.payload, default=str)
        signature = sign_webhook_payload(payload, merchant.webhook_secret)

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    merchant.webhook_url,
                    content=payload,
                    headers={
                        "Content-Type": "application/json",
                        "X-PayChains-Signature": signature,
                        "X-PayChains-Event": event.event_type,
                    },
                )

            event.attempts += 1
            event.last_response_code = response.status_code

            if response.status_code == 200:
                event.status = "delivered"
                event.delivered_at = datetime.now(timezone.utc)
                logger.info(f"Webhook {event_id} delivered successfully")
            else:
                event.last_error = f"HTTP {response.status_code}: {response.text[:500]}"
                _schedule_retry(event)
        except Exception as e:
            event.attempts += 1
            event.last_error = str(e)[:500]
            _schedule_retry(event)

        session.commit()


def _schedule_retry(event: WebhookEvent):
    """Schedule next retry with exponential backoff."""
    if event.attempts >= event.max_attempts:
        event.status = "failed"
        logger.warning(f"Webhook {event.id} failed after {event.attempts} attempts")
    else:
        delay_idx = min(event.attempts - 1, len(RETRY_DELAYS) - 1)
        delay = RETRY_DELAYS[delay_idx]
        event.next_retry_at = datetime.now(timezone.utc) + timedelta(seconds=delay)
        event.status = "pending"


@celery_app.task
def retry_failed_webhooks():
    """Pick up webhook events that are due for retry."""
    now = datetime.now(timezone.utc)
    with _get_sync_session() as session:
        result = session.execute(
            select(WebhookEvent).where(
                WebhookEvent.status == "pending",
                WebhookEvent.next_retry_at != None,
                WebhookEvent.next_retry_at <= now,
                WebhookEvent.attempts < WebhookEvent.max_attempts,
            )
        )
        for event in result.scalars().all():
            deliver_webhook.delay(str(event.id))
