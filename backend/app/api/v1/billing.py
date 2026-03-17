"""Billing endpoints — plan upgrades via crypto payments (dogfooding PayChains)."""

import logging
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_merchant_jwt
from app.models.merchant import Merchant
from app.services.payment_service import PLAN_PAYMENT_LIMITS, create_payment_session

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/billing", tags=["billing"])

PLAN_CONFIG = {
    "pro": {"amount_usd": 49.00, "name": "Pro", "limit": 2000},
    "enterprise": {"amount_usd": 199.00, "name": "Enterprise", "limit": 999999},
}

PLAN_ORDER = ["free", "pro", "enterprise"]


@router.post("/upgrade")
async def create_upgrade_payment(
    plan: str,
    chain: str = "polygon",
    token: str = "USDC",
    merchant: Merchant = Depends(get_current_merchant_jwt),
    db: AsyncSession = Depends(get_db),
):
    """Create a crypto payment to upgrade the merchant's plan."""
    plan = plan.lower()

    if plan not in PLAN_CONFIG:
        raise HTTPException(status_code=400, detail=f"Invalid plan: {plan}. Choose from: {', '.join(PLAN_CONFIG.keys())}")

    # Check if already on this plan
    if merchant.plan == plan:
        raise HTTPException(status_code=400, detail=f"You are already on the {plan} plan")

    # Check for downgrade
    current_index = PLAN_ORDER.index(merchant.plan) if merchant.plan in PLAN_ORDER else 0
    target_index = PLAN_ORDER.index(plan)
    if target_index <= current_index:
        raise HTTPException(status_code=400, detail="Cannot downgrade plan via this endpoint")

    # Find admin merchant who receives upgrade payments
    result = await db.execute(
        select(Merchant).where(Merchant.is_admin == True)  # noqa: E712
    )
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=500, detail="No admin merchant configured")

    if not admin.xpub_key:
        raise HTTPException(status_code=500, detail="Admin merchant has no xpub_key configured for receiving payments")

    # Create payment session with admin as the receiving merchant
    plan_info = PLAN_CONFIG[plan]
    metadata = {
        "type": "plan_upgrade",
        "upgrading_merchant_id": str(merchant.id),
        "target_plan": plan,
    }

    try:
        payment = await create_payment_session(
            db=db,
            merchant=admin,
            amount_usd=Decimal(str(plan_info["amount_usd"])),
            token=token,
            chain=chain,
            metadata=metadata,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    checkout_url = f"{settings.app_url}/checkout/{payment.id}"

    return {
        "payment_id": str(payment.id),
        "checkout_url": checkout_url,
        "amount_usd": str(payment.amount_usd),
        "deposit_address": payment.deposit_address,
        "chain": payment.chain,
        "token": payment.token,
        "plan": plan,
    }


@router.get("/current-plan")
async def get_current_plan(
    merchant: Merchant = Depends(get_current_merchant_jwt),
):
    """Get the current merchant's plan details."""
    limit = PLAN_PAYMENT_LIMITS.get(merchant.plan, 100)
    return {
        "plan": merchant.plan,
        "payment_limit": limit,
    }
