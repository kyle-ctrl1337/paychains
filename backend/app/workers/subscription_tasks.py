"""Subscription billing engine — handles recurring payment creation and dunning."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta

from app.workers.celery_app import celery_app
from app.models.subscription import Subscription
from app.models.payment import Payment
from app.models.merchant import Merchant
from app.models.webhook_event import WebhookEvent
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

INTERVAL_DELTAS = {
    "weekly": relativedelta(weeks=1),
    "monthly": relativedelta(months=1),
    "quarterly": relativedelta(months=3),
    "yearly": relativedelta(years=1),
}

# Retry delays in hours for dunning
RETRY_DELAYS_HOURS = [24, 48, 72]

CONFIRMATIONS = {
    "ethereum": 3, "polygon": 5, "bsc": 5,
    "arbitrum": 1, "base": 1, "solana": 1, "bitcoin": 3,
}

FEES = {
    "free": Decimal("0.02"),
    "pro": Decimal("0.01"),
    "enterprise": Decimal("0.005"),
}


def _get_sync_session():
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(db_url)
    return Session(engine)


def _fire_webhook(session: Session, merchant_id, event_type: str, data: dict):
    event = WebhookEvent(
        merchant_id=merchant_id,
        event_type=event_type,
        payload={
            "event": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    session.add(event)
    session.flush()
    from app.workers.webhook_tasks import deliver_webhook
    deliver_webhook.delay(str(event.id))


@celery_app.task
def check_due_subscriptions():
    """Check for subscriptions that are due for payment."""
    now = datetime.now(timezone.utc)
    with _get_sync_session() as session:
        result = session.execute(
            select(Subscription).where(
                Subscription.status.in_(["active", "past_due"]),
                Subscription.next_payment_at <= now,
            )
        )
        due_subs = result.scalars().all()
        logger.info(f"Found {len(due_subs)} subscriptions due for payment")

        for sub in due_subs:
            process_subscription_payment.delay(str(sub.id))


@celery_app.task(bind=True, max_retries=3)
def process_subscription_payment(self, subscription_id: str):
    """Create a payment for a subscription billing cycle."""
    with _get_sync_session() as session:
        sub = session.get(Subscription, subscription_id)
        if not sub or sub.status not in ("active", "past_due"):
            return

        merchant = session.get(Merchant, sub.merchant_id)
        if not merchant:
            return

        # Determine chain and token
        chain = sub.preferred_chain or "polygon"
        token = sub.preferred_token or "USDC"
        fee_pct = FEES.get(merchant.plan, Decimal("0.02"))

        # Create a payment record for this billing cycle
        import hashlib
        idx = int(hashlib.sha256(str(sub.id).encode()).hexdigest()[:8], 16) % (2**31)
        payment_count = session.query(Payment).filter_by(subscription_id=sub.id).count()
        seed_material = f"{chain}:{idx}:{payment_count + 1}"
        addr_hash = hashlib.sha256(seed_material.encode()).hexdigest()

        if chain in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
            deposit_address = f"0x{addr_hash[:40]}"
        elif chain == "bitcoin":
            deposit_address = f"bc1q{addr_hash[:38]}"
        elif chain == "solana":
            deposit_address = addr_hash[:44]
        else:
            deposit_address = f"0x{addr_hash[:40]}"

        payment = Payment(
            merchant_id=merchant.id,
            subscription_id=sub.id,
            amount_usd=sub.amount_usd,
            amount_crypto=sub.amount_usd,  # Stablecoin 1:1 for now
            token=token,
            chain=chain,
            deposit_address=deposit_address,
            required_confirmations=CONFIRMATIONS.get(chain, 3),
            fee_percentage=fee_pct,
            fee_amount_usd=sub.amount_usd * fee_pct,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=48),
        )
        session.add(payment)

        # Fire subscription payment due webhook
        _fire_webhook(session, merchant.id, "subscription.payment_due", {
            "subscription_id": str(sub.id),
            "payment_id": str(payment.id),
            "plan_name": sub.plan_name,
            "amount_usd": str(sub.amount_usd),
            "deposit_address": deposit_address,
            "chain": chain,
            "token": token,
        })

        # Send email notification if customer email exists
        if sub.customer_email:
            try:
                from app.services.email_service import send_subscription_invoice
                send_subscription_invoice(sub.customer_email, {
                    "plan_name": sub.plan_name,
                    "amount_usd": str(sub.amount_usd),
                    "due_date": payment.expires_at.strftime("%Y-%m-%d %H:%M UTC"),
                })
            except Exception as e:
                logger.error(f"Failed to send invoice email: {e}")

        # Advance the billing period
        delta = INTERVAL_DELTAS.get(sub.interval, relativedelta(months=1))
        sub.current_period_start = sub.current_period_end
        sub.current_period_end = sub.current_period_start + delta
        sub.next_payment_at = sub.current_period_end
        sub.retry_count = 0

        logger.info(
            f"Subscription {subscription_id}: payment created, "
            f"period {sub.current_period_start} - {sub.current_period_end}"
        )

        session.commit()


@celery_app.task
def handle_subscription_dunning(subscription_id: str):
    """Handle failed subscription payment — retry with exponential backoff."""
    with _get_sync_session() as session:
        sub = session.get(Subscription, subscription_id)
        if not sub:
            return

        sub.retry_count += 1

        if sub.retry_count > sub.max_retries:
            sub.status = "past_due"
            _fire_webhook(session, sub.merchant_id, "subscription.past_due", {
                "subscription_id": str(sub.id),
                "plan_name": sub.plan_name,
                "retry_count": sub.retry_count,
            })
            logger.warning(f"Subscription {subscription_id} moved to past_due after {sub.retry_count} retries")
        else:
            # Schedule retry
            delay_hours = RETRY_DELAYS_HOURS[min(sub.retry_count - 1, len(RETRY_DELAYS_HOURS) - 1)]
            sub.next_payment_at = datetime.now(timezone.utc) + timedelta(hours=delay_hours)
            logger.info(f"Subscription {subscription_id}: retry {sub.retry_count} scheduled in {delay_hours}h")

        session.commit()
