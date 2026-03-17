<script lang="ts">
	import { auth } from '$lib/stores/auth';

	let isLoggedIn = $state(false);
	let testApiKey = $state('');
	let tryItEndpoint = $state('');
	let tryItMethod = $state('GET');
	let tryItBody = $state('');
	let tryItResponse = $state('');
	let tryItLoading = $state(false);
	let tryItStatus = $state(0);

	auth.subscribe((s) => {
		isLoggedIn = !!s.token;
		if (s.apiKeyTest) testApiKey = s.apiKeyTest;
	});

	const API_BASE = import.meta.env.VITE_API_URL || 'https://backend-api-production-ab9c.up.railway.app/api/v1';

	async function runTryIt() {
		if (!testApiKey || !tryItEndpoint) return;
		tryItLoading = true;
		tryItResponse = '';
		tryItStatus = 0;
		try {
			const opts: RequestInit = {
				method: tryItMethod,
				headers: {
					'X-API-Key': testApiKey,
					'Content-Type': 'application/json'
				}
			};
			if (tryItMethod !== 'GET' && tryItBody.trim()) {
				opts.body = tryItBody;
			}
			const res = await fetch(`${API_BASE}${tryItEndpoint}`, opts);
			tryItStatus = res.status;
			const data = await res.json().catch(() => null);
			tryItResponse = JSON.stringify(data, null, 2);
		} catch (e: any) {
			tryItResponse = `Error: ${e.message}`;
			tryItStatus = 0;
		} finally {
			tryItLoading = false;
		}
	}

	function openTryIt(method: string, endpoint: string, body?: string) {
		tryItMethod = method;
		tryItEndpoint = endpoint;
		tryItBody = body || '';
		tryItResponse = '';
		tryItStatus = 0;
	}

	const sections = [
		{
			id: 'getting-started',
			title: 'Getting Started',
			content: `
## 1. Create an account

Register at [paychains.dev/auth/register](/auth/register) to get your API keys. You'll receive a **live key** (\`pc_live_...\`) and a **test key** (\`pc_test_...\`).

## 2. Configure your wallet

Go to [Dashboard → Settings](/dashboard/settings) and enter your wallet's extended public key (xpub).
PayChains derives unique deposit addresses from your xpub — your private keys never leave your wallet.

Supported wallets: MetaMask, Ledger, Trezor, or any BIP-44 compatible wallet.

## 3. Install the SDK

\`\`\`bash
npm install paychains
# or
pip install paychains
\`\`\`

Or use the REST API directly — all endpoints accept JSON and return JSON.

## 4. Make your first API call

\`\`\`javascript
import PayChains from 'paychains';

const pc = new PayChains({ apiKey: 'pc_test_YOUR_KEY' });

const payment = await pc.payments.create({
  amount_usd: 25.00,
  chain: 'polygon',
  token: 'USDC'
});

console.log(payment.deposit_address); // 0x7a3b...
console.log(payment.id);             // uuid
\`\`\`

### Python

\`\`\`python
from paychains import PayChains

pc = PayChains(api_key="pc_test_YOUR_KEY")

payment = pc.payments.create(
    amount_usd=25.00,
    chain="polygon",
    token="USDC"
)

print(payment["deposit_address"])
\`\`\``
		},
		{
			id: 'authentication',
			title: 'Authentication',
			content: `
All API requests require an API key passed via the \`X-API-Key\` header.

\`\`\`
X-API-Key: pc_live_your_api_key_here
\`\`\`

**Test vs Live keys**: Use \`pc_test_...\` keys for development. Test payments are processed on testnets. Use \`pc_live_...\` keys for production.

### Rate Limits

| Plan | Rate Limit |
|------|-----------|
| Free | 100 req/min |
| Pro | 1,000 req/min |
| Enterprise | 5,000 req/min |

Rate limit headers are included in every response:
\`\`\`
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1679012345
\`\`\``
		},
		{
			id: 'payments',
			title: 'Payments API',
			content: `
### Create Payment
\`POST /api/v1/payments/create\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| amount_usd | number | Yes | Amount in USD |
| chain | string | Yes | ethereum, polygon, bsc, arbitrum, base |
| token | string | Yes | USDC, USDT, ETH, MATIC, BNB |
| metadata | object | No | Custom key-value metadata |
| payment_link_id | string | No | Link to a payment link |

**Note:** Solana and Bitcoin are coming soon.

### List Payments
\`GET /api/v1/payments\`

Query params: \`status\`, \`chain\`, \`page\`, \`per_page\`

### Get Payment
\`GET /api/v1/payments/{id}\`

### Refund Payment
\`POST /api/v1/payments/{id}/refund\`

Only completed payments can be refunded.

### Payment Statuses
- **pending** — Waiting for customer to send funds
- **confirming** — Transaction detected on-chain, awaiting confirmations
- **completed** — Payment confirmed and settled
- **failed** — Payment failed
- **expired** — Payment window expired (30 minutes)
- **refunded** — Payment has been refunded`,
			tryEndpoints: [
				{ label: 'Create Payment', method: 'POST', endpoint: '/payments/create', body: '{\n  "amount_usd": 10.00,\n  "chain": "polygon",\n  "token": "USDC"\n}' },
				{ label: 'List Payments', method: 'GET', endpoint: '/payments' }
			]
		},
		{
			id: 'payment-links',
			title: 'Payment Links',
			content: `
### Create Payment Link
\`POST /api/v1/payment-links\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Display name shown on checkout |
| description | string | No | Description shown to customer |
| amount_usd | number | No | Fixed amount (omit for custom amount) |

### List Payment Links
\`GET /api/v1/payment-links\`

Payment links generate a hosted checkout page at \`/checkout/{link_id}\` that customers can use to select a chain, token, and pay via QR code.`,
			tryEndpoints: [
				{ label: 'Create Link', method: 'POST', endpoint: '/payment-links', body: '{\n  "title": "Test Product",\n  "amount_usd": 9.99\n}' },
				{ label: 'List Links', method: 'GET', endpoint: '/payment-links' }
			]
		},
		{
			id: 'subscriptions',
			title: 'Subscriptions',
			content: `
### Create Subscription
\`POST /api/v1/subscriptions\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| plan_name | string | Yes | Plan display name |
| amount_usd | number | Yes | Recurring amount in USD |
| interval | string | Yes | weekly, monthly, quarterly, yearly |
| customer_email | string | No | Customer email for notifications |
| customer_wallet | string | No | Customer wallet address |
| preferred_chain | string | No | Default chain for billing |
| preferred_token | string | No | Default token for billing |

### List Subscriptions
\`GET /api/v1/subscriptions\`

Subscriptions are automatically billed on schedule. Failed payments trigger retry logic with exponential backoff (up to 3 retries).`,
			tryEndpoints: [
				{ label: 'Create Subscription', method: 'POST', endpoint: '/subscriptions', body: '{\n  "plan_name": "Pro Plan",\n  "amount_usd": 49.99,\n  "interval": "monthly",\n  "customer_email": "test@example.com"\n}' },
				{ label: 'List Subscriptions', method: 'GET', endpoint: '/subscriptions' }
			]
		},
		{
			id: 'webhooks',
			title: 'Webhooks',
			content: `
Configure your webhook URL in [Settings](/dashboard/settings). PayChains sends POST requests with HMAC-SHA256 signatures for all payment events.

### Webhook Payload
\`\`\`json
{
  "event": "payment.completed",
  "data": {
    "payment_id": "uuid",
    "status": "completed",
    "amount_usd": "25.00",
    "token": "USDC",
    "chain": "ethereum",
    "tx_hash": "0x...",
    "deposit_address": "0x...",
    "confirmations": 5
  },
  "timestamp": "2026-03-17T00:00:00Z"
}
\`\`\`

### Verifying Signatures

\`\`\`javascript
import { createHmac } from 'crypto';

function verify(body, signature, secret) {
  const expected = createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return expected === signature;
}
\`\`\`

Or use the SDK:
\`\`\`javascript
const isValid = paychains.webhooks.verifySignature(
  requestBody, headers['x-signature'], webhookSecret
);
\`\`\`

### Events
- \`payment.pending\` — Payment created, waiting for funds
- \`payment.confirming\` — Transaction detected on-chain
- \`payment.completed\` — Payment fully confirmed
- \`payment.failed\` — Payment failed
- \`payment.expired\` — Payment expired (30 min window)
- \`subscription.created\` — New subscription created
- \`subscription.payment_due\` — Recurring payment initiated
- \`subscription.cancelled\` — Subscription cancelled`,
			tryEndpoints: [
				{ label: 'List Events', method: 'GET', endpoint: '/webhooks/events' },
				{ label: 'Send Test', method: 'POST', endpoint: '/webhooks/test' }
			]
		},
		{
			id: 'payouts',
			title: 'Payouts',
			content: `
PayChains is non-custodial — payments go directly to your wallet addresses derived from your xpub key. No payout requests needed.

### How it works
When a customer pays, funds are sent to a unique deposit address derived from your extended public key. You have immediate access to all funds in your wallet.

### List Historical Payouts
\`GET /api/v1/payouts\`

Returns historical payout records (legacy). New payments are deposited directly to your wallet.`,
			tryEndpoints: [
				{ label: 'List Payouts', method: 'GET', endpoint: '/payouts' }
			]
		},
		{
			id: 'analytics',
			title: 'Analytics',
			content: `
### Overview
\`GET /api/v1/analytics/overview\`

Query params: \`days\` (default: 30)

Returns total volume, payment count, and success rate for the specified period.

### By Chain
\`GET /api/v1/analytics/by-chain\`

Returns payment volume breakdown by blockchain.

### By Token
\`GET /api/v1/analytics/by-token\`

Returns payment volume breakdown by token.`,
			tryEndpoints: [
				{ label: 'Overview', method: 'GET', endpoint: '/analytics/overview' },
				{ label: 'By Chain', method: 'GET', endpoint: '/analytics/by-chain' },
				{ label: 'By Token', method: 'GET', endpoint: '/analytics/by-token' }
			]
		},
		{
			id: 'websockets',
			title: 'WebSocket Updates',
			content: `
Get real-time payment status updates via WebSocket:

\`\`\`javascript
const ws = new WebSocket('wss://api.paychains.dev/ws/payments/{payment_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.status);         // "confirming"
  console.log(data.confirmations);  // 3
  console.log(data.required_confirmations); // 5
};

ws.onclose = () => {
  // Payment reached terminal state
};
\`\`\`

The WebSocket sends a JSON message whenever the payment status or confirmation count changes. It automatically closes when the payment reaches a terminal state (\`completed\`, \`failed\`, \`expired\`, \`refunded\`).

### WebSocket Message Format
\`\`\`json
{
  "payment_id": "uuid",
  "status": "confirming",
  "confirmations": 3,
  "required_confirmations": 5,
  "amount_usd": "25.00",
  "amount_crypto": "25.123456",
  "token": "USDC",
  "chain": "polygon",
  "tx_hash": "0x...",
  "deposit_address": "0x..."
}
\`\`\``
		},
		{
			id: 'errors',
			title: 'Error Handling',
			content: `
All errors return a JSON response with a \`detail\` field:

\`\`\`json
{
  "detail": "Invalid API key"
}
\`\`\`

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (invalid/missing API key) |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

### SDK Error Handling

\`\`\`javascript
try {
  const payment = await pc.payments.create({ ... });
} catch (error) {
  if (error.status === 429) {
    // Rate limited — back off and retry
  }
  console.error(error.message);
}
\`\`\`

\`\`\`python
from paychains.exceptions import RateLimitError, ValidationError

try:
    payment = pc.payments.create(...)
except RateLimitError:
    # Back off and retry
    pass
except ValidationError as e:
    print(e.message)
\`\`\``
		}
	];

	let activeSection = $state('getting-started');
</script>

<svelte:head>
	<title>Documentation — PayChains</title>
</svelte:head>

<div class="min-h-screen bg-surface-950">
	<!-- Header -->
	<header class="sticky top-0 z-50 bg-surface-950/80 backdrop-blur-xl border-b border-white/[0.06]">
		<div class="max-w-7xl mx-auto flex items-center justify-between px-6 h-14">
			<a href="/" class="flex items-center gap-2">
				<div class="w-6 h-6 rounded-md bg-brand-500 flex items-center justify-center">
					<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-[14px] font-semibold">PayChains</span>
				<span class="text-[12px] text-surface-500 ml-1">Docs</span>
			</a>
			<div class="flex items-center gap-3">
				{#if isLoggedIn}
					<a href="/dashboard" class="text-[13px] font-medium text-surface-300 hover:text-white transition-colors">Dashboard</a>
				{:else}
					<a href="/auth/login" class="text-[13px] font-medium text-surface-300 hover:text-white transition-colors">Log in</a>
				{/if}
			</div>
		</div>
	</header>

	<div class="max-w-7xl mx-auto flex">
		<!-- Sidebar -->
		<aside class="hidden md:block w-56 shrink-0 sticky top-14 h-[calc(100vh-3.5rem)] overflow-y-auto border-r border-white/[0.06] py-6 px-4">
			<nav class="space-y-0.5">
				{#each sections as section}
					<a
						href="#{section.id}"
						onclick={() => activeSection = section.id}
						class="block px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors
							{activeSection === section.id ? 'bg-white/[0.06] text-white' : 'text-surface-400 hover:text-surface-200 hover:bg-white/[0.03]'}"
					>{section.title}</a>
				{/each}
			</nav>

			<!-- API Key Input -->
			<div class="mt-8 pt-6 border-t border-white/[0.06]">
				<label class="block text-[11px] font-medium text-surface-500 uppercase tracking-wider mb-2">API Key for Try It</label>
				<input
					bind:value={testApiKey}
					type="password"
					placeholder="pc_test_..."
					class="w-full px-3 py-2 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[12px] font-mono placeholder-surface-600 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
				/>
			</div>
		</aside>

		<!-- Content -->
		<main class="flex-1 min-w-0 px-6 md:px-12 py-10">
			<h1 class="text-2xl font-bold tracking-tight mb-2">API Documentation</h1>
			<p class="text-[14px] text-surface-400 mb-10">Everything you need to integrate PayChains into your application.</p>

			<!-- Mobile API Key -->
			<div class="md:hidden mb-8 rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">
				<label class="block text-[11px] font-medium text-surface-500 uppercase tracking-wider mb-2">API Key for Try It</label>
				<input
					bind:value={testApiKey}
					type="password"
					placeholder="pc_test_..."
					class="w-full px-3 py-2 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[12px] font-mono placeholder-surface-600 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
				/>
			</div>

			<div class="space-y-16">
				{#each sections as section}
					<section id={section.id} class="scroll-mt-20">
						<h2 class="text-lg font-bold tracking-tight mb-4 pb-2 border-b border-white/[0.06]">{section.title}</h2>
						<div class="prose prose-invert prose-sm max-w-none
							prose-headings:text-white prose-headings:font-semibold
							prose-p:text-surface-300 prose-p:leading-relaxed
							prose-code:text-brand-300 prose-code:bg-white/[0.06] prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-[12px] prose-code:font-mono
							prose-pre:bg-white/[0.03] prose-pre:border prose-pre:border-white/[0.06] prose-pre:rounded-xl prose-pre:text-[12px]
							prose-a:text-brand-400 prose-a:no-underline hover:prose-a:text-brand-300
							prose-table:text-[13px]
							prose-th:text-surface-400 prose-th:font-medium prose-th:border-b prose-th:border-white/[0.06] prose-th:py-2
							prose-td:py-2 prose-td:border-b prose-td:border-white/[0.04] prose-td:text-surface-300
							prose-strong:text-white
							prose-li:text-surface-300">
							{@html section.content
								.replace(/^### (.+)$/gm, '<h3>$1</h3>')
								.replace(/^## (.+)$/gm, '<h2>$1</h2>')
								.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
								.replace(/`([^`]+)`/g, '<code>$1</code>')
								.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
								.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
								.replace(/^\| (.+)$/gm, (match) => {
									const cells = match.split('|').filter(c => c.trim());
									return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
								})
								.replace(/(<tr>.*<\/tr>\n?)+/g, (match) => {
									const rows = match.trim().split('\n').filter(r => !r.match(/^[\s|:-]+$/));
									if (rows.length < 2) return match;
									const header = rows[0].replace(/<td>/g, '<th>').replace(/<\/td>/g, '</th>');
									const body = rows.slice(1).join('\n');
									return `<table><thead>${header}</thead><tbody>${body}</tbody></table>`;
								})
								.replace(/^- (.+)$/gm, '<li>$1</li>')
								.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
								.replace(/\n\n/g, '</p><p>')
								.replace(/^(?!<[huptla])(.+)$/gm, '<p>$1</p>')
							}
						</div>

						<!-- Try It Panel -->
						{#if section.tryEndpoints}
							<div class="mt-6 rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
								<div class="px-4 py-2.5 border-b border-white/[0.06] flex items-center gap-2">
									<svg class="w-4 h-4 text-brand-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728M9.172 14.828a4 4 0 010-5.656m5.656 0a4 4 0 010 5.656M12 12h.01" stroke-linecap="round" stroke-linejoin="round"/></svg>
									<span class="text-[13px] font-semibold text-brand-300">Try It Live</span>
								</div>
								<div class="p-4">
									<div class="flex flex-wrap gap-2 mb-4">
										{#each section.tryEndpoints as ep}
											<button
												onclick={() => openTryIt(ep.method, ep.endpoint, ep.body)}
												class="px-3 py-1.5 rounded-lg text-[12px] font-medium border transition-colors
													{tryItEndpoint === ep.endpoint
														? 'border-brand-500/40 bg-brand-500/10 text-brand-300'
														: 'border-white/[0.08] text-surface-400 hover:text-surface-200 hover:bg-white/[0.04]'}"
											>
												<span class="font-mono text-[11px] mr-1 {ep.method === 'POST' ? 'text-amber-400' : 'text-emerald-400'}">{ep.method}</span>
												{ep.label}
											</button>
										{/each}
									</div>

									{#if tryItEndpoint && section.tryEndpoints.some(e => e.endpoint === tryItEndpoint)}
										<div class="space-y-3">
											<div class="flex items-center gap-2 text-[12px] font-mono text-surface-400">
												<span class="px-1.5 py-0.5 rounded text-[11px] font-semibold {tryItMethod === 'POST' ? 'bg-amber-500/10 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'}">{tryItMethod}</span>
												<span>{API_BASE}{tryItEndpoint}</span>
											</div>

											{#if tryItMethod !== 'GET' && tryItBody}
												<textarea
													bind:value={tryItBody}
													rows="6"
													class="w-full px-3 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[12px] font-mono text-surface-200 placeholder-surface-600 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all resize-none"
												></textarea>
											{/if}

											<button
												onclick={runTryIt}
												disabled={!testApiKey || tryItLoading}
												class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-40 rounded-lg text-[13px] font-semibold transition-all"
											>
												{#if tryItLoading}
													Running...
												{:else if !testApiKey}
													Enter API key first
												{:else}
													Send Request
												{/if}
											</button>

											{#if tryItResponse}
												<div class="mt-3">
													<div class="flex items-center gap-2 mb-1.5">
														<span class="text-[11px] font-medium text-surface-500">Response</span>
														<span class="px-1.5 py-0.5 rounded text-[11px] font-mono font-medium
															{tryItStatus >= 200 && tryItStatus < 300 ? 'bg-emerald-500/10 text-emerald-400' :
															tryItStatus >= 400 ? 'bg-red-500/10 text-red-400' : 'bg-surface-500/10 text-surface-400'}">
															{tryItStatus || 'ERR'}
														</span>
													</div>
													<pre class="p-4 rounded-lg bg-white/[0.03] border border-white/[0.06] text-[12px] font-mono text-surface-300 overflow-x-auto max-h-80 overflow-y-auto">{tryItResponse}</pre>
												</div>
											{/if}
										</div>
									{/if}
								</div>
							</div>
						{/if}
					</section>
				{/each}
			</div>
		</main>
	</div>
</div>
