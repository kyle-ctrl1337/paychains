<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { formatUSD, formatDate } from '$lib/utils/format';
	import { onMount } from 'svelte';

	let links = $state<any[]>([]);
	let loading = $state(true);
	let showCreate = $state(false);

	// Create form
	let title = $state('');
	let description = $state('');
	let amountUsd = $state('');
	let creating = $state(false);
	let apiKey = $state('');

	onMount(() => {
		auth.subscribe(async (state) => {
			if (!state.apiKeyTest) return;
			apiKey = state.apiKeyTest;
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
	}
</script>

<div>
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-bold">Payment Links</h1>
		<button
			onclick={() => (showCreate = !showCreate)}
			class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white text-sm font-medium rounded-lg transition"
		>
			{showCreate ? 'Cancel' : '+ Create Link'}
		</button>
	</div>

	{#if showCreate}
		<form
			onsubmit={(e) => { e.preventDefault(); createLink(); }}
			class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-6 space-y-4"
		>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label class="block text-sm font-medium mb-1">Title</label>
					<input bind:value={title} required
						class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm" placeholder="Premium Plan" />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1">Amount (USD)</label>
					<input bind:value={amountUsd} type="number" step="0.01"
						class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm" placeholder="49.99 (leave empty for custom)" />
				</div>
			</div>
			<div>
				<label class="block text-sm font-medium mb-1">Description</label>
				<textarea bind:value={description}
					class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm" rows="2" placeholder="Optional description"></textarea>
			</div>
			<button type="submit" disabled={creating}
				class="px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-400 text-white text-sm font-medium rounded-lg transition">
				{creating ? 'Creating...' : 'Create Payment Link'}
			</button>
		</form>
	{/if}

	<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
		{#if loading}
			<div class="p-8 text-center text-gray-500">Loading...</div>
		{:else if links.length === 0}
			<div class="p-8 text-center text-gray-500">No payment links yet.</div>
		{:else}
			<div class="divide-y divide-gray-200 dark:divide-gray-800">
				{#each links as link}
					<div class="p-6 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/30 transition">
						<div>
							<h3 class="font-medium">{link.title}</h3>
							<p class="text-sm text-gray-500 mt-0.5">
								{link.amount_usd ? formatUSD(link.amount_usd) : 'Custom amount'} &bull;
								{link.accepted_chains.length} chains &bull;
								Created {formatDate(link.created_at)}
							</p>
						</div>
						<div class="flex items-center gap-2">
							<span class="px-2 py-1 rounded-full text-xs font-medium {link.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}">
								{link.is_active ? 'Active' : 'Inactive'}
							</span>
							<button onclick={() => copyLink(link.id)}
								class="px-3 py-1.5 text-xs font-medium border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition">
								Copy Link
							</button>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
