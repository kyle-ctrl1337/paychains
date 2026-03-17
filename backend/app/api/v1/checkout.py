import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.models.payment_link import PaymentLink
from app.schemas.payment import CheckoutInitiate, CheckoutStatusResponse
from app.services.payment_service import create_payment_session, COMING_SOON_CHAINS
from app.utils.qrcode import generate_qr_code_base64

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.get("/{payment_link_id}")
async def get_checkout_data(
    payment_link_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint — returns checkout page data for a payment link."""
    result = await db.execute(
        select(PaymentLink).where(
            PaymentLink.id == payment_link_id,
            PaymentLink.is_active == True,
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Payment link not found or inactive")

    if link.expires_at and link.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Payment link has expired")

    return {
        "id": link.id,
        "title": link.title,
        "description": link.description,
        "amount_usd": link.amount_usd,
        "currency": link.currency,
        "accepted_chains": link.accepted_chains,
        "accepted_tokens": link.accepted_tokens,
    }


@router.post("/{payment_link_id}/initiate")
async def initiate_checkout(
    payment_link_id: uuid.UUID,
    data: CheckoutInitiate,
    db: AsyncSession = Depends(get_db),
):
    """Customer selects chain/token, gets a deposit address and QR code."""
    result = await db.execute(
        select(PaymentLink).where(
            PaymentLink.id == payment_link_id,
            PaymentLink.is_active == True,
        )
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Payment link not found or inactive")

    chain = data.chain.lower()
    token = data.token.upper()

    if chain in COMING_SOON_CHAINS:
        raise HTTPException(status_code=400, detail=f"{chain.capitalize()} support is coming soon")
    if chain not in link.accepted_chains:
        raise HTTPException(status_code=400, detail=f"Chain '{chain}' not accepted")
    if token not in link.accepted_tokens:
        raise HTTPException(status_code=400, detail=f"Token '{token}' not accepted")
    if not link.amount_usd:
        raise HTTPException(status_code=400, detail="Amount must be set on this payment link")

    # Load merchant for fee calculation
    merchant_result = await db.execute(
        select(Merchant).where(Merchant.id == link.merchant_id)
    )
    merchant = merchant_result.scalar_one()

    payment = await create_payment_session(
        db=db,
        merchant=merchant,
        amount_usd=link.amount_usd,
        token=token,
        chain=chain,
        payment_link_id=link.id,
    )

    qr_data = f"{chain}:{payment.deposit_address}?amount={payment.amount_crypto}&token={token}"
    qr_code = generate_qr_code_base64(qr_data)

    return {
        "payment_id": payment.id,
        "deposit_address": payment.deposit_address,
        "amount_crypto": str(payment.amount_crypto),
        "amount_usd": str(link.amount_usd),
        "token": token,
        "chain": chain,
        "qr_code_base64": qr_code,
        "expires_at": payment.expires_at.isoformat(),
    }


@router.get("/status/{payment_id}", response_model=CheckoutStatusResponse)
async def check_payment_status(
    payment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint — poll for payment status."""
    result = await db.execute(
        select(Payment).where(Payment.id == payment_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return CheckoutStatusResponse(
        payment_id=payment.id,
        status=payment.status,
        confirmations=payment.confirmations,
        required_confirmations=payment.required_confirmations,
        amount_usd=payment.amount_usd,
        amount_crypto=payment.amount_crypto,
        token=payment.token,
        chain=payment.chain,
        deposit_address=payment.deposit_address,
        expires_at=payment.expires_at,
    )
