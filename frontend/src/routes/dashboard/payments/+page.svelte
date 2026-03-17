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
	<div class="flex items-center justify-between mb-8">
		<div>
			<h1 class="text-xl font-bold tracking-tight">Payments</h1>
			<p class="text-[13px] text-surface-400 mt-1">All payment transactions across chains</p>
		</div>
		<div class="flex gap-2">
			<select bind:value={statusFilter}
				class="px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[13px] text-surface-300 outline-none focus:border-brand-500/40">
				<option value="">All statuses</option>
				<option value="pending">Pending</option>
				<option value="confirming">Confirming</option>
				<option value="completed">Completed</option>
				<option value="failed">Failed</option>
				<option value="expired">Expired</option>
			</select>
			<select bind:value={chainFilter}
				class="px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[13px] text-surface-300 outline-none focus:border-brand-500/40">
				<option value="">All chains</option>
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

	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
		{#if loading}
			<div class="p-12 text-center text-surface-500 text-[13px]">Loading payments...</div>
		{:else if payments.length === 0}
			<div class="p-12 text-center">
				<div class="text-[13px] text-surface-500">No payments yet. Create your first payment via the API.</div>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead>
						<tr class="border-b border-white/[0.06]">
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">ID</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Amount</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Token</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Chain</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Address</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Created</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/[0.04]">
						{#each payments as payment}
							<tr class="hover:bg-white/[0.02] transition-colors">
								<td class="px-5 py-3.5 text-[12px] font-mono text-surface-500">{payment.id.slice(0, 8)}...</td>
								<td class="px-5 py-3.5 text-[13px] font-medium tabular-nums">{formatUSD(payment.amount_usd)}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300">{payment.token}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300 capitalize">{payment.chain}</td>
								<td class="px-5 py-3.5">
									<span class="px-2 py-0.5 rounded-md text-[11px] font-medium {statusColor(payment.status)}">
										{payment.status}
									</span>
								</td>
								<td class="px-5 py-3.5 text-[12px] font-mono text-surface-500">{shortenAddress(payment.deposit_address)}</td>
								<td class="px-5 py-3.5 text-[12px] text-surface-500">{formatDate(payment.created_at)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>
