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
	<div class="mb-8">
		<h1 class="text-xl font-bold tracking-tight">Payouts</h1>
		<p class="text-[13px] text-surface-400 mt-1">Withdraw funds to your settlement address</p>
	</div>

	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
		{#if loading}
			<div class="p-12 text-center text-surface-500 text-[13px]">Loading payouts...</div>
		{:else if payouts.length === 0}
			<div class="p-12 text-center">
				<div class="text-[13px] text-surface-500">No payouts yet. Request a payout once you have completed payments.</div>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead>
						<tr class="border-b border-white/[0.06]">
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Amount</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Token</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Chain</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Created</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/[0.04]">
						{#each payouts as payout}
							<tr class="hover:bg-white/[0.02] transition-colors">
								<td class="px-5 py-3.5 text-[13px] font-medium tabular-nums">{payout.amount} {payout.token}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300">{payout.token}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300 capitalize">{payout.chain}</td>
								<td class="px-5 py-3.5">
									<span class="px-2 py-0.5 rounded-md text-[11px] font-medium {statusColor(payout.status)}">
										{payout.status}
									</span>
								</td>
								<td class="px-5 py-3.5 text-[12px] text-surface-500">{formatDate(payout.created_at)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
