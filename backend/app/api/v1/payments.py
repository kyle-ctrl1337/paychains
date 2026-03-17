import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import create_payment_session

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create", response_model=PaymentResponse, status_code=201)
async def create_payment(
    data: PaymentCreate,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    try:
        payment = await create_payment_session(
            db=db,
            merchant=merchant,
            amount_usd=data.amount_usd,
            token=data.token,
            chain=data.chain,
            payment_link_id=data.payment_link_id,
            metadata=data.metadata,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return PaymentResponse.model_validate(payment)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).where(
            Payment.id == payment_id, Payment.merchant_id == merchant.id
        )
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentResponse.model_validate(payment)


@router.get("", response_model=list[PaymentResponse])
async def list_payments(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str | None = None,
    chain: str | None = None,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    query = select(Payment).where(Payment.merchant_id == merchant.id)

    if status:
        query = query.where(Payment.status == status)
    if chain:
        query = query.where(Payment.chain == chain.lower())

    query = query.order_by(Payment.created_at.desc())
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    return [PaymentResponse.model_validate(p) for p in result.scalars().all()]


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(
    payment_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment).where(
            Payment.id == payment_id, Payment.merchant_id == merchant.id
        )
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.status != "completed":
        raise HTTPException(
            status_code=400, detail="Only completed payments can be refunded"
        )

    payment.status = "refunded"
    await db.flush()
    await db.refresh(payment)

    return PaymentResponse.model_validate(payment)
