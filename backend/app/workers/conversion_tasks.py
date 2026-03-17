"""Auto-conversion tasks — swaps received crypto to stablecoins via 0x API."""

import logging
from datetime import datetime, timezone
from decimal import Decimal

import httpx
from sqlalchemy import select

from app.workers.celery_app import celery_app
from app.config import get_settings
from app.models.payment import Payment
from app.models.merchant import Merchant

logger = logging.getLogger(__name__)
settings = get_settings()

# Token contract addresses on each chain (mainnet)
TOKEN_ADDRESSES = {
    "ethereum": {
        "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    },
    "polygon": {
        "MATIC": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
    },
    "bsc": {
        "BNB": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
    },
    "arbitrum": {
        "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    },
    "base": {
        "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    },
}

# 0x API chain IDs
CHAIN_IDS = {
    "ethereum": 1,
    "polygon": 137,
    "bsc": 56,
    "arbitrum": 42161,
    "base": 8453,
}


def _get_sync_session():
    from app.database import SyncSession
    return SyncSession()


def _get_swap_quote(
    chain: str,
    sell_token: str,
    buy_token: str,
    sell_amount: str,
    taker_address: str,
) -> dict | None:
    """Get a swap quote from 0x API."""
    if not settings.zerox_api_key:
        logger.warning("0x API key not configured — skipping conversion")
        return None

    chain_id = CHAIN_IDS.get(chain)
    if not chain_id:
        logger.warning(f"Chain {chain} not supported for auto-conversion")
        return None

    try:
        resp = httpx.get(
            f"https://api.0x.org/swap/permit2/quote",
            params={
                "chainId": chain_id,
                "sellToken": sell_token,
                "buyToken": buy_token,
                "sellAmount": sell_amount,
                "taker": taker_address,
            },
            headers={
                "0x-api-key": settings.zerox_api_key,
                "0x-version": "v2",
            },
            timeout=15.0,
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"0x API error: {e.response.status_code} — {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"0x API request failed: {e}")
        return None


@celery_app.task(bind=True, max_retries=0)
def auto_convert_payment(self, payment_id: str, target_token: str = "USDC"):
    """Auto-conversion is disabled in non-custodial mode.

    PayChains never holds merchant funds, so we cannot execute swaps.
    Merchants receive crypto directly in their own wallet and can swap
    using their preferred DEX/exchange.
    """
    logger.info(
        f"Auto-conversion skipped for payment {payment_id}: "
        f"non-custodial mode — merchant controls their own funds. "
        f"Auto-conversion requires merchant wallet connection (coming soon)."
    )
    return
