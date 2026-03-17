from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant
from app.models.merchant import Merchant
from app.models.payout import Payout
from app.schemas.webhook import PayoutRequest, PayoutResponse

router = APIRouter(prefix="/payouts", tags=["Payouts"])


@router.get("", response_model=list[PayoutResponse])
async def list_payouts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    merchant: Merchant = Depends(get_current_merchant),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    result = await db.execute(
        select(Payout)
        .where(Payout.merchant_id == merchant.id)
        .order_by(Payout.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    return [PayoutResponse.model_validate(p) for p in result.scalars().all()]


@router.post("/request")
async def request_payout(
    merchant: Merchant = Depends(get_current_merchant),
):
    """Payouts are not needed in non-custodial mode.

    PayChains never holds your funds — payments are deposited directly
    to addresses derived from your wallet's xpub key.
    """
    raise HTTPException(
        status_code=400,
        detail=(
            "Payouts are not needed with PayChains. "
            "Funds are deposited directly to your wallet addresses "
            "derived from your xpub key. No withdrawal required."
        ),
    )
