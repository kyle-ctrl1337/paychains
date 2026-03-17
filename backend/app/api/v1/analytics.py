from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.schemas.webhook import (
    AnalyticsOverview,
    ChainBreakdown,
    RevenueDataPoint,
    TokenBreakdown,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _parse_date_range(
    start: str | None, end: str | None
) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    if end:
        period_end = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
    else:
        period_end = now
    if start:
        period_start = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    else:
        period_start = period_end - timedelta(days=30)
    return period_start, period_end


@router.get("/overview", response_model=AnalyticsOverview)
async def analytics_overview(
    start: str | None = Query(None, description="ISO date string"),
    end: str | None = Query(None, description="ISO date string"),
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    period_start, period_end = _parse_date_range(start, end)

    # Total volume and transaction count
    result = await db.execute(
        select(
            func.coalesce(func.sum(Payment.amount_usd), 0),
            func.count(Payment.id),
            func.coalesce(func.sum(Payment.fee_amount_usd), 0),
        ).where(
            Payment.merchant_id == merchant.id,
            Payment.status == "completed",
            Payment.created_at >= period_start,
            Payment.created_at <= period_end,
        )
    )
    row = result.one()
    total_volume = float(row[0])
    total_txns = row[1]
    total_revenue = float(row[2])

    # Active subscriptions
    sub_result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.merchant_id == merchant.id,
            Subscription.status == "active",
        )
    )
    active_subs = sub_result.scalar() or 0

    return AnalyticsOverview(
        total_volume_usd=total_volume,
        total_transactions=total_txns,
        total_revenue_usd=total_revenue,
        active_subscriptions=active_subs,
        period_start=period_start,
        period_end=period_end,
    )


@router.get("/by-chain", response_model=list[ChainBreakdown])
async def analytics_by_chain(
    start: str | None = None,
    end: str | None = None,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    period_start, period_end = _parse_date_range(start, end)

    result = await db.execute(
        select(
            Payment.chain,
            func.coalesce(func.sum(Payment.amount_usd), 0),
            func.count(Payment.id),
        )
        .where(
            Payment.merchant_id == merchant.id,
            Payment.status == "completed",
            Payment.created_at >= period_start,
            Payment.created_at <= period_end,
        )
        .group_by(Payment.chain)
    )

    return [
        ChainBreakdown(chain=row[0], volume_usd=float(row[1]), transaction_count=row[2])
        for row in result.all()
    ]


@router.get("/by-token", response_model=list[TokenBreakdown])
async def analytics_by_token(
    start: str | None = None,
    end: str | None = None,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    period_start, period_end = _parse_date_range(start, end)

    result = await db.execute(
        select(
            Payment.token,
            func.coalesce(func.sum(Payment.amount_usd), 0),
            func.count(Payment.id),
        )
        .where(
            Payment.merchant_id == merchant.id,
            Payment.status == "completed",
            Payment.created_at >= period_start,
            Payment.created_at <= period_end,
        )
        .group_by(Payment.token)
    )

    return [
        TokenBreakdown(token=row[0], volume_usd=float(row[1]), transaction_count=row[2])
        for row in result.all()
    ]


@router.get("/revenue", response_model=list[RevenueDataPoint])
async def analytics_revenue(
    start: str | None = None,
    end: str | None = None,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    period_start, period_end = _parse_date_range(start, end)

    result = await db.execute(
        select(
            func.date_trunc("day", Payment.created_at).label("day"),
            func.coalesce(func.sum(Payment.fee_amount_usd), 0),
            func.count(Payment.id),
        )
        .where(
            Payment.merchant_id == merchant.id,
            Payment.status == "completed",
            Payment.created_at >= period_start,
            Payment.created_at <= period_end,
        )
        .group_by("day")
        .order_by("day")
    )

    return [
        RevenueDataPoint(
            date=row[0].strftime("%Y-%m-%d"),
            revenue_usd=float(row[1]),
            transaction_count=row[2],
        )
        for row in result.all()
    ]
