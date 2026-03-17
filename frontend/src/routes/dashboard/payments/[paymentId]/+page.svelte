<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import QRCode from 'qrcode';

	let paymentId = $state('');
	let payment = $state<any>(null);
	let loading = $state(true);
	let error = $state('');
	let paymentStatus = $state('pending');
	let confirmations = $state(0);
	let timeRemaining = $state('');
	let timeWarning = $state(false);
	let copied = $state(false);
	let qrDataUrl = $state('');
	let pollInterval: ReturnType<typeof setInterval>;
	let countdownInterval: ReturnType<typeof setInterval>;

	onMount(() => {
		const unsub = page.subscribe((p) => {
			paymentId = p.params.paymentId;
		});
		if (paymentId) loadPayment();
		return () => {
			unsub();
			if (pollInterval) clearInterval(pollInterval);
			if (countdownInterval) clearInterval(countdownInterval);
		};
	});

	async function loadPayment() {
		try {
			payment = await api.checkPaymentStatus(paymentId);
			paymentStatus = payment.status;
			if (payment.deposit_address) {
				qrDataUrl = await QRCode.toDataURL(payment.deposit_address, { width: 200, margin: 2, color: { dark: '#000000', light: '#ffffff' } });
			}
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
				if (data.status === 'completed' || data.status === 'failed' || data.status === 'expired') {
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
</script>

<div class="max-w-lg mx-auto">
	<a href="/dashboard/payments" class="inline-flex items-center gap-1.5 text-xs text-surface-400 hover:text-surface-300 transition-colors mb-6">
		<svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18"/></svg>
		Back to Payments
	</a>

	{#if loading}
		<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl p-8 text-center shadow-2xl">
			<div class="flex flex-col items-center gap-4">
				<div class="h-10 w-10 rounded-full border-2 border-brand-500 border-t-transparent animate-spin"></div>
				<p class="text-surface-400 text-sm">Loading payment...</p>
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
			</div>
		</div>
	{:else if payment}
		<div class="rounded-2xl border border-white/[0.06] bg-surface-900/80 backdrop-blur-xl shadow-2xl overflow-hidden">
			<!-- Header -->
			<div class="px-8 pt-8 pb-6 text-center border-b border-white/[0.06]">
				<p class="text-3xl font-bold text-white">${payment.amount_usd}</p>
				<p class="text-sm text-surface-400 mt-1">
					{parseFloat(payment.amount_crypto).toFixed(2)} {payment.token}
					<span class="text-surface-500">on</span>
					<span class="capitalize">{payment.chain}</span>
				</p>
				<p class="text-[11px] text-surface-500 mt-2 font-mono">{payment.payment_id || paymentId}</p>
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
					{paymentStatus === 'expired' || paymentStatus === 'failed' ? 'border-red-500/20 bg-red-500/5' : ''}
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
							<span class="text-sm font-semibold">Payment Complete</span>
						</div>
					{:else if paymentStatus === 'expired'}
						<div class="flex items-center justify-center gap-2.5 text-red-400">
							<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<span class="text-sm font-medium">Payment Expired</span>
						</div>
					{:else if paymentStatus === 'failed'}
						<div class="flex items-center justify-center gap-2.5 text-red-400">
							<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
							<span class="text-sm font-medium">Payment Failed</span>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
