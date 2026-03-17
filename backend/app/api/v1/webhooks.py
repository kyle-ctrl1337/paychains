import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.webhook_event import WebhookEvent
from app.schemas.webhook import WebhookEventResponse, WebhookTestRequest

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get("/events", response_model=list[WebhookEventResponse])
async def list_webhook_events(
    page: int = 1,
    per_page: int = 20,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    result = await db.execute(
        select(WebhookEvent)
        .where(WebhookEvent.merchant_id == merchant.id)
        .order_by(WebhookEvent.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    return [WebhookEventResponse.model_validate(e) for e in result.scalars().all()]


@router.post("/test", response_model=WebhookEventResponse, status_code=201)
async def send_test_webhook(
    data: WebhookTestRequest,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    if not merchant.webhook_url:
        raise HTTPException(
            status_code=400, detail="No webhook URL configured. Update your merchant settings first."
        )

    test_payload = {
        "event": data.event_type,
        "data": {
            "id": str(uuid.uuid4()),
            "amount_usd": "99.99",
            "token": "USDC",
            "chain": "polygon",
            "status": "completed",
            "test": True,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    event = WebhookEvent(
        merchant_id=merchant.id,
        event_type=data.event_type,
        payload=test_payload,
        status="pending",
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)

    # In production, this would be dispatched to a Celery task
    # deliver_webhook.delay(str(event.id))

    return WebhookEventResponse.model_validate(event)
