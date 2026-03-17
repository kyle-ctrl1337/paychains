"""Blockchain monitoring tasks — polls for incoming payments and counts confirmations."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from app.workers.celery_app import celery_app
from app.models.payment import Payment
from app.models.webhook_event import WebhookEvent
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_sync_session():
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(db_url)
    return Session(engine)


def _fire_webhook(session: Session, payment: Payment, event_type: str):
    """Create a webhook event for a payment status change."""
    event = WebhookEvent(
        merchant_id=payment.merchant_id,
        event_type=event_type,
        payload={
            "event": event_type,
            "data": {
                "payment_id": str(payment.id),
                "status": payment.status,
                "amount_usd": str(payment.amount_usd),
                "amount_crypto": str(payment.amount_crypto) if payment.amount_crypto else None,
                "token": payment.token,
                "chain": payment.chain,
                "tx_hash": payment.tx_hash,
                "confirmations": payment.confirmations,
                "deposit_address": payment.deposit_address,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
    session.add(event)
    session.flush()

    from app.workers.webhook_tasks import deliver_webhook
    deliver_webhook.delay(str(event.id))


@celery_app.task
def expire_pending_payments():
    """Mark pending payments that have passed their expiration as expired."""
    now = datetime.now(timezone.utc)
    with _get_sync_session() as session:
        result = session.execute(
            select(Payment).where(
                Payment.status == "pending",
                Payment.expires_at <= now,
            )
        )
        expired = result.scalars().all()
        for payment in expired:
            payment.status = "expired"
            _fire_webhook(session, payment, "payment.failed")
            logger.info(f"Payment {payment.id} expired")

        if expired:
            session.commit()
            logger.info(f"Expired {len(expired)} pending payments")


@celery_app.task
def poll_pending_payments():
    """Poll blockchain for pending/confirming payments."""
    import asyncio
    asyncio.run(_async_poll_payments())


async def _async_poll_payments():
    from app.blockchain.monitor import get_provider

    with _get_sync_session() as session:
        result = session.execute(
            select(Payment).where(
                Payment.status.in_(["pending", "confirming"]),
                Payment.expires_at > datetime.now(timezone.utc),
            )
        )
        payments = result.scalars().all()
        if not payments:
            return

        logger.info(f"Polling {len(payments)} active payments")

        for payment in payments:
            try:
                provider = get_provider(payment.chain)

                if payment.status == "pending":
                    balance = await provider.get_balance(
                        payment.deposit_address, payment.token
                    )
                    if balance > 0:
                        payment.status = "confirming"
                        payment.amount_crypto = balance
                        logger.info(f"Payment {payment.id}: {balance} {payment.token} detected")
                        _fire_webhook(session, payment, "payment.confirming")

                elif payment.status == "confirming" and payment.tx_hash:
                    confs = await provider.get_confirmations(payment.tx_hash)
                    payment.confirmations = confs
                    if confs >= payment.required_confirmations:
                        payment.status = "completed"
                        payment.completed_at = datetime.now(timezone.utc)
                        payment.fee_amount_usd = payment.amount_usd * payment.fee_percentage
                        logger.info(f"Payment {payment.id}: completed ({confs} confs)")
                        _fire_webhook(session, payment, "payment.completed")

            except Exception as e:
                logger.error(f"Error polling payment {payment.id}: {e}")

        session.commit()


@celery_app.task
def count_confirmations(payment_id: str, tx_hash: str):
    """Check confirmations for a specific transaction."""
    import asyncio
    asyncio.run(_async_count_confirmations(payment_id, tx_hash))


async def _async_count_confirmations(payment_id: str, tx_hash: str):
    from app.blockchain.monitor import get_provider

    with _get_sync_session() as session:
        payment = session.get(Payment, payment_id)
        if not payment or payment.status not in ("confirming", "pending"):
            return

        try:
            provider = get_provider(payment.chain)
            confs = await provider.get_confirmations(tx_hash)
            payment.confirmations = confs
            payment.tx_hash = tx_hash

            if confs >= payment.required_confirmations:
                payment.status = "completed"
                payment.completed_at = datetime.now(timezone.utc)
                payment.fee_amount_usd = payment.amount_usd * payment.fee_percentage
                _fire_webhook(session, payment, "payment.completed")
            elif payment.status == "pending":
                payment.status = "confirming"
                _fire_webhook(session, payment, "payment.confirming")

            session.commit()
        except Exception as e:
            logger.error(f"Error counting confirmations for {payment_id}: {e}")
