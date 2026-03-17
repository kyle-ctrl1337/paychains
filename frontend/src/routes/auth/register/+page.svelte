<script lang="ts">
	import { api } from '$lib/api/client';
	import { setAuth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let email = $state('');
	let password = $state('');
	let companyName = $state('');
	let error = $state('');
	let loading = $state(false);
	let apiKeys = $state<{ live: string; test: string } | null>(null);
	let copied = $state('');

	async function handleRegister() {
		error = '';
		loading = true;
		try {
			const result: any = await api.register({
				email,
				password,
				company_name: companyName || undefined
			});
			apiKeys = { live: result.api_key_live, test: result.api_key_test };
			const loginResult = await api.login({ email, password });
			setAuth(loginResult.access_token, loginResult.merchant, result.api_key_live, result.api_key_test);
		} catch (e: any) {
			error = e.message || 'Registration failed';
		} finally {
			loading = false;
		}
	}

	function copyKey(key: string, type: string) {
		navigator.clipboard.writeText(key);
		copied = type;
		setTimeout(() => copied = '', 2000);
	}

	function goToDashboard() {
		goto('/dashboard');
	}
</script>

<div class="min-h-screen flex bg-surface-950">
	<!-- Left panel -->
	<div class="hidden lg:flex lg:w-1/2 relative overflow-hidden items-center justify-center">
		<div class="grid-bg absolute inset-0"></div>
		<div class="hero-glow bg-brand-500 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
		<div class="relative z-10 max-w-md px-12">
			<div class="flex items-center gap-2.5 mb-8">
				<div class="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-lg font-semibold">PayChains</span>
			</div>
			<h2 class="text-2xl font-bold tracking-tight mb-3">Start accepting crypto in minutes</h2>
			<p class="text-surface-400 text-[14px] leading-relaxed mb-8">Get your API keys instantly. No approval process, no credit card required.</p>

			<div class="space-y-4">
				<div class="flex items-start gap-3">
					<div class="w-6 h-6 rounded-full bg-brand-500/20 flex items-center justify-center shrink-0 mt-0.5">
						<span class="text-[11px] font-bold text-brand-400">1</span>
					</div>
					<div>
						<div class="text-[13px] font-medium">Create account</div>
						<div class="text-[12px] text-surface-500">Email + password. That's it.</div>
					</div>
				</div>
				<div class="flex items-start gap-3">
					<div class="w-6 h-6 rounded-full bg-brand-500/20 flex items-center justify-center shrink-0 mt-0.5">
						<span class="text-[11px] font-bold text-brand-400">2</span>
					</div>
					<div>
						<div class="text-[13px] font-medium">Get API keys</div>
						<div class="text-[12px] text-surface-500">Live and test keys generated instantly.</div>
					</div>
				</div>
				<div class="flex items-start gap-3">
					<div class="w-6 h-6 rounded-full bg-brand-500/20 flex items-center justify-center shrink-0 mt-0.5">
						<span class="text-[11px] font-bold text-brand-400">3</span>
					</div>
					<div>
						<div class="text-[13px] font-medium">Accept payments</div>
						<div class="text-[12px] text-surface-500">On 7 blockchains, from day one.</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Right panel -->
	<div class="flex-1 flex items-center justify-center px-6 py-12">
		<div class="w-full max-w-sm">
			<a href="/" class="lg:hidden flex items-center gap-2 mb-10">
				<div class="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-[15px] font-semibold">PayChains</span>
			</a>

			{#if apiKeys}
				<!-- API Keys display -->
				<div class="animate-fade-up">
					<div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-5">
						<svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
					</div>
					<h1 class="text-xl font-bold tracking-tight mb-1">Account created</h1>
					<p class="text-[13px] text-surface-400 mb-6">Save your API keys now — they won't be shown again.</p>

					<div class="space-y-4">
						<div>
							<label class="flex items-center justify-between text-[12px] font-medium text-surface-400 mb-1.5">
								Live Key
								<button onclick={() => copyKey(apiKeys!.live, 'live')} class="text-brand-400 hover:text-brand-300 transition-colors">
									{copied === 'live' ? 'Copied!' : 'Copy'}
								</button>
							</label>
							<div class="px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] font-mono text-[12px] text-surface-300 break-all select-all">
								{apiKeys.live}
							</div>
						</div>
						<div>
							<label class="flex items-center justify-between text-[12px] font-medium text-surface-400 mb-1.5">
								Test Key
								<button onclick={() => copyKey(apiKeys!.test, 'test')} class="text-brand-400 hover:text-brand-300 transition-colors">
									{copied === 'test' ? 'Copied!' : 'Copy'}
								</button>
							</label>
							<div class="px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] font-mono text-[12px] text-surface-300 break-all select-all">
								{apiKeys.test}
							</div>
						</div>
					</div>

					<div class="flex items-center gap-2 mt-4 px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
						<svg class="w-4 h-4 text-amber-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" stroke-linecap="round" stroke-linejoin="round"/></svg>
						<span class="text-[12px] text-amber-300">These keys are shown only once. Store them securely.</span>
					</div>

					<button
						onclick={goToDashboard}
						class="w-full mt-6 py-2.5 bg-brand-500 hover:bg-brand-400 rounded-lg text-[14px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20"
					>
						Go to Dashboard
					</button>
				</div>
			{:else}
				<h1 class="text-xl font-bold tracking-tight mb-1">Create your account</h1>
				<p class="text-[13px] text-surface-400 mb-8">Get your API keys in 30 seconds</p>

				<form onsubmit={(e) => { e.preventDefault(); handleRegister(); }} class="space-y-5">
					{#if error}
						<div class="flex items-center gap-2 px-3 py-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-[13px]">
							<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
							{error}
						</div>
					{/if}

					<div>
						<label for="company" class="block text-[13px] font-medium text-surface-300 mb-1.5">Company name</label>
						<input
							id="company"
							type="text"
							bind:value={companyName}
							class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
							placeholder="Acme Inc. (optional)"
						/>
					</div>

					<div>
						<label for="email" class="block text-[13px] font-medium text-surface-300 mb-1.5">Email</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							required
							class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
							placeholder="you@company.com"
						/>
					</div>

					<div>
						<label for="password" class="block text-[13px] font-medium text-surface-300 mb-1.5">Password</label>
						<input
							id="password"
							type="password"
							bind:value={password}
							required
							minlength="8"
							class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
							placeholder="Min 8 characters"
						/>
					</div>

					<button
						type="submit"
						disabled={loading}
						class="w-full py-2.5 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-[14px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20"
					>
						{loading ? 'Creating account...' : 'Create account'}
					</button>
				</form>

				<p class="text-center text-[13px] text-surface-500 mt-6">
					Already have an account?
					<a href="/auth/login" class="text-brand-400 hover:text-brand-300 font-medium transition-colors">Sign in</a>
				</p>
			{/if}
		</div>
	</div>
</div>
