<script lang="ts">
	import { auth } from '$lib/stores/auth';

	let isLoggedIn = $state(false);
	auth.subscribe((s) => (isLoggedIn = !!s.token));

	const sections = [
		{
			id: 'getting-started',
			title: 'Getting Started',
			content: `
## 1. Create an account

Register at [paychains.dev/auth/register](/auth/register) to get your API keys. You'll receive a **live key** (\`pc_live_...\`) and a **test key** (\`pc_test_...\`).

## 2. Install the SDK

\`\`\`bash
npm install paychains
# or
pip install paychains
\`\`\`

Or use the REST API directly — all endpoints accept JSON and return JSON.

## 3. Create your first payment

\`\`\`bash
curl -X POST https://api.paychains.dev/api/v1/payments/create \\
  -H "X-API-Key: pc_test_YOUR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"amount_usd": 25.00, "chain": "ethereum", "token": "USDC"}'
\`\`\`

Response includes a unique \`deposit_address\` for the customer to send funds to.`
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

The merchant dashboard uses JWT authentication via the \`Authorization: Bearer <token>\` header, obtained through the login endpoint.`
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
| chain | string | Yes | ethereum, polygon, bsc, arbitrum, base, solana, bitcoin |
| token | string | Yes | USDC, USDT, ETH, BTC, SOL, MATIC, BNB |
| metadata | object | No | Custom metadata |

### List Payments
\`GET /api/v1/payments\`

Query params: \`status\`, \`chain\`, \`limit\`, \`offset\`

### Get Payment
\`GET /api/v1/payments/{id}\`

### Payment Statuses
- **pending** — Waiting for customer payment
- **confirming** — Transaction detected, awaiting confirmations
- **completed** — Payment confirmed and settled
- **failed** — Payment failed
- **expired** — Payment window expired (30 minutes)`
		},
		{
			id: 'payment-links',
			title: 'Payment Links',
			content: `
### Create Payment Link
\`POST /api/v1/payment-links\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Display name |
| description | string | No | Description shown to customer |
| amount_usd | number | No | Fixed amount (omit for custom) |

### List Payment Links
\`GET /api/v1/payment-links\`

Payment links generate a hosted checkout page at \`/checkout/{link_id}\` that customers can use to pay.`
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
| amount_usd | number | Yes | Recurring amount |
| interval | string | Yes | weekly, monthly, quarterly, yearly |
| customer_email | string | No | Customer email |
| customer_wallet | string | No | Customer wallet address |

### List Subscriptions
\`GET /api/v1/subscriptions\`

Subscriptions are automatically billed on schedule. Failed payments trigger retry logic with exponential backoff.`
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
  "payment_id": "uuid",
  "amount_usd": "25.00",
  "token": "USDC",
  "chain": "ethereum",
  "tx_hash": "0x...",
  "timestamp": "2026-03-17T00:00:00Z"
}
\`\`\`

### Verifying Signatures
The webhook secret is provided during registration. Verify using:
\`\`\`
HMAC-SHA256(webhook_secret, request_body)
\`\`\`
Compare with the \`X-Signature\` header.

### Events
- \`payment.pending\` — Payment created
- \`payment.confirming\` — Transaction detected
- \`payment.completed\` — Payment settled
- \`payment.failed\` — Payment failed
- \`payment.expired\` — Payment expired
- \`subscription.created\` — New subscription
- \`subscription.payment_due\` — Recurring payment initiated
- \`subscription.cancelled\` — Subscription cancelled`
		},
		{
			id: 'payouts',
			title: 'Payouts',
			content: `
### Request Payout
\`POST /api/v1/payouts/request\`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| amount | number | Yes | Amount to withdraw |
| token | string | Yes | Token to withdraw |
| chain | string | Yes | Chain to withdraw on |
| destination_address | string | Yes | Wallet to send to |

### List Payouts
\`GET /api/v1/payouts\`

Payouts are processed within 24 hours. Minimum payout amount is $10.`
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
  console.log(data.status, data.confirmations);
};
\`\`\`

The WebSocket sends updates whenever the payment status or confirmation count changes, and automatically closes when the payment reaches a terminal state.`
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
		</aside>

		<!-- Content -->
		<main class="flex-1 min-w-0 px-6 md:px-12 py-10">
			<h1 class="text-2xl font-bold tracking-tight mb-2">API Documentation</h1>
			<p class="text-[14px] text-surface-400 mb-10">Everything you need to integrate PayChains into your application.</p>

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
					</section>
				{/each}
			</div>
		</main>
	</div>
</div>
