<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD, formatDate, statusColor } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let subscriptions = $state<any[]>([]);
	let loading = $state(true);

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.apiKeyTest) return;
			try {
				subscriptions = await api.listSubscriptions(state.apiKeyTest);
			} catch {
				subscriptions = [];
			} finally {
				loading = false;
			}
		});
	});
</script>

<div>
	<h1 class="text-2xl font-bold mb-6">Subscriptions</h1>

	<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
		{#if loading}
			<div class="p-8 text-center text-gray-500">Loading subscriptions...</div>
		{:else if subscriptions.length === 0}
			<div class="p-8 text-center text-gray-500">
				No subscriptions yet. Create your first subscription via the API.
			</div>
		{:else}
			<table class="w-full">
				<thead class="bg-gray-50 dark:bg-gray-800/50 text-xs text-gray-500 uppercase">
					<tr>
						<th class="px-6 py-3 text-left">Plan</th>
						<th class="px-6 py-3 text-left">Customer</th>
						<th class="px-6 py-3 text-left">Amount</th>
						<th class="px-6 py-3 text-left">Interval</th>
						<th class="px-6 py-3 text-left">Status</th>
						<th class="px-6 py-3 text-left">Next Payment</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-gray-800">
					{#each subscriptions as sub}
						<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
							<td class="px-6 py-4 text-sm font-medium">{sub.plan_name}</td>
							<td class="px-6 py-4 text-sm text-gray-500">{sub.customer_email || sub.customer_wallet || '—'}</td>
							<td class="px-6 py-4 text-sm">{formatUSD(sub.amount_usd)}</td>
							<td class="px-6 py-4 text-sm capitalize">{sub.interval}</td>
							<td class="px-6 py-4">
								<span class="px-2 py-1 rounded-full text-xs font-medium {statusColor(sub.status)}">
									{sub.status}
								</span>
							</td>
							<td class="px-6 py-4 text-sm text-gray-500">{formatDate(sub.next_payment_at)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>
