<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let token = $state('');
	let stats = $state<any>(null);
	let merchants = $state<any[]>([]);
	let payments = $state<any[]>([]);
	let loading = $state(true);
	let activeTab = $state<'overview' | 'merchants' | 'payments'>('overview');

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.token) return;
			if (!state.merchant?.is_admin) {
				goto('/dashboard');
				return;
			}
			token = state.token;
			await loadData();
		});
	});

	async function loadData() {
		loading = true;
		try {
			const [s, m, p] = await Promise.all([
				api.adminStats(token),
				api.adminMerchants(token),
				api.adminPayments(token)
			]);
			stats = s;
			merchants = m;
			payments = p;
		} catch (e) {
			console.error('Admin load error:', e);
		} finally {
			loading = false;
		}
	}

	async function toggleMerchantActive(merchant: any) {
		await api.adminUpdateMerchant(token, merchant.id, { is_active: !merchant.is_active });
		await loadData();
	}

	async function changePlan(merchant: any, plan: string) {
		await api.adminUpdateMerchant(token, merchant.id, { plan });
		await loadData();
	}

	function formatDate(iso: string) {
		return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
	}
</script>

<div>
	<div class="mb-8">
		<h1 class="text-xl font-bold tracking-tight">Admin Dashboard</h1>
		<p class="text-[13px] text-surface-400 mt-1">Platform overview and management</p>
	</div>

	<!-- Tabs -->
	<div class="flex gap-1 mb-6 border-b border-white/[0.06] pb-px">
		{#each [['overview', 'Overview'], ['merchants', 'Merchants'], ['payments', 'Payments']] as [key, label]}
			<button
				onclick={() => activeTab = key as any}
				class="px-4 py-2 text-[13px] font-medium transition-colors border-b-2 -mb-px
					{activeTab === key ? 'border-brand-400 text-white' : 'border-transparent text-surface-400 hover:text-surface-200'}"
			>{label}</button>
		{/each}
	</div>

	{#if loading}
		<div class="p-12 text-center text-surface-500 text-[13px]">Loading admin data...</div>
	{:else if activeTab === 'overview' && stats}
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
			{#each [
				{ label: 'Total Merchants', value: stats.total_merchants, sub: `${stats.active_merchants} active` },
				{ label: 'Total Payments', value: stats.total_payments, sub: `${stats.completed_payments} completed` },
				{ label: 'Total Volume', value: `$${stats.total_volume_usd.toFixed(2)}`, color: 'text-emerald-400' },
				{ label: 'Total Fees Earned', value: `$${stats.total_fees_usd.toFixed(2)}`, color: 'text-brand-400' },
				{ label: 'Payment Links', value: stats.total_payment_links },
				{ label: 'Subscriptions', value: stats.total_subscriptions },
				{ label: 'Payouts', value: stats.total_payouts },
			] as stat}
				<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
					<div class="text-[12px] font-medium text-surface-500 uppercase tracking-wider mb-1">{stat.label}</div>
					<div class="text-2xl font-bold tabular-nums {stat.color || ''}">{stat.value}</div>
					{#if stat.sub}
						<div class="text-[12px] text-surface-500 mt-1">{stat.sub}</div>
					{/if}
				</div>
			{/each}
		</div>

	{:else if activeTab === 'merchants'}
		<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead>
						<tr class="border-b border-white/[0.06]">
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Email</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Company</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Plan</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Role</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Registered</th>
							<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Actions</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/[0.04]">
						{#each merchants as m}
							<tr class="hover:bg-white/[0.02] transition-colors">
								<td class="px-5 py-3.5 text-[13px] font-medium">{m.email}</td>
								<td class="px-5 py-3.5 text-[13px] text-surface-400">{m.company_name || '—'}</td>
								<td class="px-5 py-3.5">
									<select
										value={m.plan}
										onchange={(e) => changePlan(m, e.currentTarget.value)}
										class="px-2 py-1 rounded-md border border-white/[0.08] bg-white/[0.03] text-[12px] text-surface-300 outline-none"
									>
										<option value="free">Free</option>
										<option value="starter">Starter</option>
										<option value="growth">Growth</option>
										<option value="enterprise">Enterprise</option>
									</select>
								</td>
								<td class="px-5 py-3.5">
									<span class="px-2 py-0.5 rounded-md text-[11px] font-medium
										{m.is_active ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}">
										{m.is_active ? 'Active' : 'Disabled'}
									</span>
								</td>
								<td class="px-5 py-3.5">
									{#if m.is_admin}
										<span class="px-2 py-0.5 rounded-md text-[11px] font-medium bg-brand-500/10 text-brand-400 border border-brand-500/20">Admin</span>
									{:else}
										<span class="text-[12px] text-surface-500">User</span>
									{/if}
								</td>
								<td class="px-5 py-3.5 text-[12px] text-surface-500">{formatDate(m.created_at)}</td>
								<td class="px-5 py-3.5">
									<button
										onclick={() => toggleMerchantActive(m)}
										class="px-2.5 py-1 text-[12px] font-medium rounded-md border transition-colors
											{m.is_active
												? 'text-red-400 border-red-500/20 hover:bg-red-500/[0.06]'
												: 'text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/[0.06]'}"
									>
										{m.is_active ? 'Disable' : 'Enable'}
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

	{:else if activeTab === 'payments'}
		<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
			{#if payments.length === 0}
				<div class="p-12 text-center text-surface-500 text-[13px]">No payments yet across the platform.</div>
			{:else}
				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b border-white/[0.06]">
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">ID</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Merchant</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Amount</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Token</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Chain</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Status</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Fee</th>
								<th class="px-5 py-3 text-left text-[11px] font-medium text-surface-500 uppercase tracking-wider">Created</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-white/[0.04]">
							{#each payments as p}
								<tr class="hover:bg-white/[0.02] transition-colors">
									<td class="px-5 py-3.5 text-[12px] font-mono text-surface-500">{p.id.slice(0, 8)}...</td>
									<td class="px-5 py-3.5 text-[12px] font-mono text-surface-500">{p.merchant_id.slice(0, 8)}...</td>
									<td class="px-5 py-3.5 text-[13px] font-medium tabular-nums">${p.amount_usd}</td>
									<td class="px-5 py-3.5 text-[13px] text-surface-300">{p.token}</td>
									<td class="px-5 py-3.5 text-[13px] text-surface-300 capitalize">{p.chain}</td>
									<td class="px-5 py-3.5">
										<span class="px-2 py-0.5 rounded-md text-[11px] font-medium
											{p.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
											 p.status === 'pending' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
											 p.status === 'failed' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
											 'bg-surface-500/10 text-surface-400 border border-surface-500/20'}">
											{p.status}
										</span>
									</td>
									<td class="px-5 py-3.5 text-[12px] text-surface-500">{p.fee_amount_usd ? `$${p.fee_amount_usd}` : '—'}</td>
									<td class="px-5 py-3.5 text-[12px] text-surface-500">{formatDate(p.created_at)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>
	{/if}
</div>
