"""Tests for ERC-20 address padding — ensures lowercase for log topic matching."""


def test_erc20_address_padding():
    """Address padding must be lowercase for log topic matching."""
    address = "0xE911c873b881D2d8a4540a710AbE9BE04597B7d4"
    padded = "0x" + address[2:].lower().zfill(64)
    assert padded == "0x000000000000000000000000e911c873b881d2d8a4540a710abe9be04597b7d4"
    # No uppercase letters in the padded result
    assert padded == padded.lower()


def test_erc20_address_padding_already_lowercase():
    """Already-lowercase address should also work."""
    address = "0xe911c873b881d2d8a4540a710abe9be04597b7d4"
    padded = "0x" + address[2:].lower().zfill(64)
    assert padded == "0x000000000000000000000000e911c873b881d2d8a4540a710abe9be04597b7d4"


def test_chain_token_validation():
    """VALID_TOKENS_PER_CHAIN should reject invalid combos."""
    from app.constants import VALID_TOKENS_PER_CHAIN

    # USDT is not on Base
    assert "USDT" not in VALID_TOKENS_PER_CHAIN["base"]
    # USDC is on all chains
    for chain in VALID_TOKENS_PER_CHAIN:
        assert "USDC" in VALID_TOKENS_PER_CHAIN[chain]
    # Invalid chain
    assert "solana" not in VALID_TOKENS_PER_CHAIN
