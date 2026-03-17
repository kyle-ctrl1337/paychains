<script>
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		auth.subscribe((state) => {
			if (state.token) {
				goto('/dashboard');
			}
		});
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
	<nav class="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
		<div class="text-2xl font-bold tracking-tight">
			<span class="text-purple-400">Pay</span>Chains
		</div>
		<div class="flex gap-4">
			<a href="/auth/login" class="px-4 py-2 text-sm font-medium hover:text-purple-300 transition">Log In</a>
			<a href="/auth/register" class="px-4 py-2 text-sm font-medium bg-purple-600 hover:bg-purple-500 rounded-lg transition">Get Started</a>
		</div>
	</nav>

	<main class="max-w-7xl mx-auto px-8 py-24 text-center">
		<div class="inline-block px-4 py-1.5 bg-purple-500/20 border border-purple-500/30 rounded-full text-sm text-purple-300 mb-8">
			Now supporting 7 chains &bull; ETH, Polygon, BSC, Solana, Bitcoin & more
		</div>

		<h1 class="text-6xl font-bold tracking-tight leading-tight mb-6">
			Stripe for<br />
			<span class="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Crypto Payments</span>
		</h1>

		<p class="text-xl text-gray-300 max-w-2xl mx-auto mb-12">
			Accept crypto payments and subscriptions with a single API call.
			Auto-convert to stablecoins. Beautiful checkout. Recurring billing that actually works.
		</p>

		<div class="flex gap-4 justify-center mb-16">
			<a href="/auth/register" class="px-8 py-3 bg-purple-600 hover:bg-purple-500 rounded-lg font-medium text-lg transition">
				Start Building — Free
			</a>
			<a href="/dashboard" class="px-8 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg font-medium text-lg transition">
				View Dashboard
			</a>
		</div>

		<!-- Code Example -->
		<div class="max-w-xl mx-auto bg-gray-800/80 backdrop-blur rounded-xl border border-gray-700 overflow-hidden text-left">
			<div class="px-4 py-2 bg-gray-700/50 border-b border-gray-700 flex gap-2">
				<div class="w-3 h-3 rounded-full bg-red-500"></div>
				<div class="w-3 h-3 rounded-full bg-yellow-500"></div>
				<div class="w-3 h-3 rounded-full bg-green-500"></div>
			</div>
			<pre class="p-6 text-sm font-mono overflow-x-auto"><code class="text-gray-300"><span class="text-purple-400">const</span> payment = <span class="text-purple-400">await</span> paychains.payments.<span class="text-yellow-300">create</span>({'{'}
  <span class="text-green-400">amount_usd</span>: <span class="text-orange-300">49.99</span>,
  <span class="text-green-400">token</span>: <span class="text-orange-300">"USDC"</span>,
  <span class="text-green-400">chain</span>: <span class="text-orange-300">"polygon"</span>,
{'}'});

<span class="text-gray-500">// Returns deposit address + QR code</span>
console.<span class="text-yellow-300">log</span>(payment.deposit_address);
console.<span class="text-yellow-300">log</span>(payment.qr_code_base64);</code></pre>
		</div>

		<!-- Features Grid -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 text-left">
			<div class="p-6 bg-white/5 rounded-xl border border-white/10">
				<div class="text-3xl mb-3">&#9889;</div>
				<h3 class="text-lg font-semibold mb-2">Multi-Chain</h3>
				<p class="text-gray-400">Ethereum, Polygon, BSC, Arbitrum, Base, Solana, Bitcoin — all from one API.</p>
			</div>
			<div class="p-6 bg-white/5 rounded-xl border border-white/10">
				<div class="text-3xl mb-3">&#128260;</div>
				<h3 class="text-lg font-semibold mb-2">Recurring Billing</h3>
				<p class="text-gray-400">The first crypto subscription engine that works. Weekly, monthly, quarterly, yearly.</p>
			</div>
			<div class="p-6 bg-white/5 rounded-xl border border-white/10">
				<div class="text-3xl mb-3">&#128176;</div>
				<h3 class="text-lg font-semibold mb-2">Auto-Convert</h3>
				<p class="text-gray-400">Receive ETH, BTC, SOL — auto-convert to USDC. No volatility risk.</p>
			</div>
		</div>
	</main>
</div>
