"""Bitcoin chain provider."""

import logging
from decimal import Decimal

from app.blockchain.base import ChainProvider, Transaction

logger = logging.getLogger(__name__)


class BitcoinProvider(ChainProvider):
    """Provider for Bitcoin."""

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    async def generate_address(self, seed: bytes, account_index: int, address_index: int) -> str:
        raise NotImplementedError("Bitcoin HD wallet coming in Phase 5")

    async def get_balance(self, address: str, token: str | None = None) -> Decimal:
        raise NotImplementedError("Coming in Phase 5")

    async def get_transaction(self, tx_hash: str) -> Transaction | None:
        raise NotImplementedError("Coming in Phase 5")

    async def get_confirmations(self, tx_hash: str) -> int:
        raise NotImplementedError("Coming in Phase 5")

    async def subscribe_address(self, address: str, callback):
        raise NotImplementedError("Coming in Phase 5")

    def get_required_confirmations(self) -> int:
        return 3
