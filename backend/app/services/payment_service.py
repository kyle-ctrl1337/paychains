"""Payment service — handles address generation and payment creation."""

import logging
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.blockchain.wallet import derive_address_from_xpub
from app.config import get_settings
from app.models.merchant import Merchant
from app.models.payment import Payment
from app.utils.pricing import usd_to_crypto

logger = logging.getLogger(__name__)
settings = get_settings()

CONFIRMATIONS = {
    "ethereum": 3,
    "polygon": 5,
    "bsc": 5,
    "arbitrum": 1,
    "base": 1,
    "solana": 1,
    "bitcoin": 3,
}

# Chains that are fully supported — others show "Coming Soon"
SUPPORTED_CHAINS = {"ethereum", "polygon", "bsc", "arbitrum", "base"}
COMING_SOON_CHAINS = {"solana", "bitcoin"}

PLAN_PAYMENT_LIMITS = {
    "free": 100,
    "pro": 2000,
    "enterprise": 999999,
}


async def get_next_payment_index(db: AsyncSession, merchant_id: uuid.UUID) -> int:
    """Get the next payment index for address derivation."""
    result = await db.execute(
        select(func.count(Payment.id)).where(Payment.merchant_id == merchant_id)
    )
    return (result.scalar() or 0) + 1


async def get_merchant_index(db: AsyncSession, merchant_id: uuid.UUID) -> int:
    """Derive a deterministic merchant index from UUID (first 4 bytes as int)."""
    return int(str(merchant_id).replace("-", "")[:8], 16) % (2**31)


async def create_payment_session(
    db: AsyncSession,
    merchant: Merchant,
    amount_usd: Decimal,
    token: str,
    chain: str,
    payment_link_id: uuid.UUID | None = None,
    subscription_id: uuid.UUID | None = None,
    metadata: dict | None = None,
) -> Payment:
    """Create a payment with a deposit address derived from merchant's xpub (non-custodial)."""
    chain = chain.lower()
    token = token.upper()

    if chain not in CONFIRMATIONS:
        raise ValueError(f"Unsupported chain: {chain}")

    if chain in COMING_SOON_CHAINS:
        raise ValueError(f"{chain.capitalize()} support is coming soon")

    # Check plan payment limits
    start_of_month = datetime.now(timezone.utc).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    payment_count = await db.scalar(
        select(func.count(Payment.id))
        .where(Payment.merchant_id == merchant.id)
        .where(Payment.created_at >= start_of_month)
    )
    limit = PLAN_PAYMENT_LIMITS.get(merchant.plan, 100)
    if (payment_count or 0) >= limit:
        raise ValueError(
            f"Monthly payment limit reached ({limit} payments). "
            f"Upgrade your plan at paychains.dev/dashboard/settings"
        )

    # Convert USD to crypto amount
    amount_crypto = await usd_to_crypto(amount_usd, token)

    # Round to appropriate decimal places
    DISPLAY_DECIMALS = {"USDC": 2, "USDT": 2, "DAI": 2, "ETH": 6, "MATIC": 4, "BNB": 6}
    decimals = DISPLAY_DECIMALS.get(token, 8)
    amount_crypto = round(amount_crypto, decimals)

    # Derive deposit address from merchant's xpub (non-custodial)
    payment_idx = await get_next_payment_index(db, merchant.id)

    if merchant.xpub_key:
        address = derive_address_from_xpub(merchant.xpub_key, payment_idx, chain)
    else:
        raise ValueError(
            "Wallet not configured. Please add your wallet address in Settings before accepting payments."
        )

    payment = Payment(
        merchant_id=merchant.id,
        payment_link_id=payment_link_id,
        subscription_id=subscription_id,
        amount_usd=amount_usd,
        amount_crypto=amount_crypto,
        token=token,
        chain=chain,
        deposit_address=address,
        required_confirmations=CONFIRMATIONS[chain],
        fee_percentage=Decimal("0"),
        fee_amount_usd=Decimal("0"),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        metadata_=metadata or {},
    )
    db.add(payment)
    await db.flush()
    await db.refresh(payment)

    logger.info(
        f"Payment {payment.id} created: {amount_usd} USD = {amount_crypto} {token} "
        f"on {chain}, deposit: {address}"
    )

    return payment
