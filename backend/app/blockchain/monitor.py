"""Blockchain transaction monitor — coordinates watching addresses across chains."""

import logging
from app.blockchain.ethereum import EVMProvider
from app.blockchain.solana import SolanaProvider
from app.blockchain.bitcoin import BitcoinProvider
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def get_provider(chain: str):
    """Get the blockchain provider for a given chain."""
    chain = chain.lower()

    if chain in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
        rpc_urls = {
            "ethereum": settings.ethereum_rpc_ws,
            "polygon": settings.polygon_rpc_ws,
            "bsc": settings.bsc_rpc_ws,
            "arbitrum": settings.arbitrum_rpc_ws,
            "base": settings.base_rpc_ws,
        }
        return EVMProvider(chain, rpc_urls.get(chain, ""))
    elif chain == "solana":
        return SolanaProvider(settings.solana_rpc_ws)
    elif chain == "bitcoin":
        return BitcoinProvider(settings.bitcoin_rpc_url)
    else:
        raise ValueError(f"Unsupported chain: {chain}")
