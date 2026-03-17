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

	let apiKeyLive = $state('');
	let apiKeyTest = $state('');
	let showKeys = $state(false);
	let rolling = $state(false);
	let newKeys = $state<{ live: string; test: string } | null>(null);
	let copiedKey = $state('');

	onMount(() => {
		auth.subscribe((state) => {
			if (!state.token) return;
			token = state.token;
			merchant = state.merchant;
			webhookUrl = state.merchant?.webhook_url || '';
			autoConvert = state.merchant?.auto_convert_to || 'USDC';
			apiKeyLive = state.apiKeyLive || '';
			apiKeyTest = state.apiKeyTest || '';
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
			setAuth(token, merchant, result.api_key_live, result.api_key_test);
		} catch {
		} finally {
			rolling = false;
		}
	}

	function copyToClipboard(text: string, type: string) {
		navigator.clipboard.writeText(text);
		copiedKey = type;
		setTimeout(() => copiedKey = '', 2000);
	}
</script>

<div class="max-w-2xl">
	<div class="mb-8">
		<h1 class="text-xl font-bold tracking-tight">Settings</h1>
		<p class="text-[13px] text-surface-400 mt-1">Manage your API keys and configuration</p>
	</div>

	<!-- API Keys -->
	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 mb-6">
		<h2 class="text-[15px] font-semibold mb-4">API Keys</h2>

		{#if newKeys}
			<div class="flex items-center gap-2 px-3 py-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 mb-4">
				<svg class="w-4 h-4 text-amber-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" stroke-linecap="round" stroke-linejoin="round"/></svg>
				<span class="text-[12px] text-amber-300">New keys generated. Save them now — they won't be shown again.</span>
			</div>
		{/if}

		<div class="space-y-4">
			<div>
				<label class="flex items-center justify-between text-[12px] font-medium text-surface-400 mb-1.5">
					Live Key
					<button onclick={() => copyToClipboard(apiKeyLive, 'live')} class="text-brand-400 hover:text-brand-300 transition-colors">
						{copiedKey === 'live' ? 'Copied!' : 'Copy'}
					</button>
				</label>
				<div class="px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] font-mono text-[12px] text-surface-400 truncate">
					{showKeys ? apiKeyLive : '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}
				</div>
			</div>
			<div>
				<label class="flex items-center justify-between text-[12px] font-medium text-surface-400 mb-1.5">
					Test Key
					<button onclick={() => copyToClipboard(apiKeyTest, 'test')} class="text-brand-400 hover:text-brand-300 transition-colors">
						{copiedKey === 'test' ? 'Copied!' : 'Copy'}
					</button>
				</label>
				<div class="px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] font-mono text-[12px] text-surface-400 truncate">
					{showKeys ? apiKeyTest : '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}
				</div>
			</div>
		</div>

		<div class="flex gap-2 mt-4">
			<button onclick={() => (showKeys = !showKeys)}
				class="px-3 py-1.5 text-[12px] font-medium border border-white/[0.08] rounded-lg hover:bg-white/[0.04] transition-colors">
				{showKeys ? 'Hide keys' : 'Show keys'}
			</button>
			<button onclick={rollKeys} disabled={rolling}
				class="px-3 py-1.5 text-[12px] font-medium text-red-400 border border-red-500/20 rounded-lg hover:bg-red-500/[0.06] transition-colors">
				{rolling ? 'Regenerating...' : 'Regenerate keys'}
			</button>
		</div>
	</div>

	<!-- Configuration -->
	<form onsubmit={(e) => { e.preventDefault(); saveSettings(); }}
		class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 space-y-5">
		<h2 class="text-[15px] font-semibold">Configuration</h2>

		<div>
			<label class="block text-[13px] font-medium text-surface-300 mb-1.5">Webhook URL</label>
			<input bind:value={webhookUrl}
				class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
				placeholder="https://yourapp.com/webhooks/paychains" />
			<p class="text-[12px] text-surface-500 mt-1.5">We'll POST payment events to this URL with HMAC-SHA256 signatures.</p>
		</div>

		<div>
			<label class="block text-[13px] font-medium text-surface-300 mb-1.5">Auto-Convert To</label>
			<select bind:value={autoConvert}
				class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] text-surface-300 outline-none focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 transition-all">
				<option value="USDC">USDC</option>
				<option value="USDT">USDT</option>
				<option value="none">Don't convert (keep original token)</option>
			</select>
		</div>

		<div class="flex items-center gap-3">
			<button type="submit" disabled={saving}
				class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-semibold transition-all">
				{saving ? 'Saving...' : 'Save settings'}
			</button>
			{#if saved}
				<span class="text-[13px] text-emerald-400 flex items-center gap-1">
					<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
					Saved
				</span>
			{/if}
		</div>
	</form>
</div>
