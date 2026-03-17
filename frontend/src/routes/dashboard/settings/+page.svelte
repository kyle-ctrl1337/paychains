<script lang="ts">
	import { auth, setAuth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { onMount } from 'svelte';

	let merchant = $state<any>(null);
	let token = $state('');
	let webhookUrl = $state('');
	let autoConvert = $state('USDC');
	let saving = $state(false);
	let saved = $state(false);

	// API key display
	let apiKeyLive = $state('');
	let apiKeyTest = $state('');
	let showKeys = $state(false);
	let rolling = $state(false);
	let newKeys = $state<{ live: string; test: string } | null>(null);

	onMount(() => {
		auth.subscribe((state) => {
			if (!state.token) return;
			token = state.token;
			merchant = state.merchant;
			webhookUrl = state.merchant?.webhook_url || '';
			autoConvert = state.merchant?.auto_convert_to || 'USDC';
			apiKeyLive = state.apiKeyLive || '••••••••••••••••';
			apiKeyTest = state.apiKeyTest || '••••••••••••••••';
		});
	});

	async function saveSettings() {
		saving = true;
		saved = false;
		try {
			const updated = await api.updateMe(token, {
				webhook_url: webhookUrl || null,
				auto_convert_to: autoConvert
			});
			merchant = updated;
			saved = true;
			setTimeout(() => (saved = false), 3000);
		} catch {
		} finally {
			saving = false;
		}
	}

	async function rollKeys() {
		if (!confirm('Are you sure? This will invalidate your current API keys.')) return;
		rolling = true;
		try {
			const result = await api.rollApiKeys(token);
			newKeys = { live: result.api_key_live, test: result.api_key_test };
			apiKeyLive = result.api_key_live;
			apiKeyTest = result.api_key_test;
			// Update stored keys
			setAuth(token, merchant, result.api_key_live, result.api_key_test);
		} catch {
		} finally {
			rolling = false;
		}
	}

	function copyToClipboard(text: string) {
		navigator.clipboard.writeText(text);
	}
</script>

<div class="max-w-2xl">
	<h1 class="text-2xl font-bold mb-8">Settings</h1>

	<!-- API Keys -->
	<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 mb-6">
		<h2 class="text-lg font-semibold mb-4">API Keys</h2>

		{#if newKeys}
			<div class="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg mb-4">
				<p class="text-sm font-medium text-yellow-800 dark:text-yellow-300">New keys generated! Save them now — they won't be shown again.</p>
			</div>
		{/if}

		<div class="space-y-4">
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Live Key</label>
				<div class="flex gap-2">
					<div class="flex-1 p-2.5 bg-gray-100 dark:bg-gray-800 rounded-lg font-mono text-xs truncate">
						{showKeys ? apiKeyLive : '••••••••••••••••••••••••'}
					</div>
					<button onclick={() => copyToClipboard(apiKeyLive)}
						class="px-3 py-1 text-xs border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">Copy</button>
				</div>
			</div>
			<div>
				<label class="block text-xs font-medium text-gray-500 mb-1">Test Key</label>
				<div class="flex gap-2">
					<div class="flex-1 p-2.5 bg-gray-100 dark:bg-gray-800 rounded-lg font-mono text-xs truncate">
						{showKeys ? apiKeyTest : '••••••••••••••••••••••••'}
					</div>
					<button onclick={() => copyToClipboard(apiKeyTest)}
						class="px-3 py-1 text-xs border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">Copy</button>
				</div>
			</div>
		</div>

		<div class="flex gap-3 mt-4">
			<button onclick={() => (showKeys = !showKeys)}
				class="px-3 py-1.5 text-xs font-medium border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition">
				{showKeys ? 'Hide' : 'Show'} Keys
			</button>
			<button onclick={rollKeys} disabled={rolling}
				class="px-3 py-1.5 text-xs font-medium text-red-600 border border-red-300 dark:border-red-700 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition">
				{rolling ? 'Regenerating...' : 'Regenerate Keys'}
			</button>
		</div>
	</div>

	<!-- Webhook & Settings -->
	<form
		onsubmit={(e) => { e.preventDefault(); saveSettings(); }}
		class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 space-y-4"
	>
		<h2 class="text-lg font-semibold">Configuration</h2>

		<div>
			<label class="block text-sm font-medium mb-1">Webhook URL</label>
			<input bind:value={webhookUrl}
				class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm"
				placeholder="https://yourapp.com/webhooks/paychains" />
			<p class="text-xs text-gray-500 mt-1">We'll POST payment events to this URL.</p>
		</div>

		<div>
			<label class="block text-sm font-medium mb-1">Auto-Convert To</label>
			<select bind:value={autoConvert}
				class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm">
				<option value="USDC">USDC</option>
				<option value="USDT">USDT</option>
				<option value="none">Don't convert (keep original token)</option>
			</select>
		</div>

		<div class="flex items-center gap-3">
			<button type="submit" disabled={saving}
				class="px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-400 text-white text-sm font-medium rounded-lg transition">
				{saving ? 'Saving...' : 'Save Settings'}
			</button>
			{#if saved}
				<span class="text-sm text-green-600">Saved!</span>
			{/if}
		</div>
	</form>
</div>
