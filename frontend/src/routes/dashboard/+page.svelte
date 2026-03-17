<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let overview = $state<any>(null);
	let chainData = $state<any[]>([]);
	let loading = $state(true);
	let error = $state('');

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.apiKeyTest) return;
			try {
				const [ov, chains] = await Promise.all([
					api.getOverview(state.apiKeyTest),
					api.getByChain(state.apiKeyTest)
				]);
				overview = ov;
				chainData = chains;
			} catch (e: any) {
				error = e.message;
			} finally {
				loading = false;
			}
		});
	});
</script>

<div>
	<h1 class="text-2xl font-bold mb-8">Dashboard Overview</h1>

	{#if loading}
		<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
			{#each Array(4) as _}
				<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 animate-pulse">
					<div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24 mb-3"></div>
					<div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-32"></div>
				</div>
			{/each}
		</div>
	{:else if error}
		<div class="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg text-yellow-700 dark:text-yellow-300">
			No data yet — start by creating a payment to see your dashboard populate.
		</div>
	{:else if overview}
		<!-- Stats Cards -->
		<div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
				<p class="text-sm text-gray-500 mb-1">Total Volume</p>
				<p class="text-2xl font-bold">{formatUSD(overview.total_volume_usd)}</p>
			</div>
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
				<p class="text-sm text-gray-500 mb-1">Transactions</p>
				<p class="text-2xl font-bold">{overview.total_transactions}</p>
			</div>
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
				<p class="text-sm text-gray-500 mb-1">Revenue (Fees)</p>
				<p class="text-2xl font-bold text-green-600">{formatUSD(overview.total_revenue_usd)}</p>
			</div>
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
				<p class="text-sm text-gray-500 mb-1">Active Subscriptions</p>
				<p class="text-2xl font-bold">{overview.active_subscriptions}</p>
			</div>
		</div>

		<!-- Chain Breakdown -->
		{#if chainData.length > 0}
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
				<h2 class="text-lg font-semibold mb-4">Volume by Chain</h2>
				<div class="space-y-3">
					{#each chainData as chain}
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<span class="text-sm font-medium capitalize">{chain.chain}</span>
								<span class="text-xs text-gray-500">{chain.transaction_count} txns</span>
							</div>
							<span class="font-medium">{formatUSD(chain.volume_usd)}</span>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	{/if}
</div>
