from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_jwt
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.models.payment_link import PaymentLink
from app.models.subscription import Subscription
from app.models.payout import Payout

router = APIRouter(prefix="/admin", tags=["Admin"])


async def require_admin(
    merchant: Merchant = Depends(get_current_merchant_jwt),
) -> Merchant:
    if not merchant.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return merchant


@router.get("/stats")
async def admin_stats(
    admin: Merchant = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    total_merchants = await db.scalar(select(func.count(Merchant.id)))
    active_merchants = await db.scalar(
        select(func.count(Merchant.id)).where(Merchant.is_active == True)
    )
    total_payments = await db.scalar(select(func.count(Payment.id)))
    completed_payments = await db.scalar(
        select(func.count(Payment.id)).where(Payment.status == "completed")
    )
    total_volume = await db.scalar(
        select(func.coalesce(func.sum(Payment.amount_usd), 0)).where(
            Payment.status == "completed"
        )
    )
    total_fees = await db.scalar(
        select(func.coalesce(func.sum(Payment.fee_amount_usd), 0)).where(
            Payment.status == "completed"
        )
    )
    total_links = await db.scalar(select(func.count(PaymentLink.id)))
    total_subs = await db.scalar(select(func.count(Subscription.id)))
    total_payouts = await db.scalar(select(func.count(Payout.id)))

    return {
        "total_merchants": total_merchants,
        "active_merchants": active_merchants,
        "total_payments": total_payments,
        "completed_payments": completed_payments,
        "total_volume_usd": float(total_volume),
        "total_fees_usd": float(total_fees),
        "total_payment_links": total_links,
        "total_subscriptions": total_subs,
        "total_payouts": total_payouts,
    }


@router.get("/merchants")
async def list_merchants(
    admin: Merchant = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Merchant).order_by(Merchant.created_at.desc())
    )
    merchants = result.scalars().all()
    return [
        {
            "id": str(m.id),
            "email": m.email,
            "company_name": m.company_name,
            "plan": m.plan,
            "is_active": m.is_active,
            "is_admin": m.is_admin,
            "auto_convert_to": m.auto_convert_to,
            "webhook_url": m.webhook_url,
            "created_at": m.created_at.isoformat(),
            "updated_at": m.updated_at.isoformat(),
        }
        for m in merchants
    ]


@router.get("/payments")
async def list_all_payments(
    admin: Merchant = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).order_by(Payment.created_at.desc()).limit(100)
    )
    payments = result.scalars().all()
    return [
        {
            "id": str(p.id),
            "merchant_id": str(p.merchant_id),
            "status": p.status,
            "amount_usd": str(p.amount_usd),
            "token": p.token,
            "chain": p.chain,
            "deposit_address": p.deposit_address,
            "tx_hash": p.tx_hash,
            "fee_amount_usd": str(p.fee_amount_usd) if p.fee_amount_usd else None,
            "created_at": p.created_at.isoformat(),
        }
        for p in payments
    ]


@router.patch("/merchants/{merchant_id}")
async def update_merchant(
    merchant_id: str,
    data: dict,
    admin: Merchant = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    import uuid

    result = await db.execute(
        select(Merchant).where(Merchant.id == uuid.UUID(merchant_id))
    )
    merchant = result.scalar_one_or_none()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    allowed_fields = {"is_active", "plan", "is_admin"}
    for field, value in data.items():
        if field in allowed_fields:
            setattr(merchant, field, value)

    await db.flush()
    await db.refresh(merchant)

    return {
        "id": str(merchant.id),
        "email": merchant.email,
        "company_name": merchant.company_name,
        "plan": merchant.plan,
        "is_active": merchant.is_active,
        "is_admin": merchant.is_admin,
    }
