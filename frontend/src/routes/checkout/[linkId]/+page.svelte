<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { formatUSD } from '$lib/utils/format';

	let linkId = $state('');
	let checkoutData = $state<any>(null);
	let paymentResult = $state<any>(null);
	let selectedChain = $state('');
	let selectedToken = $state('');
	let loading = $state(true);
	let initiating = $state(false);
	let error = $state('');
	let paymentStatus = $state('');
	let pollInterval: ReturnType<typeof setInterval>;

	const chainIcons: Record<string, string> = {
		ethereum: 'ETH',
		polygon: 'MATIC',
		bsc: 'BNB',
		arbitrum: 'ARB',
		base: 'BASE',
		solana: 'SOL',
		bitcoin: 'BTC'
	};

	onMount(() => {
		const unsub = page.subscribe((p) => {
			linkId = p.params.linkId;
		});
		loadCheckout();
		return () => {
			unsub();
			if (pollInterval) clearInterval(pollInterval);
		};
	});

	async function loadCheckout() {
		try {
			const res = await fetch(`/api/v1/checkout/${linkId}`);
			if (!res.ok) throw new Error('Payment link not found');
			checkoutData = await res.json();
		} catch (e: any) {
			error = e.message;
		} finally {
			loading = false;
		}
	}

	async function initiate() {
		if (!selectedChain || !selectedToken) return;
		initiating = true;
		error = '';
		try {
			const res = await fetch(`/api/v1/checkout/${linkId}/initiate`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ chain: selectedChain, token: selectedToken })
			});
			if (!res.ok) {
				const err = await res.json();
				throw new Error(err.detail || 'Failed to initiate');
			}
			paymentResult = await res.json();
			paymentStatus = 'pending';
			startPolling();
		} catch (e: any) {
			error = e.message;
		} finally {
			initiating = false;
		}
	}

	function startPolling() {
		pollInterval = setInterval(async () => {
			if (!paymentResult) return;
			try {
				const res = await fetch(`/api/v1/checkout/status/${paymentResult.payment_id}`);
				const data = await res.json();
				paymentStatus = data.status;
				if (data.status === 'completed' || data.status === 'failed' || data.status === 'expired') {
					clearInterval(pollInterval);
				}
			} catch {}
		}, 3000);
	}
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-950 px-4">
	<div class="w-full max-w-lg">
		{#if loading}
			<div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8 text-center">
				<p class="text-gray-500">Loading checkout...</p>
			</div>
		{:else if error && !checkoutData}
			<div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8 text-center">
				<p class="text-red-500">{error}</p>
			</div>
		{:else if paymentResult}
			<!-- Payment Created — Show deposit info -->
			<div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8">
				<div class="text-center mb-6">
					<h2 class="text-xl font-bold">{checkoutData.title}</h2>
					<p class="text-3xl font-bold mt-2">{formatUSD(checkoutData.amount_usd)}</p>
					<p class="text-sm text-gray-500 mt-1">{paymentResult.amount_crypto} {paymentResult.token}</p>
				</div>

				<!-- QR Code -->
				{#if paymentResult.qr_code_base64}
					<div class="flex justify-center mb-6">
						<img src="data:image/png;base64,{paymentResult.qr_code_base64}" alt="QR Code" class="w-48 h-48 rounded-lg" />
					</div>
				{/if}

				<!-- Deposit Address -->
				<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mb-6">
					<p class="text-xs text-gray-500 mb-1">Send {paymentResult.token} on {paymentResult.chain} to:</p>
					<p class="font-mono text-sm break-all select-all">{paymentResult.deposit_address}</p>
				</div>

				<!-- Status -->
				<div class="text-center">
					{#if paymentStatus === 'pending'}
						<div class="flex items-center justify-center gap-2 text-yellow-600">
							<div class="w-3 h-3 bg-yellow-500 rounded-full animate-pulse"></div>
							Waiting for payment...
						</div>
					{:else if paymentStatus === 'confirming'}
						<div class="flex items-center justify-center gap-2 text-blue-600">
							<div class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
							Confirming transaction...
						</div>
					{:else if paymentStatus === 'completed'}
						<div class="text-green-600 font-medium text-lg">Payment Confirmed!</div>
					{:else if paymentStatus === 'expired'}
						<div class="text-red-600 font-medium">Payment Expired</div>
					{/if}
				</div>
			</div>
		{:else}
			<!-- Chain/Token Selection -->
			<div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl p-8">
				<div class="text-center mb-6">
					<h2 class="text-xl font-bold">{checkoutData.title}</h2>
					{#if checkoutData.description}
						<p class="text-sm text-gray-500 mt-1">{checkoutData.description}</p>
					{/if}
					<p class="text-3xl font-bold mt-3">{formatUSD(checkoutData.amount_usd)}</p>
				</div>

				{#if error}
					<div class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 text-sm mb-4">
						{error}
					</div>
				{/if}

				<div class="mb-4">
					<label class="block text-sm font-medium mb-2">Select Chain</label>
					<div class="grid grid-cols-3 gap-2">
						{#each checkoutData.accepted_chains as chain}
							<button
								onclick={() => (selectedChain = chain)}
								class="p-3 rounded-lg border text-sm font-medium text-center transition
									{selectedChain === chain
										? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300'
										: 'border-gray-200 dark:border-gray-700 hover:border-gray-400'}"
							>
								<div class="text-lg">{chainIcons[chain] || chain}</div>
								<div class="text-xs capitalize mt-0.5">{chain}</div>
							</button>
						{/each}
					</div>
				</div>

				<div class="mb-6">
					<label class="block text-sm font-medium mb-2">Select Token</label>
					<div class="grid grid-cols-4 gap-2">
						{#each checkoutData.accepted_tokens as token}
							<button
								onclick={() => (selectedToken = token)}
								class="p-2.5 rounded-lg border text-sm font-medium text-center transition
									{selectedToken === token
										? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300'
										: 'border-gray-200 dark:border-gray-700 hover:border-gray-400'}"
							>
								{token}
							</button>
						{/each}
					</div>
				</div>

				<button
					onclick={initiate}
					disabled={!selectedChain || !selectedToken || initiating}
					class="w-full py-3 bg-purple-600 hover:bg-purple-500 disabled:bg-gray-300 dark:disabled:bg-gray-700 text-white rounded-lg font-medium transition"
				>
					{initiating ? 'Generating address...' : 'Pay Now'}
				</button>

				<p class="text-xs text-center text-gray-400 mt-4">
					Powered by <span class="font-medium">PayChains</span>
				</p>
			</div>
		{/if}
	</div>
</div>
