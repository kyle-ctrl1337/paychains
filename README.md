# PayChains

The non-custodial crypto billing API for SaaS. Recurring subscriptions, automatic dunning, real-time webhooks — payments go straight to your wallet.

## Features

- **Non-custodial** — your keys, your crypto. We never touch your funds.
- **Recurring billing** — weekly, monthly, quarterly, yearly subscriptions with smart dunning
- **5 EVM chains** — Ethereum, Polygon, BSC, Arbitrum, Base (Solana + Bitcoin coming soon)
- **Developer SDKs** — `npm install paychains` / `pip install paychains`
- **Hosted checkout** — beautiful, embeddable payment pages with QR codes
- **Real-time webhooks** — HMAC-signed events with exponential backoff retries
- **Analytics dashboard** — volume, revenue, and chain breakdown charts

## Quick Start

### 1. Sign up
Create an account at [paychains.dev](https://paychains.dev) to get your API keys.

### 2. Set your wallet address
Go to Dashboard → Settings and paste your EVM wallet address.

### 3. Accept payments

```bash
npm install paychains
```

```javascript
import PayChains from 'paychains';
const pc = new PayChains({ apiKey: 'pc_live_...' });

const payment = await pc.payments.create({
  amount_usd: 49.99,
  chain: 'polygon',
  token: 'USDC'
});
// payment.deposit_address — your wallet address
```

## Self-Hosting

```bash
git clone https://github.com/your-org/paychains.git
cp .env.example .env
# Edit .env with your configuration
docker-compose up
```

Visit `http://localhost:5173` for the frontend and `http://localhost:8000/docs` for API documentation.

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Celery, Redis, PostgreSQL
- **Frontend:** SvelteKit, Svelte 5, TailwindCSS 4, Chart.js
- **Blockchain:** web3.py, BIP-44 HD wallets, EVM multi-chain
- **SDKs:** TypeScript (npm), Python (pip) with sync + async clients

## License

MIT
