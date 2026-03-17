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
			if (!state.token) return;
			await loadPayments(state.apiKeyTest || state.token);
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

	function exportCSV() {
		if (!payments.length) return;
		const headers = ['ID', 'Status', 'Amount USD', 'Token', 'Chain', 'Deposit Address', 'TX Hash', 'Created At'];
		const rows = payments.map(p => [
			p.id, p.status, p.amount_usd, p.token, p.chain, p.deposit_address, p.tx_hash || '', p.created_at
		]);
		const csv = [headers, ...rows].map(r => r.map((c: string) => `"${c}"`).join(',')).join('\n');
		const blob = new Blob([csv], { type: 'text/csv' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `paychains-payments-${new Date().toISOString().slice(0, 10)}.csv`;
		a.click();
		URL.revokeObjectURL(url);
	}
</script>

<div>
	<div class="flex items-center justify-between mb-8">
		<div>
			<h1 class="text-xl font-bold tracking-tight">Payments</h1>
			<p class="text-[13px] text-surface-400 mt-1">All payment transactions across chains</p>
		</div>
		<div class="flex gap-2">
			{#if payments.length > 0}
				<button
					onclick={exportCSV}
					class="inline-flex items-center gap-1.5 px-3 py-1.5 border border-white/[0.08] rounded-lg text-[12px] font-medium text-surface-300 hover:bg-white/[0.04] transition-colors"
				>
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"/></svg>
					CSV
				</button>
			{/if}
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
							{@const isOpenable = (payment.status === 'pending' || payment.status === 'confirming') && new Date(payment.expires_at) > new Date()}
							<tr class="hover:bg-white/[0.02] transition-colors {isOpenable ? 'cursor-pointer' : ''}"
								onclick={() => { if (isOpenable) window.location.href = `/dashboard/payments/${payment.id}`; }}>
								<td class="px-5 py-3.5 text-[12px] font-mono text-surface-500">{payment.id.slice(0, 8)}...</td>
								<td class="px-5 py-3.5 text-[13px] font-medium tabular-nums">{formatUSD(payment.amount_usd)}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300">{payment.token}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-300 capitalize">{payment.chain}</td>
								<td class="px-5 py-3.5">
									<span class="px-2 py-0.5 rounded-md text-[11px] font-medium {statusColor(payment.status)}">
										{payment.status}
									</span>
									{#if isOpenable}
										<span class="ml-1.5 text-[10px] text-brand-400">Open</span>
									{/if}
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
