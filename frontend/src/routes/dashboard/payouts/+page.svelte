<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatDate, statusColor } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let payouts = $state<any[]>([]);
	let loading = $state(true);

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.apiKeyTest) return;
			try {
				payouts = await api.listPayouts(state.apiKeyTest);
			} catch {
				payouts = [];
			} finally {
				loading = false;
			}
		});
	});
</script>

<div>
	<h1 class="text-2xl font-bold mb-6">Payouts</h1>

	<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
		{#if loading}
			<div class="p-8 text-center text-gray-500">Loading payouts...</div>
		{:else if payouts.length === 0}
			<div class="p-8 text-center text-gray-500">
				No payouts yet. Request a payout once you have completed payments.
			</div>
		{:else}
			<table class="w-full">
				<thead class="bg-gray-50 dark:bg-gray-800/50 text-xs text-gray-500 uppercase">
					<tr>
						<th class="px-6 py-3 text-left">Amount</th>
						<th class="px-6 py-3 text-left">Token</th>
						<th class="px-6 py-3 text-left">Chain</th>
						<th class="px-6 py-3 text-left">Status</th>
						<th class="px-6 py-3 text-left">Created</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-gray-800">
					{#each payouts as payout}
						<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
							<td class="px-6 py-4 text-sm font-medium">{payout.amount} {payout.token}</td>
							<td class="px-6 py-4 text-sm">{payout.token}</td>
							<td class="px-6 py-4 text-sm capitalize">{payout.chain}</td>
							<td class="px-6 py-4">
								<span class="px-2 py-1 rounded-full text-xs font-medium {statusColor(payout.status)}">
									{payout.status}
								</span>
							</td>
							<td class="px-6 py-4 text-sm text-gray-500">{formatDate(payout.created_at)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>
