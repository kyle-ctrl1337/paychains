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
