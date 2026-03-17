<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD, formatDate, shortenAddress, statusColor } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let payments = $state<any[]>([]);
	let loading = $state(true);
	let statusFilter = $state('');
	let chainFilter = $state('');

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.apiKeyTest) return;
			await loadPayments(state.apiKeyTest);
		});
	});

	async function loadPayments(apiKey: string) {
		loading = true;
		try {
			const params = new URLSearchParams();
			if (statusFilter) params.set('status', statusFilter);
			if (chainFilter) params.set('chain', chainFilter);
			payments = await api.listPayments(apiKey, params.toString());
		} catch {
			payments = [];
		} finally {
			loading = false;
		}
	}
</script>

<div>
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-bold">Payments</h1>
		<div class="flex gap-3">
			<select
				bind:value={statusFilter}
				class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm"
			>
				<option value="">All Statuses</option>
				<option value="pending">Pending</option>
				<option value="confirming">Confirming</option>
				<option value="completed">Completed</option>
				<option value="failed">Failed</option>
				<option value="expired">Expired</option>
			</select>
			<select
				bind:value={chainFilter}
				class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm"
			>
				<option value="">All Chains</option>
				<option value="ethereum">Ethereum</option>
				<option value="polygon">Polygon</option>
				<option value="bsc">BSC</option>
				<option value="arbitrum">Arbitrum</option>
				<option value="base">Base</option>
				<option value="solana">Solana</option>
				<option value="bitcoin">Bitcoin</option>
			</select>
		</div>
	</div>

	<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
		{#if loading}
			<div class="p-8 text-center text-gray-500">Loading payments...</div>
		{:else if payments.length === 0}
			<div class="p-8 text-center text-gray-500">
				No payments yet. Create your first payment via the API.
			</div>
		{:else}
			<table class="w-full">
				<thead class="bg-gray-50 dark:bg-gray-800/50 text-xs text-gray-500 uppercase">
					<tr>
						<th class="px-6 py-3 text-left">ID</th>
						<th class="px-6 py-3 text-left">Amount</th>
						<th class="px-6 py-3 text-left">Token</th>
						<th class="px-6 py-3 text-left">Chain</th>
						<th class="px-6 py-3 text-left">Status</th>
						<th class="px-6 py-3 text-left">Address</th>
						<th class="px-6 py-3 text-left">Created</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-gray-800">
					{#each payments as payment}
						<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
							<td class="px-6 py-4 text-sm font-mono text-gray-500">{payment.id.slice(0, 8)}...</td>
							<td class="px-6 py-4 text-sm font-medium">{formatUSD(payment.amount_usd)}</td>
							<td class="px-6 py-4 text-sm">{payment.token}</td>
							<td class="px-6 py-4 text-sm capitalize">{payment.chain}</td>
							<td class="px-6 py-4">
								<span class="px-2 py-1 rounded-full text-xs font-medium {statusColor(payment.status)}">
									{payment.status}
								</span>
							</td>
							<td class="px-6 py-4 text-sm font-mono text-gray-500">{shortenAddress(payment.deposit_address)}</td>
							<td class="px-6 py-4 text-sm text-gray-500">{formatDate(payment.created_at)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>
