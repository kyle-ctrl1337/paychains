<script>
	import { auth } from '$lib/stores/auth';

	let isLoggedIn = $state(false);

	auth.subscribe((state) => {
		isLoggedIn = !!state.token;
	});

	const chains = [
		{ name: 'Ethereum', symbol: 'ETH' },
		{ name: 'Polygon', symbol: 'MATIC' },
		{ name: 'BSC', symbol: 'BNB' },
		{ name: 'Arbitrum', symbol: 'ARB' },
		{ name: 'Base', symbol: 'BASE' },
		{ name: 'Solana', symbol: 'SOL' },
		{ name: 'Bitcoin', symbol: 'BTC' }
	];

	const features = [
		{
			title: 'Multi-Chain Payments',
			description: 'Accept payments on Ethereum, Polygon, BSC, Arbitrum, Base, Solana, and Bitcoin through a single unified API.',
			icon: 'chains'
		},
		{
			title: 'Recurring Billing',
			description: 'The first crypto subscription engine that actually works. Weekly, monthly, quarterly, yearly — with automatic dunning.',
			icon: 'billing'
		},
		{
			title: 'Auto-Convert to Stablecoins',
			description: 'Receive ETH, BTC, or SOL and auto-convert to USDC or USDT at the time of payment. Zero volatility risk.',
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
			title: 'HD Wallet Isolation',
			description: 'Every payment gets a unique deposit address derived from BIP-44 HD wallets. No address reuse, ever.',
			icon: 'wallet'
		}
	];

	const metrics = [
		{ value: '7', label: 'Blockchains' },
		{ value: '<1s', label: 'API Latency' },
		{ value: '99.99%', label: 'Uptime SLA' },
		{ value: '0.5%', label: 'Transaction Fee' }
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
				Now processing on 7 networks
			</div>

			<h1 class="animate-fade-up-delay-1 text-[clamp(2.5rem,6vw,4.5rem)] font-bold leading-[1.08] tracking-[-0.035em] mb-6">
				The payment infrastructure<br />
				<span class="bg-gradient-to-r from-brand-400 via-brand-300 to-purple-300 bg-clip-text text-transparent">for crypto-native businesses</span>
			</h1>

			<p class="animate-fade-up-delay-2 text-lg text-surface-400 max-w-xl mx-auto mb-10 leading-relaxed">
				Accept payments, manage subscriptions, and settle in stablecoins — all through a single API. Built for developers who ship fast.
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
					<div class="flex items-center gap-2 text-surface-500 hover:text-surface-300 transition-colors">
						<span class="text-[13px] font-medium">{chain.name}</span>
						<span class="text-[11px] text-surface-600 font-mono">{chain.symbol}</span>
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
					<p class="text-[13px] text-surface-400 leading-relaxed">We monitor the blockchain, confirm transactions, fire webhooks, and auto-convert to stablecoins.</p>
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
				<p class="text-surface-400">No monthly fees. Pay only when you get paid.</p>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<!-- Free -->
				<div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8">
					<div class="text-[13px] font-medium text-surface-400 mb-1">Free</div>
					<div class="text-3xl font-bold mb-1">1.0%</div>
					<div class="text-[12px] text-surface-500 mb-6">per transaction</div>
					<ul class="space-y-3 text-[13px] text-surface-400">
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							All 7 blockchains
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Hosted checkout
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							Webhook notifications
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
					<div class="text-3xl font-bold mb-1">0.5%</div>
					<div class="text-[12px] text-surface-500 mb-6">per transaction</div>
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
							Auto-convert to stablecoins
						</li>
						<li class="flex items-center gap-2">
							<svg class="w-4 h-4 text-brand-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
							1,000 req/min API limit
						</li>
					</ul>
					<a href="/auth/register" class="block mt-8 text-center px-4 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-400 text-[13px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20">
						Start with Pro
					</a>
				</div>

				<!-- Enterprise -->
				<div class="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8">
					<div class="text-[13px] font-medium text-surface-400 mb-1">Enterprise</div>
					<div class="text-3xl font-bold mb-1">Custom</div>
					<div class="text-[12px] text-surface-500 mb-6">volume-based pricing</div>
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
					<a href="mailto:sales@paychains.dev" class="block mt-8 text-center px-4 py-2.5 rounded-xl border border-white/[0.08] text-[13px] font-medium hover:bg-white/[0.04] transition-colors">
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
			</div>
			<p class="text-[11px] text-surface-600">&copy; 2026 PayChains. All rights reserved.</p>
		</div>
	</footer>
</div>
