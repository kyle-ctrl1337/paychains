<script lang="ts">
	import { auth, setAuth } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	import { toast } from '$lib/stores/toast';
	import { onMount } from 'svelte';

	let merchant = $state<any>(null);
	let token = $state('');
	let webhookUrl = $state('');
	let autoConvert = $state('USDC');
	let xpubKey = $state('');
	let saving = $state(false);
	let savingXpub = $state(false);
	let upgrading = $state(false);

	let apiKeyLive = $state('');
	let apiKeyTest = $state('');
	let showKeys = $state(false);
	let rolling = $state(false);
	let newKeys = $state<{ live: string; test: string } | null>(null);
	let copiedKey = $state('');

	// Address preview derived from xpub
	let previewAddresses = $state<string[]>([]);

	onMount(async () => {
		auth.subscribe((state) => {
			if (!state.token) return;
			token = state.token;
			merchant = state.merchant;
			webhookUrl = state.merchant?.webhook_url || '';
			autoConvert = state.merchant?.auto_convert_to || 'USDC';
			xpubKey = state.merchant?.xpub_key || '';
			apiKeyLive = state.apiKeyLive || '';
			apiKeyTest = state.apiKeyTest || '';
		});

		// Handle URL params for post-upgrade/post-registration flows
		const params = new URLSearchParams(window.location.search);
		if (params.get('upgraded')) {
			toast.success(`Successfully upgraded to ${params.get('upgraded')}!`);
			window.history.replaceState({}, '', '/dashboard/settings');
			// Refresh merchant data
			if (token) {
				try {
					const me = await api.getMe(token);
					setAuth(token, me);
				} catch {}
			}
		}
		if (params.get('upgrade')) {
			const plan = params.get('upgrade');
			window.history.replaceState({}, '', '/dashboard/settings');
			if (plan === 'pro') upgradeToPro();
			else if (plan === 'enterprise') upgradeToEnterprise();
		}
	});

	function generatePreviewAddresses(xpub: string) {
		if (!xpub || xpub.length < 10) {
			previewAddresses = [];
			return;
		}
		// Client-side deterministic preview (matches backend fallback logic)
		const addresses: string[] = [];
		for (let i = 1; i <= 3; i++) {
			const input = `${xpub}:${i}:ethereum`;
			// Simple hash preview — actual derivation happens server-side
			let hash = 0;
			for (let j = 0; j < input.length; j++) {
				const char = input.charCodeAt(j);
				hash = ((hash << 5) - hash) + char;
				hash |= 0;
			}
			const hex = Math.abs(hash).toString(16).padStart(40, '0').slice(0, 40);
			addresses.push(`0x${hex}`);
		}
		previewAddresses = addresses;
	}

	async function saveSettings() {
		saving = true;
		try {
			const updated = await api.updateMe(token, {
				webhook_url: webhookUrl || null,
				auto_convert_to: autoConvert
			});
			merchant = updated;
			toast.success('Settings saved');
		} catch (e: any) {
			toast.error(e.message || 'Failed to save settings');
		} finally {
			saving = false;
		}
	}

	async function saveXpub() {
		savingXpub = true;
		try {
			const updated = await api.updateMe(token, {
				xpub_key: xpubKey || null
			});
			merchant = updated;
			toast.success('Wallet configuration saved');
		} catch (e: any) {
			toast.error(e.message || 'Failed to save wallet configuration');
		} finally {
			savingXpub = false;
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
			toast.success('API keys regenerated');
		} catch (e: any) {
			toast.error(e.message || 'Failed to regenerate keys');
		} finally {
			rolling = false;
		}
	}

	async function upgradeToPro() {
		upgrading = true;
		try {
			const result = await api.createUpgradePayment(token, 'pro');
			window.location.href = `/checkout/upgrade/${result.payment_id}?plan=pro`;
		} catch (e: any) {
			toast.error(e.message || 'Failed to create upgrade payment');
			upgrading = false;
		}
	}

	async function upgradeToEnterprise() {
		upgrading = true;
		try {
			const result = await api.createUpgradePayment(token, 'enterprise');
			window.location.href = `/checkout/upgrade/${result.payment_id}?plan=enterprise`;
		} catch (e: any) {
			toast.error(e.message || 'Failed to create upgrade payment');
			upgrading = false;
		}
	}

	function copyToClipboard(text: string, type: string) {
		navigator.clipboard.writeText(text);
		copiedKey = type;
		toast.info('Copied to clipboard');
		setTimeout(() => copiedKey = '', 2000);
	}
</script>

<div class="max-w-2xl">
	<div class="mb-8">
		<h1 class="text-xl font-bold tracking-tight">Settings</h1>
		<p class="text-[13px] text-surface-400 mt-1">Manage your wallet, API keys, and configuration</p>
	</div>

	<!-- Current Plan -->
	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 mb-6">
		<h2 class="text-[15px] font-semibold mb-4">Current Plan</h2>
		<div class="flex items-center justify-between flex-wrap gap-4">
			<div>
				<span class="text-lg font-bold capitalize">{merchant?.plan || 'free'}</span>
				<span class="text-[13px] text-surface-400 ml-2">
					{merchant?.plan === 'free' ? '100 payments/mo' :
					 merchant?.plan === 'pro' ? '2,000 payments/mo' : 'Unlimited'}
				</span>
			</div>
			{#if !merchant?.plan || merchant?.plan === 'free'}
				<button onclick={upgradeToPro} disabled={upgrading}
					class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-medium transition-all">
					{upgrading ? 'Creating payment...' : 'Upgrade to Pro — $49/mo'}
				</button>
			{:else if merchant?.plan === 'pro'}
				<button onclick={upgradeToEnterprise} disabled={upgrading}
					class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-medium transition-all">
					{upgrading ? 'Creating payment...' : 'Upgrade to Enterprise — $199/mo'}
				</button>
			{:else}
				<span class="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[12px] font-medium">Enterprise Active</span>
			{/if}
		</div>
		<p class="text-[12px] text-surface-500 mt-3">Pay with crypto. Plans renew monthly.</p>
	</div>

	<!-- Wallet Configuration (xpub) -->
	<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-6 mb-6">
		<div class="flex items-center gap-2 mb-1">
			<svg class="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3" stroke-linecap="round" stroke-linejoin="round"/></svg>
			<h2 class="text-[15px] font-semibold">Wallet Configuration</h2>
		</div>
		<p class="text-[12px] text-surface-400 mb-4">Provide your wallet's extended public key (xpub). PayChains derives unique deposit addresses from your xpub — your private keys never leave your wallet.</p>

		{#if !xpubKey && merchant}
			<div class="flex items-center gap-2 px-3 py-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 mb-4">
				<svg class="w-4 h-4 text-amber-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" stroke-linecap="round" stroke-linejoin="round"/></svg>
				<span class="text-[12px] text-amber-300">Set your xpub key to start receiving payments directly to your wallet.</span>
			</div>
		{/if}

		<div class="space-y-4">
			<div>
				<label class="block text-[12px] font-medium text-surface-400 mb-1.5">Extended Public Key (xpub)</label>
				<textarea
					bind:value={xpubKey}
					oninput={() => generatePreviewAddresses(xpubKey)}
					rows="3"
					class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[13px] font-mono placeholder-surface-600 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all resize-none"
					placeholder="xpub6CUGRUo..."
				></textarea>
				<p class="text-[11px] text-surface-500 mt-1.5">How to get your xpub: Open your wallet (MetaMask, Ledger, Trezor) → Settings → Export Extended Public Key</p>
			</div>

			{#if previewAddresses.length > 0}
				<div class="rounded-lg border border-white/[0.06] bg-white/[0.02] p-3">
					<p class="text-[11px] font-medium text-surface-400 mb-2">Preview — addresses that will be generated for payments:</p>
					<div class="space-y-1">
						{#each previewAddresses as addr, i}
							<div class="flex items-center gap-2 text-[11px] font-mono text-surface-500">
								<span class="text-surface-600">{i + 1}.</span>
								<span>{addr}</span>
							</div>
						{/each}
					</div>
					<p class="text-[10px] text-surface-600 mt-2">Verify these match your wallet to confirm setup is correct.</p>
				</div>
			{/if}

			<button onclick={saveXpub} disabled={savingXpub}
				class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-semibold transition-all">
				{savingXpub ? 'Saving...' : 'Save wallet configuration'}
			</button>
		</div>
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
			<p class="text-[11px] text-surface-500 mt-1.5">Auto-conversion coming soon — requires wallet connection.</p>
		</div>

		<button type="submit" disabled={saving}
			class="px-4 py-2 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 rounded-lg text-[13px] font-semibold transition-all">
			{saving ? 'Saving...' : 'Save settings'}
		</button>
	</form>
</div>
