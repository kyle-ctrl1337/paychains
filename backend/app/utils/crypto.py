import secrets
import hashlib
import hmac
import json

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_api_key(prefix: str = "pc") -> str:
    """Generate a random API key with a prefix."""
    random_part = secrets.token_hex(28)
    return f"{prefix}_{random_part}"


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage. Using SHA-256 for fast lookups."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def generate_webhook_secret() -> str:
    """Generate a webhook signing secret."""
    return f"whsec_{secrets.token_hex(24)}"


def sign_webhook_payload(payload: str, secret: str) -> str:
    """Sign a webhook payload with HMAC-SHA256."""
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()


def verify_webhook_signature(payload: str, secret: str, signature: str) -> bool:
    """Verify a webhook signature."""
    expected = sign_webhook_payload(payload, secret)
    return hmac.compare_digest(expected, signature)


def encrypt_seed(seed: bytes, key_hex: str) -> bytes:
    """Encrypt a wallet seed with AES-256-GCM."""
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, seed, None)
    return nonce + ciphertext


def decrypt_seed(encrypted: bytes, key_hex: str) -> bytes:
    """Decrypt a wallet seed with AES-256-GCM."""
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    nonce = encrypted[:12]
    ciphertext = encrypted[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)
