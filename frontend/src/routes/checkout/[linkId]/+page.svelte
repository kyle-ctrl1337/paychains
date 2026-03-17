<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { formatUSD } from '$lib/utils/format';
	import { api } from '$lib/api/client';
	import QRCode from 'qrcode';

	let linkId = $state('');
	let checkoutData = $state<any>(null);
	let paymentResult = $state<any>(null);
	let selectedChain = $state('');
	let selectedToken = $state('');
	let loading = $state(true);
	let initiating = $state(false);
	let error = $state('');
	let paymentStatus = $state('');
	let confirmations = $state(0);
	let pollInterval: ReturnType<typeof setInterval>;
	let countdownInterval: ReturnType<typeof setInterval>;
	let timeRemaining = $state('');
	let timeWarning = $state(false);
	let copied = $state(false);
	let qrDataUrl = $state('');

	function formatCrypto(amount: string | number, token: string): string {
		const num = parseFloat(String(amount));
		if (['USDC', 'USDT', 'DAI'].includes(token)) return num.toFixed(2);
		return num.toFixed(6);
	}

	const comingSoonChains = ['solana', 'bitcoin'];

	const chainMeta: Record<string, { symbol: string; name: string; color: string }> = {
		ethereum: { symbol: 'ETH', name: 'Ethereum', color: 'bg-blue-500' },
		polygon: { symbol: 'MATIC', name: 'Polygon', color: 'bg-purple-500' },
		bsc: { symbol: 'BNB', name: 'BNB Chain', color: 'bg-yellow-500' },
		arbitrum: { symbol: 'ARB', name: 'Arbitrum', color: 'bg-sky-500' },
		base: { symbol: 'BASE', name: 'Base', color: 'bg-blue-600' },
		solana: { symbol: 'SOL', name: 'Solana', color: 'bg-gradient-to-r from-purple-500 to-teal-400' },
		bitcoin: { symbol: 'BTC', name: 'Bitcoin', color: 'bg-orange-500' }
	};

	onMount(() => {
		const unsub = page.subscribe((p) => {
			linkId = p.params.linkId;
		});
		loadCheckout();
		return () => {
			unsub();
			if (pollInterval) clearInterval(pollInterval);
			if (countdownInterval) clearInterval(countdownInterval);
		};
	});

	async function loadCheckout() {
		try {
			checkoutData = await api.getCheckout(linkId);
		} catch (e: any) {
			error = e.message || 'Payment link not found';
		} finally {
			loading = false;
		}
	}

	async function initiate() {
		if (!selectedChain || !selectedToken) return;
		initiating = true;
		error = '';
		try {
			paymentResult = await api.initiateCheckout(linkId, {
				chain: selectedChain,
				token: selectedToken
			});
			paymentStatus = 'pending';
			if (paymentResult.deposit_address) {
				qrDataUrl = await QRCode.toDataURL(paymentResult.deposit_address, { width: 200, margin: 2, color: { dark: '#000000', light: '#ffffff' } });
			}
			startPolling();
			startCountdown();
		} catch (e: any) {
			error = e.message || 'Failed to initiate payment';
		} finally {
			initiating = false;
		}
	}

	function startPolling() {
		pollInterval = setInterval(async () => {
			if (!paymentResult) return;
			try {
				const data = await api.checkPaymentStatus(paymentResult.payment_id);
				paymentStatus = data.status;
				if (data.confirmations !== undefined) {
					confirmations = data.confirmations;
				}
				if (data.status === 'completed' || data.status === 'failed' || data.status === 'expired') {
					clearInterval(pollInterval);
					if (countdownInterval) clearInterval(countdownInterval);
				}
			} catch {
				// Silently retry on next interval
			}
		}, 3000);
	}

	function startCountdown() {
		if (!paymentResult?.expires_at) return;
		const updateTimer = () => {
			const now = Date.now();
			const expires = new Date(paymentResult.expires_at).getTime();
			const diff = expires - now;
			if (diff <= 0) {
				timeRemaining = '00:00';
				timeWarning = true;
				if (countdownInterval) clearInterval(countdownInterval);
				return;
			}
			const minutes = Math.floor(diff / 60000);
			const seconds = Math.floor((diff % 60000) / 1000);
			timeRemaining = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
			timeWarning = minutes < 5;
		};
		updateTimer();
		countdownInterval = setInterval(updateTimer, 1000);
	}

	async function copyAddress() {
		if (!paymentResult?.deposit_address) return;
		try {
			await navigator.clipboard.writeText(paymentResult.deposit_address);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		} catch {
			// Fallback for older browsers
			const el = document.createElement('textarea');
			el.value = paymentResult.deposit_address;
			document.body.appendChild(el);
			el.select();
			document.execCommand('copy');
			document.body.removeChild(el);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		}
	}
</script>

<svelte:head>
	<title>{checkoutData?.title ? `${checkoutData.title} — PayChains Checkout` : 'PayChains Checkout'}</title>
</svelte:head>

<!-- Background with subtle grid -->
<div class="min-h-screen flex flex-col items-center justify-center bg-surface-950 px-4 py-8 relative">
	<!-- Grid pattern overlay -->
	<div
		class="pointer-events-none absolute inset-0 opacity-[0.03]"
		style="background-image: url(&quot;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M60 0H0v60' fill='none' stroke='white' stroke-width='0.5'/%3E%3C/svg%3E&quot;);"
	></div>

	<div class="w-full max-w-lg relative z-10">
		{#if loading}
			<!-- Loading State -->
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl p-8 text-center shadow-2xl">
				<div class="flex flex-col items-center gap-4">
					<div class="h-10 w-10 rounded-full border-2 border-brand-500 border-t-transparent animate-spin"></div>
					<p class="text-surface-400 text-sm">Loading checkout...</p>
				</div>
			</div>
		{:else if error && !checkoutData}
			<!-- Error State -->
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl p-8 text-center shadow-2xl">
				<div class="flex flex-col items-center gap-3">
					<div class="h-12 w-12 rounded-full bg-red-500/10 flex items-center justify-center">
						<svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</div>
					<p class="text-red-400 text-sm font-medium">{error}</p>
					<p class="text-surface-500 text-xs">This payment link may be invalid or expired.</p>
				</div>
			</div>
		{:else if paymentResult}
			<!-- Payment Created — Deposit Info -->
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl shadow-2xl overflow-hidden">
				<!-- Header -->
				<div class="px-8 pt-8 pb-6 text-center border-b border-white/[0.06]">
					<h2 class="text-lg font-semibold text-white">{checkoutData.title}</h2>
					<p class="text-3xl font-bold text-white mt-2">{formatUSD(checkoutData.amount_usd)}</p>
					<p class="text-sm text-surface-400 mt-1">
						{formatCrypto(paymentResult.amount_crypto, paymentResult.token)} {paymentResult.token}
						<span class="text-surface-500">on</span>
						<span class="capitalize">{paymentResult.chain}</span>
					</p>
				</div>

				<div class="p-8 space-y-6">
					<!-- Countdown Timer -->
					{#if timeRemaining && paymentStatus === 'pending'}
						<div class="flex items-center justify-center gap-2 {timeWarning ? 'text-amber-400' : 'text-surface-400'}">
							<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<span class="text-sm font-mono font-medium {timeWarning ? 'animate-pulse' : ''}">{timeRemaining}</span>
							<span class="text-xs {timeWarning ? 'text-amber-400/70' : 'text-surface-500'}">remaining</span>
						</div>
					{/if}

					<!-- QR Code -->
					{#if qrDataUrl && (paymentStatus === 'pending' || paymentStatus === 'confirming')}
						<div class="flex justify-center">
							<div class="rounded-xl bg-white p-3">
								<img src={qrDataUrl} alt="Deposit address QR code" class="w-44 h-44" />
							</div>
						</div>
					{/if}

					<!-- Deposit Address -->
					<div class="rounded-xl bg-surface-950/60 border border-white/[0.04] p-4">
						<div class="flex items-center justify-between mb-2">
							<p class="text-xs text-surface-500 uppercase tracking-wider font-medium">Deposit Address</p>
							<button
								onclick={copyAddress}
								class="flex items-center gap-1.5 text-xs font-medium transition-colors {copied ? 'text-emerald-400' : 'text-brand-400 hover:text-brand-300'}"
							>
								{#if copied}
									<svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
									</svg>
									Copied!
								{:else}
									<svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
									</svg>
									Copy
								{/if}
							</button>
						</div>
						<p class="font-mono text-sm text-surface-300 break-all select-all leading-relaxed">{paymentResult.deposit_address}</p>
					</div>

					<!-- Status Indicator -->
					<div class="rounded-xl border p-4 text-center
						{paymentStatus === 'pending' ? 'border-amber-500/20 bg-amber-500/5' : ''}
						{paymentStatus === 'confirming' ? 'border-blue-500/20 bg-blue-500/5' : ''}
						{paymentStatus === 'completed' ? 'border-emerald-500/20 bg-emerald-500/5' : ''}
						{paymentStatus === 'expired' ? 'border-red-500/20 bg-red-500/5' : ''}
					">
						{#if paymentStatus === 'pending'}
							<div class="flex items-center justify-center gap-2.5 text-amber-400">
								<div class="h-2.5 w-2.5 rounded-full bg-amber-400 animate-pulse"></div>
								<span class="text-sm font-medium">Waiting for payment...</span>
							</div>
							<p class="text-xs text-surface-500 mt-1.5">Send the exact amount to the address above</p>
						{:else if paymentStatus === 'confirming'}
							<div class="flex items-center justify-center gap-2.5 text-blue-400">
								<div class="h-2.5 w-2.5 rounded-full bg-blue-400 animate-pulse"></div>
								<span class="text-sm font-medium">Confirming transaction...</span>
							</div>
							{#if confirmations > 0}
								<p class="text-xs text-blue-400/70 mt-1.5">{confirmations} confirmation{confirmations !== 1 ? 's' : ''}</p>
							{/if}
						{:else if paymentStatus === 'completed'}
							<div class="flex items-center justify-center gap-2.5 text-emerald-400">
								<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
								<span class="text-sm font-semibold">Payment Confirmed!</span>
							</div>
							<p class="text-xs text-emerald-400/70 mt-1.5">Thank you for your payment</p>
						{:else if paymentStatus === 'expired'}
							<div class="flex items-center justify-center gap-2.5 text-red-400">
								<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
								<span class="text-sm font-medium">Payment Expired</span>
							</div>
							<p class="text-xs text-surface-500 mt-1.5">This payment session has timed out</p>
						{/if}
					</div>
				</div>
			</div>
		{:else}
			<!-- Chain / Token Selection -->
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl shadow-2xl overflow-hidden">
				<!-- Header -->
				<div class="px-8 pt-8 pb-6 text-center border-b border-white/[0.06]">
					<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-medium mb-4">
						<div class="h-1.5 w-1.5 rounded-full bg-brand-400"></div>
						Secure Checkout
					</div>
					<h2 class="text-lg font-semibold text-white">{checkoutData.title}</h2>
					{#if checkoutData.description}
						<p class="text-sm text-surface-400 mt-1">{checkoutData.description}</p>
					{/if}
					<p class="text-3xl font-bold text-white mt-3">{formatUSD(checkoutData.amount_usd)}</p>
				</div>

				<div class="p-8">
					{#if error}
						<div class="p-3 mb-5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
							{error}
						</div>
					{/if}

					<!-- Chain Selection -->
					<div class="mb-6">
						<label class="block text-xs font-medium text-surface-400 uppercase tracking-wider mb-3">Select Network</label>
						<div class="grid grid-cols-3 gap-2">
							{#each checkoutData.accepted_chains as chain}
								{@const isComingSoon = comingSoonChains.includes(chain)}
								{@const meta = chainMeta[chain] || { symbol: chain.toUpperCase(), name: chain, color: 'bg-surface-500' }}
								<button
									onclick={() => { if (!isComingSoon) selectedChain = chain; }}
									disabled={isComingSoon}
									class="relative p-3 rounded-xl border text-center transition-all duration-150
										{isComingSoon
											? 'border-white/[0.04] bg-surface-950/40 opacity-50 cursor-not-allowed'
											: selectedChain === chain
												? 'border-brand-500 bg-brand-500/10 text-brand-300 ring-1 ring-brand-500/30'
												: 'border-white/[0.06] bg-surface-950/40 hover:border-white/[0.12] hover:bg-surface-950/60 text-surface-300'}"
								>
									{#if isComingSoon}
										<span class="absolute -top-1.5 -right-1.5 px-1.5 py-0.5 rounded-full bg-surface-700 text-[9px] font-semibold text-surface-300 uppercase tracking-wide">Soon</span>
									{/if}
									<div class="text-base font-bold">{meta.symbol}</div>
									<div class="text-[10px] capitalize mt-0.5 {selectedChain === chain ? 'text-brand-400' : 'text-surface-500'}">{meta.name}</div>
								</button>
							{/each}
						</div>
					</div>

					<!-- Token Selection -->
					<div class="mb-8">
						<label class="block text-xs font-medium text-surface-400 uppercase tracking-wider mb-3">Select Token</label>
						<div class="grid grid-cols-4 gap-2">
							{#each checkoutData.accepted_tokens as token}
								<button
									onclick={() => (selectedToken = token)}
									class="p-2.5 rounded-xl border text-sm font-semibold text-center transition-all duration-150
										{selectedToken === token
											? 'border-brand-500 bg-brand-500/10 text-brand-300 ring-1 ring-brand-500/30'
											: 'border-white/[0.06] bg-surface-950/40 hover:border-white/[0.12] hover:bg-surface-950/60 text-surface-300'}"
								>
									{token}
								</button>
							{/each}
						</div>
					</div>

					<!-- Pay Button -->
					<button
						onclick={initiate}
						disabled={!selectedChain || !selectedToken || initiating}
						class="w-full py-3.5 rounded-xl font-semibold text-sm transition-all duration-150
							{!selectedChain || !selectedToken || initiating
								? 'bg-surface-800 text-surface-500 cursor-not-allowed'
								: 'bg-brand-500 hover:bg-brand-400 text-white shadow-lg shadow-brand-500/20 hover:shadow-brand-500/30'}"
					>
						{#if initiating}
							<span class="flex items-center justify-center gap-2">
								<div class="h-4 w-4 rounded-full border-2 border-white/30 border-t-white animate-spin"></div>
								Generating address...
							</span>
						{:else}
							Pay Now
						{/if}
					</button>
				</div>
			</div>
		{/if}

		<!-- Powered by PayChains footer -->
		<div class="text-center mt-6">
			<a
				href="/"
				class="inline-flex items-center gap-1.5 text-xs text-surface-500 hover:text-surface-400 transition-colors"
			>
				Powered by
				<span class="font-semibold text-brand-400">PayChains</span>
			</a>
		</div>
	</div>
</div>
