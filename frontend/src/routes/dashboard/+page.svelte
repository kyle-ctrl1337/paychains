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

	const stats = $derived(overview ? [
		{ label: 'Total Volume', value: formatUSD(overview.total_volume_usd), change: null },
		{ label: 'Transactions', value: overview.total_transactions.toLocaleString(), change: null },
		{ label: 'Revenue', value: formatUSD(overview.total_revenue_usd), accent: true },
		{ label: 'Subscriptions', value: overview.active_subscriptions.toLocaleString(), change: null }
	] : []);
</script>

<div>
	<div class="flex items-center justify-between mb-8">
		<div>
			<h1 class="text-xl font-bold tracking-tight">Overview</h1>
			<p class="text-[13px] text-surface-400 mt-1">Your payment activity at a glance</p>
		</div>
	</div>

	{#if loading}
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
			{#each Array(4) as _}
				<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
					<div class="h-3 bg-white/[0.04] rounded w-20 mb-3"></div>
					<div class="h-7 bg-white/[0.04] rounded w-28"></div>
				</div>
			{/each}
		</div>
	{:else if error}
		<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-12 text-center">
			<div class="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mx-auto mb-4">
				<svg class="w-6 h-6 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" stroke-linecap="round" stroke-linejoin="round"/></svg>
			</div>
			<h3 class="text-[15px] font-semibold mb-1">No data yet</h3>
			<p class="text-[13px] text-surface-400 mb-6 max-w-sm mx-auto">Create your first payment to see analytics populate here.</p>
			<a href="/dashboard/payments" class="inline-flex items-center gap-2 px-4 py-2 bg-brand-500 hover:bg-brand-400 rounded-lg text-[13px] font-semibold transition-all">
				Create Payment
				<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
			</a>
		</div>
	{:else if overview}
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
			{#each stats as stat}
				<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5 hover:bg-white/[0.03] transition-colors">
					<div class="text-[12px] font-medium text-surface-400 mb-1">{stat.label}</div>
					<div class="text-2xl font-bold tracking-tight {stat.accent ? 'text-emerald-400' : 'text-white'}">
						{stat.value}
					</div>
				</div>
			{/each}
		</div>

		<!-- Chain Breakdown -->
		{#if chainData.length > 0}
			<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
				<div class="px-5 py-4 border-b border-white/[0.06]">
					<h2 class="text-[14px] font-semibold">Volume by Chain</h2>
				</div>
				<div class="divide-y divide-white/[0.04]">
					{#each chainData as chain}
						<div class="flex items-center justify-between px-5 py-3.5 hover:bg-white/[0.02] transition-colors">
							<div class="flex items-center gap-3">
								<div class="w-8 h-8 rounded-lg bg-white/[0.04] flex items-center justify-center">
									<span class="text-[11px] font-bold text-surface-400 uppercase">{chain.chain?.substring(0, 3)}</span>
								</div>
								<div>
									<span class="text-[13px] font-medium capitalize">{chain.chain}</span>
									<span class="text-[12px] text-surface-500 ml-2">{chain.transaction_count} transactions</span>
								</div>
							</div>
							<span class="text-[14px] font-semibold tabular-nums">{formatUSD(chain.volume_usd)}</span>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	{/if}
</div>
