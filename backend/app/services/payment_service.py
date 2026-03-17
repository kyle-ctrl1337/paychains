"""Payment service — handles address generation and payment creation."""

import logging
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.blockchain.wallet import generate_deposit_address
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

FEES = {
    "free": Decimal("0.02"),
    "pro": Decimal("0.01"),
    "enterprise": Decimal("0.005"),
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
    """Create a payment with a unique HD-wallet deposit address."""
    chain = chain.lower()
    token = token.upper()

    if chain not in CONFIRMATIONS:
        raise ValueError(f"Unsupported chain: {chain}")

    # Convert USD to crypto amount
    amount_crypto = await usd_to_crypto(amount_usd, token)
    fee_pct = FEES.get(merchant.plan, Decimal("0.02"))

    # Generate unique deposit address via HD wallet
    merchant_idx = await get_merchant_index(db, merchant.id)
    payment_idx = await get_next_payment_index(db, merchant.id)

    if settings.wallet_encryption_key and settings.wallet_master_seed:
        # Use real HD wallet derivation
        master_seed_encrypted = bytes.fromhex(settings.wallet_master_seed)
        address, _private_key = generate_deposit_address(
            master_seed_encrypted,
            settings.wallet_encryption_key,
            chain,
            merchant_idx,
            payment_idx,
        )
    else:
        # Fallback for development — deterministic but not real HD wallet
        import hashlib
        seed_material = f"{chain}:{merchant_idx}:{payment_idx}"
        addr_hash = hashlib.sha256(seed_material.encode()).hexdigest()
        if chain in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
            address = f"0x{addr_hash[:40]}"
        elif chain == "bitcoin":
            address = f"bc1q{addr_hash[:38]}"
        elif chain == "solana":
            address = addr_hash[:44]
        else:
            address = f"0x{addr_hash[:40]}"

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
        fee_percentage=fee_pct,
        fee_amount_usd=amount_usd * fee_pct,
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
