<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD, formatDate } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let links = $state<any[]>([]);
	let loading = $state(true);
	let showCreate = $state(false);
	let title = $state('');
	let description = $state('');
	let amountUsd = $state('');
	let creating = $state(false);
	let apiKey = $state('');
	let copiedId = $state('');

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.token) return;
			apiKey = state.apiKeyTest || state.token;
			await loadLinks();
		});
	});

	async function loadLinks() {
		try {
			links = await api.listPaymentLinks(apiKey);
		} catch {
			links = [];
		} finally {
			loading = false;
		}
	}

	async function createLink() {
		creating = true;
		try {
			await api.createPaymentLink(apiKey, {
				title,
				description: description || undefined,
				amount_usd: amountUsd ? parseFloat(amountUsd) : undefined
			});
			showCreate = false;
			title = '';
			description = '';
			amountUsd = '';
			await loadLinks();
		} catch {
		} finally {
			creating = false;
		}
	}

	function copyLink(id: string) {
		const url = `${window.location.origin}/checkout/${id}`;
		navigator.clipboard.writeText(url);
		copiedId = id;
		setTimeout(() => copiedId = '', 2000);
	}
</script>

<div>
	<div class="flex items-center justify-between mb-8">
		<div>
			<h1 class="text-xl font-bold tracking-tight">Payment Links</h1>
			<p class="text-[13px] text-surface-400 mt-1">Shareable checkout pages for your customers</p>
		</div>
		<button
			onclick={() => (showCreate = !showCreate)}
			class="inline-flex items-center gap-1.5 px-4 py-2 bg-brand-500 hover:bg-brand-400 rounded-lg text-[13px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20"
		>
			{#if showCreate}
				Cancel
			{:else}
				<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 4.5v15m7.5-7.5h-15" stroke-linecap="round" stroke-linejoin="round"/></svg>
				Create Link
			{/if}
		</button>
	</div>

	{#if showCreate}
		<form onsubmit={(e) => { e.preventDefault(); createLink(); }}
			class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 mb-6 space-y-4">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label class="block text-[13px] font-medium text-surface-300 mb-1.5">Title</label>
					<input bind:value={title} required
						class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
						placeholder="Premium Plan" />
				</div>
				<div>
					<label class="block text-[13px] font-medium text-surface-300 mb-1.5">Amount (USD)</label>
					<input bind:value={amountUsd} type="number" step="0.01"
						class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
						placeholder="49.99 (leave empty for custom)" />
				</div>
			</div>
			<div>
				<label class="block text-[13px] font-medium text-surface-300 mb-1.5">Description</label>
				<textarea bind:value={description}
					class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all resize-none"
					rows="2" placeholder="Optional description"></textarea>
			</div>
			<button type="submit" disabled={creating}
				class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-semibold transition-all">
				{creating ? 'Creating...' : 'Create Payment Link'}
			</button>
		</form>
	{/if}

	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] overflow-hidden">
		{#if loading}
			<div class="p-12 text-center text-surface-500 text-[13px]">Loading...</div>
		{:else if links.length === 0}
			<div class="p-12 text-center">
				<div class="text-[13px] text-surface-500">No payment links yet.</div>
			</div>
		{:else}
			<div class="divide-y divide-white/[0.04]">
				{#each links as link}
					<div class="px-5 py-4 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
						<div>
							<h3 class="text-[14px] font-medium">{link.title}</h3>
							<p class="text-[12px] text-surface-500 mt-0.5">
								{link.amount_usd ? formatUSD(link.amount_usd) : 'Custom amount'} &middot;
								{link.accepted_chains?.length || 0} chains &middot;
								{formatDate(link.created_at)}
							</p>
						</div>
						<div class="flex items-center gap-2">
							<span class="px-2 py-0.5 rounded-md text-[11px] font-medium {link.is_active ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-surface-500/10 text-surface-400 border border-surface-500/20'}">
								{link.is_active ? 'Active' : 'Inactive'}
							</span>
							<button onclick={() => copyLink(link.id)}
								class="px-3 py-1.5 text-[12px] font-medium border border-white/[0.08] rounded-lg hover:bg-white/[0.04] transition-colors">
								{copiedId === link.id ? 'Copied!' : 'Copy Link'}
							</button>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
