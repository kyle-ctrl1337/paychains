<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD, formatDate, statusColor } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let subscriptions = $state<any[]>([]);
	let loading = $state(true);

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.token) return;
			try {
				subscriptions = await api.listSubscriptions(state.apiKeyTest || state.token);
			} catch {
				subscriptions = [];
			} finally {
				loading = false;
			}
		});
	});
</script>

<div>
	<div class="mb-8">
		<h1 class="text-xl font-bold tracking-tight">Subscriptions</h1>
		<p class="text-[13px] text-surface-400 mt-1">Manage recurring billing plans</p>
	</div>

	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
		{#if loading}
			<div class="p-12 text-center text-surface-500 text-[13px]">Loading subscriptions...</div>
		{:else if subscriptions.length === 0}
			<div class="p-12 text-center">
				<div class="text-[13px] text-surface-500">No subscriptions yet. Create your first subscription via the API.</div>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead>
						<tr class="border-b border-white/[0.06]">
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Plan</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Customer</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Amount</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Interval</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Next Payment</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/[0.04]">
						{#each subscriptions as sub}
							<tr class="hover:bg-white/[0.02] transition-colors">
								<td class="px-5 py-3.5 text-[13px] font-medium">{sub.plan_name}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-400">{sub.customer_email || sub.customer_wallet || '—'}</td>
								<td class="px-5 py-3.5 text-[13px] tabular-nums">{formatUSD(sub.amount_usd)}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300 capitalize">{sub.interval}</td>
								<td class="px-5 py-3.5">
									<span class="px-2 py-0.5 rounded-md text-[11px] font-medium {statusColor(sub.status)}">
										{sub.status}
									</span>
								</td>
								<td class="px-5 py-3.5 text-[12px] text-surface-500">{formatDate(sub.next_payment_at)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
