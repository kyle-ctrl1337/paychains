import uuid
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.subscription import Subscription
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

INTERVAL_DELTAS = {
    "weekly": relativedelta(weeks=1),
    "monthly": relativedelta(months=1),
    "quarterly": relativedelta(months=3),
    "yearly": relativedelta(years=1),
}


@router.post("", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(
    data: SubscriptionCreate,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    if data.interval not in INTERVAL_DELTAS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid interval. Must be one of: {', '.join(INTERVAL_DELTAS)}",
        )

    now = datetime.now(timezone.utc)
    delta = INTERVAL_DELTAS[data.interval]
    period_end = now + delta

    subscription = Subscription(
        merchant_id=merchant.id,
        customer_email=data.customer_email,
        customer_wallet=data.customer_wallet,
        plan_name=data.plan_name,
        amount_usd=data.amount_usd,
        interval=data.interval,
        preferred_chain=data.preferred_chain,
        preferred_token=data.preferred_token,
        current_period_start=now,
        current_period_end=period_end,
        next_payment_at=now,
        metadata_=data.metadata,
    )
    db.add(subscription)
    await db.flush()
    await db.refresh(subscription)
    return SubscriptionResponse.model_validate(subscription)


@router.get("", response_model=list[SubscriptionResponse])
async def list_subscriptions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str | None = None,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    query = select(Subscription).where(Subscription.merchant_id == merchant.id)
    if status:
        query = query.where(Subscription.status == status)

    query = query.order_by(Subscription.created_at.desc())
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    return [SubscriptionResponse.model_validate(s) for s in result.scalars().all()]


@router.get("/{sub_id}", response_model=SubscriptionResponse)
async def get_subscription(
    sub_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Subscription).where(
            Subscription.id == sub_id, Subscription.merchant_id == merchant.id
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return SubscriptionResponse.model_validate(sub)


@router.patch("/{sub_id}", response_model=SubscriptionResponse)
async def update_subscription(
    sub_id: uuid.UUID,
    data: SubscriptionUpdate,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Subscription).where(
            Subscription.id == sub_id, Subscription.merchant_id == merchant.id
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    update_data = data.model_dump(exclude_unset=True)

    # Validate status transitions
    if "status" in update_data:
        valid_transitions = {
            "active": ["paused"],
            "paused": ["active"],
        }
        allowed = valid_transitions.get(sub.status, [])
        if update_data["status"] not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot transition from '{sub.status}' to '{update_data['status']}'",
            )

    for field, value in update_data.items():
        setattr(sub, field, value)

    await db.flush()
    await db.refresh(sub)
    return SubscriptionResponse.model_validate(sub)


@router.delete("/{sub_id}", status_code=204)
async def cancel_subscription(
    sub_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Subscription).where(
            Subscription.id == sub_id, Subscription.merchant_id == merchant.id
        )
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    sub.status = "cancelled"
    sub.cancelled_at = datetime.now(timezone.utc)
    await db.flush()
