from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    tx_hash: str
    from_address: str
    to_address: str
    amount: Decimal
    token: str
    block_number: int
    confirmations: int


class ChainProvider(ABC):
    """Abstract base class for blockchain providers."""

    @abstractmethod
    async def generate_address(self, seed: bytes, account_index: int, address_index: int) -> str:
        """Generate a deposit address using HD wallet derivation."""
        ...

    @abstractmethod
    async def get_balance(self, address: str, token: str | None = None) -> Decimal:
        """Get the balance of an address."""
        ...

    @abstractmethod
    async def get_transaction(self, tx_hash: str) -> Transaction | None:
        """Get transaction details by hash."""
        ...

    @abstractmethod
    async def get_confirmations(self, tx_hash: str) -> int:
        """Get the number of confirmations for a transaction."""
        ...

    @abstractmethod
    async def subscribe_address(self, address: str, callback):
        """Subscribe to incoming transactions for an address."""
        ...

    @abstractmethod
    def get_required_confirmations(self) -> int:
        """Return the number of confirmations required for this chain."""
        ...
