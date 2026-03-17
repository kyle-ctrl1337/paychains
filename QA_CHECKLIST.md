# PayChains QA Checklist

## Registration
- [ ] Landing page loads, no console errors
- [ ] "Get started free" → register → see API keys → dashboard
- [ ] xpub setup banner shown on dashboard

## Wallet Setup
- [ ] Settings → enter xpub → save → see preview addresses
- [ ] Banner disappears after xpub saved

## Payment Flow
- [ ] Create payment link → copy checkout URL
- [ ] Open checkout in incognito → chain selector shows
- [ ] Solana/Bitcoin greyed out with "Coming Soon"
- [ ] Select Polygon + USDC → deposit address + QR + timer shown
- [ ] Copy address works

## Plan Upgrade
- [ ] Settings shows current plan (free) + upgrade button
- [ ] Click "Upgrade to Pro" → upgrade checkout page loads
- [ ] Shows $49.00 USDC payment details
- [ ] (Manual) Send crypto → plan upgrades to Pro

## Dashboard
- [ ] Overview: stats + charts load
- [ ] Payments: table with filters
- [ ] Payment Links: create + copy
- [ ] Subscriptions: loads
- [ ] Payouts: shows "funds go directly to wallet"
- [ ] Settings: plan + keys + webhook + xpub

## API
- [ ] GET /api/v1/health → 200
- [ ] POST /api/v1/payments/create → deposit address returned
- [ ] Free plan: 101st payment → limit error
- [ ] GET /api/v1/billing/current-plan → returns plan info
- [ ] POST /api/v1/billing/upgrade?plan=pro → creates payment

## Docs
- [ ] /docs loads with all sections
- [ ] Interactive playground works

## Legal
- [ ] /terms loads
- [ ] /privacy loads

## Infrastructure
- [ ] Celery worker starts (check Railway logs)
- [ ] Celery beat starts (check Railway logs)
- [ ] Redis connected
- [ ] Price feed working (CoinGecko API key configured)
- [ ] Webhook delivery works when payment completes
