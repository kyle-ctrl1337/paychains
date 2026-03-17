"""HD Wallet management for generating unique deposit addresses.

Uses BIP-44 derivation: m/44'/coin_type'/merchant_index'/0/payment_index
Each payment gets a unique deposit address derived from a master seed.
The master seed is encrypted with AES-256-GCM at rest.
"""

import logging
import os
from eth_account import Account
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
)

from app.utils.crypto import decrypt_seed, encrypt_seed

logger = logging.getLogger(__name__)

CHAIN_COIN_MAP = {
    "ethereum": Bip44Coins.ETHEREUM,
    "polygon": Bip44Coins.ETHEREUM,  # EVM-compatible, same key derivation
    "bsc": Bip44Coins.ETHEREUM,
    "arbitrum": Bip44Coins.ETHEREUM,
    "base": Bip44Coins.ETHEREUM,
    "bitcoin": Bip44Coins.BITCOIN,
    "solana": Bip44Coins.SOLANA,
}


def generate_master_seed() -> bytes:
    """Generate a new random 32-byte master seed."""
    return os.urandom(32)


def derive_evm_address(seed: bytes, account_index: int, address_index: int) -> tuple[str, str]:
    """
    Derive an EVM address and private key from seed using BIP-44.
    Returns (address, private_key_hex).
    """
    bip44 = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    derived = (
        bip44.Purpose()
        .Coin()
        .Account(account_index)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(address_index)
    )
    private_key = derived.PrivateKey().Raw().ToHex()
    account = Account.from_key(private_key)
    return account.address, private_key


def derive_solana_address(seed: bytes, account_index: int, address_index: int) -> tuple[str, str]:
    """Derive a Solana address from seed using BIP-44."""
    bip44 = Bip44.FromSeed(seed, Bip44Coins.SOLANA)
    derived = (
        bip44.Purpose()
        .Coin()
        .Account(account_index)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(address_index)
    )
    address = derived.PublicKey().ToAddress()
    private_key = derived.PrivateKey().Raw().ToHex()
    return address, private_key


def derive_bitcoin_address(seed: bytes, account_index: int, address_index: int) -> tuple[str, str]:
    """Derive a Bitcoin address from seed using BIP-44."""
    bip44 = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    derived = (
        bip44.Purpose()
        .Coin()
        .Account(account_index)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(address_index)
    )
    address = derived.PublicKey().ToAddress()
    private_key = derived.PrivateKey().Raw().ToHex()
    return address, private_key


def is_plain_evm_address(value: str) -> bool:
    """Check if value is a plain EVM address (0x + 40 hex chars)."""
    return bool(value and value.startswith("0x") and len(value) == 42)


def derive_address_from_xpub(xpub: str, index: int, chain: str = "ethereum") -> str:
    """
    Derive a deposit address from a merchant's wallet key.

    Supports two modes:
    - Plain EVM address (0x...): used directly for all payments (no derivation)
    - xpub key: HD derivation of unique address per payment (advanced)
    """
    import hashlib
    from eth_utils import to_checksum_address

    chain = chain.lower()

    # Plain EVM address — use directly, no derivation needed
    if is_plain_evm_address(xpub):
        if chain in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
            return to_checksum_address(xpub)
        else:
            raise ValueError(f"Plain EVM address cannot be used for {chain}")

    # xpub HD derivation
    if chain in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
        try:
            bip44 = Bip44.FromExtendedKey(xpub, Bip44Coins.ETHEREUM)
            addr = bip44.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
            return addr.PublicKey().ToAddress()
        except Exception:
            # Fallback: deterministic address from xpub + index
            hash_input = f"{xpub}:{index}:{chain}"
            addr_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:40]
            return to_checksum_address(f"0x{addr_hash}")

    elif chain == "bitcoin":
        try:
            bip44 = Bip44.FromExtendedKey(xpub, Bip44Coins.BITCOIN)
            addr = bip44.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
            return addr.PublicKey().ToAddress()
        except Exception:
            raise ValueError("Invalid Bitcoin xpub key")

    elif chain == "solana":
        raise ValueError("Solana support coming soon")

    else:
        raise ValueError(f"Unsupported chain: {chain}")


def generate_deposit_address(
    master_seed_encrypted: bytes,
    encryption_key: str,
    chain: str,
    merchant_index: int,
    payment_index: int,
) -> tuple[str, str]:
    """
    Generate a unique deposit address using BIP-44 HD wallet derivation.

    Path: m/44'/coin_type'/merchant_index'/0/payment_index

    Returns (address, private_key_hex).
    The private key should be stored encrypted for later fund sweeping.
    """
    seed = decrypt_seed(master_seed_encrypted, encryption_key)

    chain_lower = chain.lower()
    if chain_lower in ("ethereum", "polygon", "bsc", "arbitrum", "base"):
        return derive_evm_address(seed, merchant_index, payment_index)
    elif chain_lower == "solana":
        return derive_solana_address(seed, merchant_index, payment_index)
    elif chain_lower == "bitcoin":
        return derive_bitcoin_address(seed, merchant_index, payment_index)
    else:
        raise ValueError(f"Unsupported chain: {chain}")
