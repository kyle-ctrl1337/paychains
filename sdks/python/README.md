# PayChains Python SDK

Official Python SDK for the [PayChains](https://paychains.dev) non-custodial crypto billing API.

## Install

```bash
pip install paychains
```

## Quick Start

```python
from paychains import PayChains

pc = PayChains(api_key="pc_live_...")

# Payments go directly to your wallet.
# Set your xpub key in the dashboard first.
payment = pc.payments.create(
    amount_usd=49.99,
    chain="polygon",
    token="USDC"
)
# payment["deposit_address"] is derived from YOUR xpub
print(payment["deposit_address"])
```

## Async Support

```python
from paychains import AsyncPayChains

pc = AsyncPayChains(api_key="pc_live_...")
payment = await pc.payments.create(amount_usd=49.99, chain="polygon", token="USDC")
```

## Non-Custodial

PayChains never holds your funds. Deposit addresses are derived from your wallet's extended public key (xpub). Your private keys never leave your wallet.

## License

MIT
