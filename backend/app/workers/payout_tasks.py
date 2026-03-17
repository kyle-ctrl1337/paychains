import logging
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def process_payout(payout_id: str):
    """Process a merchant payout on-chain (Phase 6)."""
    logger.info(f"Processing payout {payout_id} — not yet implemented")
