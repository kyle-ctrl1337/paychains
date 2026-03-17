<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD } from '$lib/utils/format';
	import { onMount } from 'svelte';
	import { Chart, DoughnutController, ArcElement, Tooltip, Legend, LineController, LineElement, PointElement, CategoryScale, LinearScale, Filler } from 'chart.js';

	Chart.register(DoughnutController, ArcElement, Tooltip, Legend, LineController, LineElement, PointElement, CategoryScale, LinearScale, Filler);

	let overview = $state<any>(null);
	let chainData = $state<any[]>([]);
	let recentPayments = $state<any[]>([]);
	let loading = $state(true);
	let error = $state('');
	let hasXpub = $state(true);
	let chainChartEl = $state<HTMLCanvasElement>();
	let volumeChartEl = $state<HTMLCanvasElement>();
	let chainChart: Chart | null = null;
	let volumeChart: Chart | null = null;

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.token) return;
			hasXpub = !!state.merchant?.xpub_key;
			try {
				const auth_key = state.apiKeyTest || state.token;
				const [ov, chains, payments] = await Promise.all([
					api.getOverview(auth_key),
					api.getByChain(auth_key),
					api.listPayments(auth_key, 'per_page=10').catch(() => [])
				]);
				overview = ov;
				chainData = chains;
				recentPayments = payments;

				// Render charts after data is loaded
				setTimeout(() => {
					renderChainChart();
					renderVolumeChart();
				}, 50);
			} catch (e: any) {
				error = e.message;
			} finally {
				loading = false;
			}
		});

		return () => {
			chainChart?.destroy();
			volumeChart?.destroy();
		};
	});

	const CHAIN_COLORS: Record<string, string> = {
		ethereum: '#627EEA',
		polygon: '#8247E5',
		bsc: '#F0B90B',
		arbitrum: '#28A0F0',
		base: '#0052FF',
		solana: '#9945FF',
		bitcoin: '#F7931A',
	};

	function renderChainChart() {
		if (!chainChartEl || chainData.length === 0) return;
		chainChart?.destroy();

		const labels = chainData.map(c => c.chain?.charAt(0).toUpperCase() + c.chain?.slice(1));
		const values = chainData.map(c => parseFloat(c.volume_usd) || 0);
		const colors = chainData.map(c => CHAIN_COLORS[c.chain] || '#6366f1');

		chainChart = new Chart(chainChartEl, {
			type: 'doughnut',
			data: {
				labels,
				datasets: [{
					data: values,
					backgroundColor: colors,
					borderColor: 'transparent',
					borderWidth: 0,
					hoverOffset: 4,
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				cutout: '70%',
				plugins: {
					legend: { display: false },
					tooltip: {
						backgroundColor: 'rgba(15, 15, 25, 0.95)',
						titleColor: '#fff',
						bodyColor: '#a0a0b0',
						borderColor: 'rgba(255,255,255,0.06)',
						borderWidth: 1,
						cornerRadius: 8,
						padding: 10,
						callbacks: {
							label: (ctx) => ` $${ctx.parsed.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
						}
					}
				}
			}
		});
	}

	function renderVolumeChart() {
		if (!volumeChartEl || recentPayments.length === 0) return;
		volumeChart?.destroy();

		// Group payments by date for last 7 days
		const now = new Date();
		const days: string[] = [];
		const volumes: number[] = [];

		for (let i = 6; i >= 0; i--) {
			const d = new Date(now);
			d.setDate(d.getDate() - i);
			const key = d.toISOString().slice(0, 10);
			days.push(d.toLocaleDateString('en-US', { weekday: 'short' }));

			const dayVolume = recentPayments
				.filter(p => p.created_at?.startsWith(key) && p.status === 'completed')
				.reduce((sum: number, p: any) => sum + (parseFloat(p.amount_usd) || 0), 0);
			volumes.push(dayVolume);
		}

		volumeChart = new Chart(volumeChartEl, {
			type: 'line',
			data: {
				labels: days,
				datasets: [{
					data: volumes,
					borderColor: '#6366f1',
					backgroundColor: 'rgba(99, 102, 241, 0.08)',
					borderWidth: 2,
					pointRadius: 0,
					pointHoverRadius: 5,
					pointHoverBackgroundColor: '#6366f1',
					pointHoverBorderColor: '#fff',
					pointHoverBorderWidth: 2,
					fill: true,
					tension: 0.4,
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					x: {
						grid: { color: 'rgba(255,255,255,0.03)' },
						ticks: { color: '#64748b', font: { size: 11 } },
						border: { display: false }
					},
					y: {
						grid: { color: 'rgba(255,255,255,0.03)' },
						ticks: {
							color: '#64748b',
							font: { size: 11 },
							callback: (v) => '$' + Number(v).toLocaleString()
						},
						border: { display: false },
						beginAtZero: true
					}
				},
				plugins: {
					legend: { display: false },
					tooltip: {
						backgroundColor: 'rgba(15, 15, 25, 0.95)',
						titleColor: '#fff',
						bodyColor: '#a0a0b0',
						borderColor: 'rgba(255,255,255,0.06)',
						borderWidth: 1,
						cornerRadius: 8,
						padding: 10,
						callbacks: {
							label: (ctx) => ` $${ctx.parsed.y.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
						}
					}
				}
			}
		});
	}

	function exportCSV() {
		if (!recentPayments.length) return;
		const headers = ['ID', 'Status', 'Amount USD', 'Token', 'Chain', 'Deposit Address', 'TX Hash', 'Created At'];
		const rows = recentPayments.map(p => [
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
		{#if overview && recentPayments.length > 0}
			<button
				onclick={exportCSV}
				class="inline-flex items-center gap-1.5 px-3 py-1.5 border border-white/[0.08] rounded-lg text-[12px] font-medium text-surface-300 hover:bg-white/[0.04] transition-colors"
			>
				<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"/></svg>
				Export CSV
			</button>
		{/if}
	</div>

	{#if !hasXpub}
		<div class="flex items-center gap-3 px-4 py-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 mb-6">
			<svg class="w-5 h-5 text-amber-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" stroke-linecap="round" stroke-linejoin="round"/></svg>
			<div class="flex-1">
				<span class="text-[13px] font-medium text-amber-300">Setup Required:</span>
				<span class="text-[13px] text-amber-200/80"> Add your wallet's extended public key in Settings to start receiving payments directly to your wallet.</span>
			</div>
			<a href="/dashboard/settings" class="shrink-0 px-3 py-1.5 bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/30 rounded-lg text-[12px] font-medium text-amber-300 transition-colors">
				Go to Settings
			</a>
		</div>
	{/if}

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

		<!-- Charts Row -->
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
			<!-- Volume Chart (2/3 width) -->
			<div class="lg:col-span-2 rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
				<div class="px-5 py-4 border-b border-white/[0.06]">
					<h2 class="text-[14px] font-semibold">Volume (Last 7 Days)</h2>
				</div>
				<div class="p-5 h-64">
					<canvas bind:this={volumeChartEl}></canvas>
				</div>
			</div>

			<!-- Chain Distribution (1/3 width) -->
			<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
				<div class="px-5 py-4 border-b border-white/[0.06]">
					<h2 class="text-[14px] font-semibold">By Chain</h2>
				</div>
				<div class="p-5 flex items-center justify-center h-64">
					{#if chainData.length > 0}
						<div class="w-full h-full relative">
							<canvas bind:this={chainChartEl}></canvas>
						</div>
					{:else}
						<div class="text-[13px] text-surface-500">No chain data</div>
					{/if}
				</div>
				{#if chainData.length > 0}
					<div class="px-5 pb-4 flex flex-wrap gap-3">
						{#each chainData as chain}
							<div class="flex items-center gap-1.5">
								<div class="w-2.5 h-2.5 rounded-full" style="background-color: {CHAIN_COLORS[chain.chain] || '#6366f1'}"></div>
								<span class="text-[11px] text-surface-400 capitalize">{chain.chain}</span>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>

		<!-- Chain Breakdown Table -->
		{#if chainData.length > 0}
			<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden mb-8">
				<div class="px-5 py-4 border-b border-white/[0.06]">
					<h2 class="text-[14px] font-semibold">Volume by Chain</h2>
				</div>
				<div class="divide-y divide-white/[0.04]">
					{#each chainData as chain}
						<div class="flex items-center justify-between px-5 py-3.5 hover:bg-white/[0.02] transition-colors">
							<div class="flex items-center gap-3">
								<div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background-color: {CHAIN_COLORS[chain.chain] || '#6366f1'}20">
									<span class="text-[11px] font-bold uppercase" style="color: {CHAIN_COLORS[chain.chain] || '#6366f1'}">{chain.chain?.substring(0, 3)}</span>
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

		<!-- Recent Payments -->
		{#if recentPayments.length > 0}
			<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
				<div class="px-5 py-4 border-b border-white/[0.06] flex items-center justify-between">
					<h2 class="text-[14px] font-semibold">Recent Payments</h2>
					<a href="/dashboard/payments" class="text-[12px] text-brand-400 hover:text-brand-300 font-medium transition-colors">View all</a>
				</div>
				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b border-white/[0.06]">
								<th class="px-5 py-2.5 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Amount</th>
								<th class="px-5 py-2.5 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Token</th>
								<th class="px-5 py-2.5 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Chain</th>
								<th class="px-5 py-2.5 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-white/[0.04]">
							{#each recentPayments.slice(0, 5) as p}
								<tr class="hover:bg-white/[0.02] transition-colors">
									<td class="px-5 py-3 text-[13px] font-medium tabular-nums">{formatUSD(p.amount_usd)}</td>
									<td class="px-5 py-3 text-[13px] text-surface-300">{p.token}</td>
									<td class="px-5 py-3 text-[13px] text-surface-300 capitalize">{p.chain}</td>
									<td class="px-5 py-3">
										<span class="px-2 py-0.5 rounded-md text-[11px] font-medium
											{p.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
											 p.status === 'pending' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
											 p.status === 'confirming' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
											 'bg-surface-500/10 text-surface-400 border border-surface-500/20'}">
											{p.status}
										</span>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/if}
	{/if}
</div>
