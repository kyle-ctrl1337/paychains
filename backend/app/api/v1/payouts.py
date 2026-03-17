from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.payout import Payout
from app.schemas.webhook import PayoutRequest, PayoutResponse

router = APIRouter(prefix="/payouts", tags=["Payouts"])


@router.get("", response_model=list[PayoutResponse])
async def list_payouts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    merchant: Merchant = Depends(get_current_merchant_api_key),
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


@router.post("/request", response_model=PayoutResponse, status_code=201)
async def request_payout(
    data: PayoutRequest,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    # Validate chain has a settlement address
    settlement = merchant.settlement_address or {}
    if data.chain not in settlement:
        raise HTTPException(
            status_code=400,
            detail=f"No settlement address configured for chain '{data.chain}'. Update your merchant settings.",
        )

    payout = Payout(
        merchant_id=merchant.id,
        amount=Decimal(str(data.amount)),
        token=data.token,
        chain=data.chain,
        to_address=data.to_address,
    )
    db.add(payout)
    await db.flush()
    await db.refresh(payout)

    # In production, dispatch to Celery for processing
    # process_payout.delay(str(payout.id))

    return PayoutResponse.model_validate(payout)
