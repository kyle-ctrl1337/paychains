<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';

	let paymentId = $state('');
	let payment = $state<any>(null);
	let targetPlan = $state('pro');
	let loading = $state(true);
	let error = $state('');
	let paymentStatus = $state('pending');
	let confirmations = $state(0);
	let timeRemaining = $state('');
	let timeWarning = $state(false);
	let copied = $state(false);
	let pollInterval: ReturnType<typeof setInterval>;
	let countdownInterval: ReturnType<typeof setInterval>;

	onMount(() => {
		const unsub = page.subscribe((p) => {
			paymentId = p.params.paymentId;
		});
		// Get plan from URL search params
		const params = new URLSearchParams(window.location.search);
		targetPlan = params.get('plan') || 'pro';
		// Use public checkout status endpoint (payment belongs to admin, not upgrading merchant)
		if (paymentId) loadPayment();
		return () => {
			unsub();
			if (pollInterval) clearInterval(pollInterval);
			if (countdownInterval) clearInterval(countdownInterval);
		};
	});

	async function loadPayment() {
		try {
			// Use public status endpoint — the upgrading merchant doesn't own this payment
			payment = await api.checkPaymentStatus(paymentId);
			paymentStatus = payment.status;
			if (payment.status === 'pending' || payment.status === 'confirming') {
				startPolling();
				startCountdown();
			}
		} catch (e: any) {
			error = e.message || 'Payment not found';
		} finally {
			loading = false;
		}
	}

	function startPolling() {
		pollInterval = setInterval(async () => {
			try {
				const data = await api.checkPaymentStatus(paymentId);
				paymentStatus = data.status;
				if (data.confirmations !== undefined) confirmations = data.confirmations;
				if (data.status === 'completed') {
					clearInterval(pollInterval);
					if (countdownInterval) clearInterval(countdownInterval);
					setTimeout(() => {
						window.location.href = `/dashboard/settings?upgraded=${targetPlan}`;
					}, 3000);
				}
				if (data.status === 'failed' || data.status === 'expired') {
					clearInterval(pollInterval);
					if (countdownInterval) clearInterval(countdownInterval);
				}
			} catch {}
		}, 3000);
	}

	function startCountdown() {
		if (!payment?.expires_at) return;
		const updateTimer = () => {
			const now = Date.now();
			const expires = new Date(payment.expires_at).getTime();
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
		if (!payment?.deposit_address) return;
		try {
			await navigator.clipboard.writeText(payment.deposit_address);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		} catch {
			const el = document.createElement('textarea');
			el.value = payment.deposit_address;
			document.body.appendChild(el);
			el.select();
			document.execCommand('copy');
			document.body.removeChild(el);
			copied = true;
			setTimeout(() => (copied = false), 2000);
		}
	}

	const planNames: Record<string, string> = { pro: 'Pro', enterprise: 'Enterprise' };
</script>

<svelte:head>
	<title>Upgrade Plan — PayChains</title>
</svelte:head>

<div class="min-h-screen flex flex-col items-center justify-center bg-surface-950 px-4 py-8 relative">
	<div class="pointer-events-none absolute inset-0 opacity-[0.03]"
		style="background-image: url(&quot;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M60 0H0v60' fill='none' stroke='white' stroke-width='0.5'/%3E%3C/svg%3E&quot;);">
	</div>

	<div class="w-full max-w-lg relative z-10">
		{#if loading}
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl p-8 text-center shadow-2xl">
				<div class="flex flex-col items-center gap-4">
					<div class="h-10 w-10 rounded-full border-2 border-brand-500 border-t-transparent animate-spin"></div>
					<p class="text-surface-400 text-sm">Loading upgrade details...</p>
				</div>
			</div>
		{:else if error}
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl p-8 text-center shadow-2xl">
				<div class="flex flex-col items-center gap-3">
					<div class="h-12 w-12 rounded-full bg-red-500/10 flex items-center justify-center">
						<svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</div>
					<p class="text-red-400 text-sm font-medium">{error}</p>
					<a href="/dashboard/settings" class="text-brand-400 hover:text-brand-300 text-sm font-medium transition-colors">Back to Settings</a>
				</div>
			</div>
		{:else if payment}
			<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl shadow-2xl overflow-hidden">
				<!-- Header -->
				<div class="px-8 pt-8 pb-6 text-center border-b border-white/[0.06]">
					<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-medium mb-4">
						<div class="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
							<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
								<polyline points="4 12 9 17 20 6" />
							</svg>
						</div>
						PayChains
					</div>
					<h2 class="text-lg font-semibold text-white">
						Upgrade to {planNames[targetPlan] || 'Pro'}
					</h2>
					<p class="text-3xl font-bold text-white mt-2">${payment.amount_usd}</p>
					<p class="text-sm text-surface-400 mt-1">
						{parseFloat(payment.amount_crypto).toFixed(2)} {payment.token}
						<span class="text-surface-500">on</span>
						<span class="capitalize">{payment.chain}</span>
					</p>
					<p class="text-[11px] text-surface-500 mt-1">per month</p>
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

					<!-- Deposit Address -->
					<div class="rounded-xl bg-surface-950/60 border border-white/[0.04] p-4">
						<div class="flex items-center justify-between mb-2">
							<p class="text-xs text-surface-500 uppercase tracking-wider font-medium">Send to Address</p>
							<button onclick={copyAddress}
								class="flex items-center gap-1.5 text-xs font-medium transition-colors {copied ? 'text-emerald-400' : 'text-brand-400 hover:text-brand-300'}">
								{copied ? 'Copied!' : 'Copy'}
							</button>
						</div>
						<p class="font-mono text-sm text-surface-300 break-all select-all leading-relaxed">{payment.deposit_address}</p>
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
								<span class="text-sm font-semibold">Plan Upgraded!</span>
							</div>
							<p class="text-xs text-emerald-400/70 mt-1.5">Redirecting to dashboard...</p>
						{:else if paymentStatus === 'expired'}
							<div class="flex items-center justify-center gap-2.5 text-red-400">
								<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
								<span class="text-sm font-medium">Payment Expired</span>
							</div>
							<p class="text-xs text-surface-500 mt-1.5">
								<a href="/dashboard/settings" class="text-brand-400 hover:text-brand-300">Go back to settings</a> and try again
							</p>
						{/if}
					</div>
				</div>
			</div>
		{/if}

		<div class="text-center mt-6">
			<a href="/" class="inline-flex items-center gap-1.5 text-xs text-surface-500 hover:text-surface-400 transition-colors">
				Powered by <span class="font-semibold text-brand-400">PayChains</span>
			</a>
		</div>
	</div>
</div>
