# PayChains JavaScript/TypeScript SDK

Official JavaScript SDK for the [PayChains](https://paychains.dev) non-custodial crypto billing API.

## Install

```bash
npm install paychains
```

## Quick Start

```typescript
import PayChains from 'paychains';

const pc = new PayChains({ apiKey: 'pc_live_...' });

// Payments go directly to your wallet.
// Set your xpub key in the dashboard first.
const payment = await pc.payments.create({
  amount_usd: 49.99,
  chain: 'polygon',
  token: 'USDC'
});
// payment.deposit_address is derived from YOUR xpub
console.log(payment.deposit_address);
```

## Non-Custodial

PayChains never holds your funds. Deposit addresses are derived from your wallet's extended public key (xpub). Your private keys never leave your wallet.

## Webhook Verification

```typescript
const isValid = pc.webhooks.verifySignature(
  requestBody,
  headers['x-signature'],
  webhookSecret
);
```

## License

MIT
