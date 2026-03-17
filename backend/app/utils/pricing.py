import logging
import httpx
from decimal import Decimal

from app.config import get_settings

logger = logging.getLogger(__name__)

# CoinGecko token ID mapping
TOKEN_IDS = {
    "ETH": "ethereum",
    "BTC": "bitcoin",
    "MATIC": "matic-network",
    "BNB": "binancecoin",
    "SOL": "solana",
    "USDC": "usd-coin",
    "USDT": "tether",
    "DAI": "dai",
}

# Cache prices for 60 seconds
_price_cache: dict[str, tuple[Decimal, float]] = {}
CACHE_TTL = 60.0


async def get_token_price_usd(token: str) -> Decimal:
    """Get the current USD price of a token from CoinGecko."""
    import time

    token_upper = token.upper()

    # Stablecoins are always ~$1
    if token_upper in ("USDC", "USDT", "DAI"):
        return Decimal("1.00")

    # Check cache
    if token_upper in _price_cache:
        price, cached_at = _price_cache[token_upper]
        if time.time() - cached_at < CACHE_TTL:
            return price

    coingecko_id = TOKEN_IDS.get(token_upper)
    if not coingecko_id:
        raise ValueError(f"Unsupported token: {token}")

    settings = get_settings()
    headers: dict[str, str] = {}
    params: dict[str, str] = {"ids": coingecko_id, "vs_currencies": "usd"}

    if settings.coingecko_api_key:
        headers["x-cg-demo-api-key"] = settings.coingecko_api_key

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params=params,
            headers=headers,
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        price = Decimal(str(data[coingecko_id]["usd"]))

    _price_cache[token_upper] = (price, time.time())
    logger.debug(f"Price for {token_upper}: ${price}")
    return price


async def usd_to_crypto(amount_usd: Decimal, token: str) -> Decimal:
    """Convert a USD amount to the equivalent crypto amount."""
    price = await get_token_price_usd(token)
    if price == 0:
        raise ValueError(f"Price for {token} is zero")
    return amount_usd / price
