import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_merchant_api_key
from app.models.merchant import Merchant
from app.models.payment_link import PaymentLink
from app.schemas.payment import (
    PaymentLinkCreate,
    PaymentLinkResponse,
    PaymentLinkUpdate,
)

router = APIRouter(prefix="/payment-links", tags=["Payment Links"])


@router.post("", response_model=PaymentLinkResponse, status_code=201)
async def create_payment_link(
    data: PaymentLinkCreate,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    link = PaymentLink(
        merchant_id=merchant.id,
        title=data.title,
        description=data.description,
        amount_usd=data.amount_usd,
        currency=data.currency,
        accepted_chains=data.accepted_chains,
        accepted_tokens=data.accepted_tokens,
        redirect_url=data.redirect_url,
        expires_at=data.expires_at,
        metadata_=data.metadata,
    )
    db.add(link)
    await db.flush()
    await db.refresh(link)
    return PaymentLinkResponse.model_validate(link)


@router.get("", response_model=list[PaymentLinkResponse])
async def list_payment_links(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    result = await db.execute(
        select(PaymentLink)
        .where(PaymentLink.merchant_id == merchant.id)
        .order_by(PaymentLink.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    return [PaymentLinkResponse.model_validate(link) for link in result.scalars().all()]


@router.get("/{link_id}", response_model=PaymentLinkResponse)
async def get_payment_link(
    link_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PaymentLink).where(
            PaymentLink.id == link_id, PaymentLink.merchant_id == merchant.id
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Payment link not found")
    return PaymentLinkResponse.model_validate(link)


@router.patch("/{link_id}", response_model=PaymentLinkResponse)
async def update_payment_link(
    link_id: uuid.UUID,
    data: PaymentLinkUpdate,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PaymentLink).where(
            PaymentLink.id == link_id, PaymentLink.merchant_id == merchant.id
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Payment link not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(link, field, value)

    await db.flush()
    await db.refresh(link)
    return PaymentLinkResponse.model_validate(link)


@router.delete("/{link_id}", status_code=204)
async def deactivate_payment_link(
    link_id: uuid.UUID,
    merchant: Merchant = Depends(get_current_merchant_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PaymentLink).where(
            PaymentLink.id == link_id, PaymentLink.merchant_id == merchant.id
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Payment link not found")

    link.is_active = False
    await db.flush()
