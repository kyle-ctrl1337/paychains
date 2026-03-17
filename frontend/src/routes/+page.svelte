<script>
	import { auth } from '$lib/stores/auth';

	let isLoggedIn = $state(false);

	auth.subscribe((state) => {
		isLoggedIn = !!state.token;
	});

	const chains = [
		{ name: 'Ethereum', symbol: 'ETH', active: true },
		{ name: 'Polygon', symbol: 'MATIC', active: true },
		{ name: 'BSC', symbol: 'BNB', active: true },
		{ name: 'Arbitrum', symbol: 'ARB', active: true },
		{ name: 'Base', symbol: 'BASE', active: true },
		{ name: 'Solana', symbol: 'SOL', active: false },
		{ name: 'Bitcoin', symbol: 'BTC', active: false }
	];

	const features = [
		{
			title: 'Multi-Chain Payments',
			description: 'Accept payments on Ethereum, Polygon, BSC, Arbitrum, and Base through a single unified API. Solana and Bitcoin coming soon.',
			icon: 'chains'
		},
		{
			title: 'Recurring Billing',
			description: 'The first crypto subscription engine that actually works. Weekly, monthly, quarterly, yearly — with automatic dunning.',
			icon: 'billing'
		},
		{
			title: 'Non-Custodial by Design',
			description: 'Unlike other payment processors, PayChains never holds your crypto. Payments are deposited directly to addresses derived from YOUR wallet. Your keys, your crypto.',
			icon: 'convert'
		},
		{
			title: 'Hosted Checkout',
			description: 'Beautiful, conversion-optimized checkout pages. Share a link or embed in your app. QR codes included.',
			icon: 'checkout'
		},
		{
			title: 'Webhook Delivery',
			description: 'Real-time event notifications with HMAC-SHA256 signatures, automatic retries, and exponential backoff.',
			icon: 'webhook'
		},
		{
			title: 'Your Wallet, Your Keys',
			description: 'Paste your wallet address and payments go directly to you. Your private keys never leave your wallet.',
			icon: 'wallet'
		}
	];

	const metrics = [
		{ value: '5+', label: 'Blockchains' },
		{ value: '<1s', label: 'API Latency' },
		{ value: '100%', label: 'Non-Custodial' },
		{ value: '$0', label: 'Transaction Fee' }
	];

	const comparison = [
		{ feature: 'Multi-chain EVM support', paychains: true, stripe: false, coinbase: true, bitpay: false },
		{ feature: 'Recurring subscriptions', paychains: true, stripe: true, coinbase: false, bitpay: false },
		{ feature: 'Auto-convert to stablecoins', paychains: 'soon', stripe: false, coinbase: false, bitpay: true },
		{ feature: 'HD wallet per payment', paychains: true, stripe: false, coinbase: false, bitpay: false },
		{ feature: 'API-first (no dashboard required)', paychains: true, stripe: true, coinbase: false, bitpay: false },
		{ feature: 'Hosted checkout + QR codes', paychains: true, stripe: true, coinbase: true, bitpay: true },
		{ feature: 'Webhook with HMAC signatures', paychains: true, stripe: true, coinbase: true, bitpay: true },
		{ feature: 'Real-time WebSocket updates', paychains: true, stripe: false, coinbase: false, bitpay: false },
		{ feature: 'Open-source SDKs (JS + Python)', paychains: true, stripe: true, coinbase: true, bitpay: true },
		{ feature: 'No KYB to start', paychains: true, stripe: false, coinbase: false, bitpay: false },
		{ feature: 'Self-custody option', paychains: true, stripe: false, coinbase: false, bitpay: false },
		{ feature: 'Non-custodial (your keys)', paychains: true, stripe: false, coinbase: false, bitpay: false },
	];
</script>

<div class="min-h-screen bg-surface-950 relative overflow-hidden">
	<!-- Background effects -->
	<div class="grid-bg fixed inset-0 z-0"></div>
	<div class="hero-glow bg-brand-500 top-[-200px] left-1/2 -translate-x-1/2 z-0"></div>

	<!-- Navigation -->
	<nav class="relative z-10 border-b border-white/[0.06]">
		<div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
			<a href="/" class="flex items-center gap-2.5">
				<div class="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-[15px] font-semibold tracking-[-0.01em]">PayChains</span>
			</a>

			<div class="hidden md:flex items-center gap-8 text-[13px] text-surface-400">
				<a href="#features" class="hover:text-white transition-colors">Features</a>
				<a href="#compare" class="hover:text-white transition-colors">Compare</a>
				<a href="#pricing" class="hover:text-white transition-colors">Pricing</a>
				<a href="/docs" class="hover:text-white transition-colors">Docs</a>
			</div>

			<div class="flex items-center gap-3">
				{#if isLoggedIn}
					<a href="/dashboard" class="text-[13px] font-medium bg-brand-500 hover:bg-brand-400 text-white px-4 py-1.5 rounded-lg transition-all hover:shadow-lg hover:shadow-brand-500/20">
						Dashboard
					</a>
				{:else}
					<a href="/auth/login" class="text-[13px] font-medium text-surface-300 hover:text-white px-3 py-1.5 transition-colors">
						Log in
					</a>
					<a href="/auth/register" class="text-[13px] font-medium bg-brand-500 hover:bg-brand-400 text-white px-4 py-1.5 rounded-lg transition-all hover:shadow-lg hover:shadow-brand-500/20">
						Get API Keys
					</a>
				{/if}
			</div>
		</div>
	</nav>

	<!-- Hero -->
	<section class="relative z-10 pt-24 pb-20 px-6">
		<div class="max-w-4xl mx-auto text-center">
			<div class="animate-fade-up inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/[0.08] bg-white/[0.03] text-[12px] text-surface-400 mb-8">
				<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
				Now processing on 5 EVM networks
			</div>

			<h1 class="animate-fade-up-delay-1 text-[clamp(2.5rem,6vw,4.5rem)] font-bold leading-[1.08] tracking-[-0.035em] mb-6">
				The payment infrastructure<br />
				<span class="bg-gradient-to-r from-brand-400 via-brand-300 to-purple-300 bg-clip-text text-transparent">for crypto-native businesses</span>
			</h1>

			<p class="animate-fade-up-delay-2 text-lg text-surface-400 max-w-xl mx-auto mb-10 leading-relaxed">
				The only crypto billing API where you keep full custody. Recurring subscriptions, automatic dunning, and real-time webhooks — payments go straight to your wallet.
			</p>

			<div class="animate-fade-up-delay-3 flex items-center justify-center gap-4 mb-20">
				<a href="/auth/register" class="group inline-flex items-center gap-2 px-6 py-3 bg-brand-500 hover:bg-brand-400 rounded-xl text-[14px] font-semibold transition-all hover:shadow-xl hover:shadow-brand-500/20">
					Start Building
					<svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
				</a>
				<a href="#features" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-[14px] font-medium border border-white/[0.08] text-surface-300 hover:bg-white/[0.04] hover:border-white/[0.12] transition-all">
					See how it works
				</a>
			</div>

			<!-- Code Block -->
			<div class="animate-fade-up-delay-4 max-w-2xl mx-auto">
				<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl overflow-hidden shadow-2xl shadow-black/40">
					<div class="flex items-center justify-between px-5 py-3 border-b border-white/[0.06]">
						<div class="flex items-center gap-2">
							<div class="w-2.5 h-2.5 rounded-full bg-surface-700"></div>
							<div class="w-2.5 h-2.5 rounded-full bg-surface-700"></div>
							<div class="w-2.5 h-2.5 rounded-full bg-surface-700"></div>
						</div>
						<span class="text-[11px] text-surface-500 font-mono">create-payment.ts</span>
						<div class="w-16"></div>
					</div>
					<pre class="p-6 text-[13px] font-mono leading-relaxed text-left overflow-x-auto"><code><span class="token-keyword">const</span> payment = <span class="token-keyword">await</span> paychains.payments.<span class="token-function">create</span>(<span class="token-punctuation">{'{'}</span>
  <span class="token-property">amount_usd</span><span class="token-punctuation">:</span> <span class="token-number">49.99</span><span class="token-punctuation">,</span>
  <span class="token-property">token</span><span class="token-punctuation">:</span>      <span class="token-string">"USDC"</span><span class="token-punctuation">,</span>
  <span class="token-property">chain</span><span class="token-punctuation">:</span>      <span class="token-string">"polygon"</span><span class="token-punctuation">,</span>
  <span class="token-property">metadata</span><span class="token-punctuation">:</span>   <span class="token-punctuation">{'{'}</span> <span class="token-property">order_id</span><span class="token-punctuation">:</span> <span class="token-string">"ord_8x2k"</span> <span class="token-punctuation">{'}'}</span>
<span class="token-punctuation">{'}'}</span>)<span class="token-punctuation">;</span>

<span class="token-comment">// Unique deposit address + QR code per payment</span>
console.<span class="token-function">log</span>(payment.<span class="token-property">deposit_address</span>)<span class="token-punctuation">;</span>  <span class="token-comment">// 0x7a3b...</span>
console.<span class="token-function">log</span>(payment.<span class="token-property">checkout_url</span>)<span class="token-punctuation">;</span>     <span class="token-comment">// https://pay.paychains.dev/p/...</span></code></pre>
				</div>
			</div>
		</div>
	</section>

	<!-- Chain Logos Strip -->
	<section class="relative z-10 py-16 border-y border-white/[0.04]">
		<div class="max-w-4xl mx-auto px-6">
			<p class="text-center text-[12px] text-surface-500 uppercase tracking-widest font-medium mb-8">Supported Networks</p>
			<div class="flex items-center justify-center gap-8 md:gap-14 flex-wrap">
				{#each chains as chain}
					<div class="flex items-center gap-2 {chain.active ? 'text-surface-500 hover:text-surface-300' : 'text-surface-700'} transition-colors">
						<span class="text-[13px] font-medium">{chain.name}</span>
						<span class="text-[11px] {chain.active ? 'text-surface-600' : 'text-surface-700'} font-mono">{chain.symbol}</span>
						{#if !chain.active}
							<span class="text-[9px] px-1.5 py-0.5 rounded-full bg-surface-800 text-surface-500 font-medium uppercase tracking-wider">Soon</span>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Metrics -->
	<section class="relative z-10 py-20 px-6">
		<div class="max-w-4xl mx-auto">
			<div class="grid grid-cols-2 md:grid-cols-4 gap-8">
				{#each metrics as metric}
					<div class="text-center">
						<div class="text-4xl md:text-5xl font-bold tracking-tight text-white mb-2">{metric.value}</div>
						<div class="text-[13px] text-surface-500">{metric.label}</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- Features -->
	<section id="features" class="relative z-10 py-24 px-6">
		<div class="max-w-5xl mx-auto">
			<div class="text-center mb-16">
				<p class="text-[12px] text-brand-400 uppercase tracking-widest font-semibold mb-4">Platform</p>
				<h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-4">Everything you need to accept crypto</h2>
				<p class="text-surface-400 max-w-lg mx-auto">A complete payments stack — from checkout to settlement. No blockchain expertise required.</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-white/[0.04] rounded-2xl overflow-hidden border border-white/[0.06]">
				{#each features as feature}
					<div class="bg-surface-950 p-8 hover:bg-white/[0.02] transition-colors">
						<div class="w-10 h-10 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-5">
							{#if feature.icon === 'chains'}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.553-3.554L19.378 4.5a4.5 4.5 0 016.364 6.364l-4.5 4.5a4.5 4.5 0 01-7.244-1.242" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else if feature.icon === 'billing'}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else if feature.icon === 'convert'}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else if feature.icon === 'checkout'}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else if feature.icon === 'webhook'}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6a2.25 2.25 0 01-2.25-2.25v-1.5M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{:else}
								<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" stroke-linecap="round" stroke-linejoin="round"/></svg>
							{/if}
						</div>
						<h3 class="text-[15px] font-semibold mb-2">{feature.title}</h3>
						<p class="text-[13px] text-surface-400 leading-relaxed">{feature.description}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- How it Works -->
	<section class="relative z-10 py-24 px-6 border-t border-white/[0.04]">
		<div class="max-w-4xl mx-auto">
			<div class="text-center mb-16">
				<p class="text-[12px] text-brand-400 uppercase tracking-widest font-semibold mb-4">Integration</p>
				<h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-4">Live in under 5 minutes</h2>
				<p class="text-surface-400 max-w-lg mx-auto">Three steps from signup to accepting your first payment.</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<div class="relative">
					<div class="text-[11px] font-mono text-brand-400 mb-3">01</div>
					<h3 class="text-[15px] font-semibold mb-2">Get your API keys</h3>
					<p class="text-[13px] text-surface-400 leading-relaxed">Create an account and receive live and test API keys instantly. No approval process.</p>
				</div>
				<div class="relative">
					<div class="text-[11px] font-mono text-brand-400 mb-3">02</div>
					<h3 class="text-[15px] font-semibold mb-2">Create a payment</h3>
					<p class="text-[13px] text-surface-400 leading-relaxed">One API call generates a unique deposit address, QR code, and hosted checkout page.</p>
				</div>
				<div class="relative">
					<div class="text-[11px] font-mono text-brand-400 mb-3">03</div>
					<h3 class="text-[15px] font-semibold mb-2">Get notified & settle</h3>
					<p class="text-[13px] text-surface-400 leading-relaxed">We monitor the blockchain, confirm transactions, and fire webhooks. Funds arrive directly in your wallet — no withdrawal needed.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Comparison Table -->
	<section id="compare" class="relative z-10 py-24 px-6 border-t border-white/[0.04]">
		<div class="max-w-4xl mx-auto">
			<div class="text-center mb-16">
				<p class="text-[12px] text-brand-400 uppercase tracking-widest font-semibold mb-4">Why PayChains</p>
				<h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-4">Built different from the start</h2>
				<p class="text-surface-400 max-w-lg mx-auto">See how PayChains compares to other crypto payment providers.</p>
			</div>

			<div class="rounded-2xl border border-white/[0.06] overflow-hidden">
				<div class="overflow-x-auto">
					<table class="w-full text-[13px]">
						<thead>
							<tr class="border-b border-white/[0.06] bg-white/[0.02]">
								<th class="text-left px-5 py-3.5 text-surface-500 font-medium">Feature</th>
								<th class="px-5 py-3.5 text-brand-400 font-semibold text-center">PayChains</th>
								<th class="px-5 py-3.5 text-surface-500 font-medium text-center">Stripe Crypto</th>
								<th class="px-5 py-3.5 text-surface-500 font-medium text-center">Coinbase Commerce</th>
								<th class="px-5 py-3.5 text-surface-500 font-medium text-center">BitPay</th>
							</tr>
						</thead>
						<tbody>
							{#each comparison as row, i}
								<tr class="{i % 2 === 0 ? 'bg-white/[0.01]' : ''} border-b border-white/[0.04] last:border-0">
									<td class="px-5 py-3 text-surface-300">{row.feature}</td>
									<td class="px-5 py-3 text-center">
										{#if row.paychains === true}
											<svg class="w-5 h-5 text-emerald-400 mx-auto" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
										{:else if row.paychains === 'soon'}
											<span class="text-[11px] text-amber-400 font-medium">Soon</span>
										{:else}
											<span class="text-surface-600">—</span>
										{/if}
									</td>
									<td class="px-5 py-3 text-center">
										{#if row.stripe}
											<svg class="w-4 h-4 text-surface-500 mx-auto" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
										{:else}
											<span class="text-surface-600">—</span>
										{/if}
									</td>
									<td class="px-5 py-3 text-center">
										{#if row.coinbase}
											<svg class="w-4 h-4 text-surface-500 mx-auto" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
										{:else}
											<span class="text-surface-600">—</span>
										{/if}
									</td>
									<td class="px-5 py-3 text-center">
										{#if row.bitpay}
											<svg class="w-4 h-4 text-surface-500 mx-auto" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
										{:else}
											<span class="text-surface-600">—</span>
										{/if}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</section>

	<!-- SDK Install -->
	<section class="relative z-10 py-16 px-6 border-t border-white/[0.04]">
		<div class="max-w-2xl mx-auto text-center">
			<p class="text-[12px] text-brand-400 uppercase tracking-widest font-semibold mb-6">Get Started in Seconds</p>
			<div class="flex flex-col sm:flex-row items-center justify-center gap-4">
				<div class="rounded-xl border border-white/[0.06] bg-surface-900/80 px-5 py-3 font-mono text-[13px] text-surface-300">
					<span class="text-surface-500">$</span> npm install <span class="text-brand-300">paychains</span>
				</div>
				<div class="rounded-xl border border-white/[0.06] bg-surface-900/80 px-5 py-3 font-mono text-[13px] text-surface-300">
					<span class="text-surface-500">$</span> pip install <span class="text-brand-300">paychains</span>
				</div>
			</div>
		</div>
	</section>

	<!-- Pricing -->
	<section id="pricing" class="relative z-10 py-24 px-6 border-t border-white/[0.04]">
		<div class="max-w-4xl mx-auto">
			<div class="text-center mb-16">
				<p class="text-[12px] text-brand-400 uppercase tracking-widest font-semibold mb-4">Pricing</p>
				<h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-4">Simple, transparent pricing</h2>
				<p class="text-surface-400">Pure SaaS pricing. No transaction fees, ever.</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<!-- Free -->
				<div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8">
					<div class="text-[13px] font-medium text-surface-400 mb-1">Free</div>
					<div class="text-3xl font-bold mb-1">$0/mo</div>
					<div class="text-[12px] text-surface-500 mb-6">up to 100 payments/month</div>
					<ul class="space-y-3 text-[13px] text-surface-400">
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							5 EVM chains
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Hosted checkout
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Webhooks
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							100 req/min API limit
						</li>
					</ul>
					<a href="/auth/register" class="block mt-8 text-center px-4 py-2.5 rounded-xl border border-white/[0.08] text-[13px] font-medium hover:bg-white/[0.04] transition-colors">
						Get started free
					</a>
				</div>

				<!-- Pro -->
				<div class="rounded-2xl border border-brand-500/30 bg-brand-500/[0.04] p-8 relative">
					<div class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-brand-500 text-[11px] font-semibold">Popular</div>
					<div class="text-[13px] font-medium text-brand-300 mb-1">Pro</div>
					<div class="text-3xl font-bold mb-1">$49/mo</div>
					<div class="text-[12px] text-surface-500 mb-6">up to 2,000 payments/month</div>
					<ul class="space-y-3 text-[13px] text-surface-400">
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Everything in Free
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Recurring billing
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Priority webhooks
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Analytics dashboard
						</li>
					</ul>
					<a href="/auth/register?plan=pro" class="block mt-8 text-center px-4 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-400 text-[13px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20">
						Pay with Crypto
					</a>
				</div>

				<!-- Enterprise -->
				<div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8">
					<div class="text-[13px] font-medium text-surface-400 mb-1">Enterprise</div>
					<div class="text-3xl font-bold mb-1">$199/mo</div>
					<div class="text-[12px] text-surface-500 mb-6">unlimited payments</div>
					<ul class="space-y-3 text-[13px] text-surface-400">
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Everything in Pro
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Dedicated support
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Custom SLA
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							5,000 req/min API limit
						</li>
					</ul>
					<a href="mailto:hello@paychains.dev?subject=PayChains Enterprise" class="block mt-8 text-center px-4 py-2.5 rounded-xl border border-white/[0.08] text-[13px] font-medium hover:bg-white/[0.04] transition-colors">
						Contact sales
					</a>
				</div>
			</div>
		</div>
	</section>

	<!-- CTA -->
	<section class="relative z-10 py-24 px-6 border-t border-white/[0.04]">
		<div class="max-w-2xl mx-auto text-center">
			<h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-4">Start accepting crypto today</h2>
			<p class="text-surface-400 mb-8">Free to start. No credit card required. Get your API keys in 30 seconds.</p>
			<a href="/auth/register" class="group inline-flex items-center gap-2 px-8 py-3.5 bg-brand-500 hover:bg-brand-400 rounded-xl text-[15px] font-semibold transition-all hover:shadow-xl hover:shadow-brand-500/20">
				Create Free Account
				<svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
			</a>
		</div>
	</section>

	<!-- Footer -->
	<footer class="relative z-10 border-t border-white/[0.04] py-12 px-6">
		<div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
			<div class="flex items-center gap-2.5">
				<div class="w-6 h-6 rounded-md bg-brand-500 flex items-center justify-center">
					<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-[13px] font-semibold">PayChains</span>
			</div>
			<div class="flex items-center gap-6 text-[12px] text-surface-500">
				<a href="#features" class="hover:text-surface-300 transition-colors">Features</a>
				<a href="#pricing" class="hover:text-surface-300 transition-colors">Pricing</a>
				<a href="/docs" class="hover:text-surface-300 transition-colors">Documentation</a>
				<a href="mailto:support@paychains.dev" class="hover:text-surface-300 transition-colors">Support</a>
				<a href="/privacy" class="hover:text-surface-300 transition-colors">Privacy</a>
				<a href="/terms" class="hover:text-surface-300 transition-colors">Terms</a>
			</div>
			<p class="text-[11px] text-surface-600">&copy; 2026 PayChains. All rights reserved.</p>
		</div>
	</footer>
</div>
