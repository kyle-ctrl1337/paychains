import logging
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def auto_convert_payment(payment_id: str, target_token: str = "USDC"):
    """Auto-convert received crypto to stablecoin via DEX (Phase 6)."""
    logger.info(f"Auto-conversion for payment {payment_id} to {target_token} — not yet implemented")
