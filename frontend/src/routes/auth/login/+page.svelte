<script lang="ts">
	import { api } from '$lib/api/client';
	import { setAuth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleLogin() {
		error = '';
		loading = true;
		try {
			const result = await api.login({ email, password });
			setAuth(result.access_token, result.merchant);
			goto('/dashboard');
		} catch (e: any) {
			error = e.message || 'Login failed';
		} finally {
			loading = false;
		}
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
			<h2 class="text-2xl font-bold tracking-tight mb-3">The payment infrastructure for crypto-native businesses</h2>
			<p class="text-surface-400 text-[14px] leading-relaxed">Accept payments on 7 chains, manage subscriptions, and auto-convert to stablecoins — all through a single API.</p>
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

			<h1 class="text-xl font-bold tracking-tight mb-1">Welcome back</h1>
			<p class="text-[13px] text-surface-400 mb-8">Sign in to your merchant dashboard</p>

			<form onsubmit={(e) => { e.preventDefault(); handleLogin(); }} class="space-y-5">
				{#if error}
					<div class="flex items-center gap-2 px-3 py-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-[13px]">
						<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
						{error}
					</div>
				{/if}

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
						class="w-full px-3.5 py-2.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-[14px] placeholder-surface-500 focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/40 outline-none transition-all"
						placeholder="Enter your password"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="w-full py-2.5 bg-brand-500 hover:bg-brand-400 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-[14px] font-semibold transition-all hover:shadow-lg hover:shadow-brand-500/20"
				>
					{loading ? 'Signing in...' : 'Sign in'}
				</button>
			</form>

			<p class="text-center text-[13px] text-surface-500 mt-6">
				Don't have an account?
				<a href="/auth/register" class="text-brand-400 hover:text-brand-300 font-medium transition-colors">Create one</a>
			</p>
		</div>
	</div>
</div>
