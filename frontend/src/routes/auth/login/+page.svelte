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

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
	<div class="w-full max-w-md">
		<div class="text-center mb-8">
			<a href="/" class="text-2xl font-bold">
				<span class="text-purple-600">Pay</span>Chains
			</a>
			<p class="text-gray-500 mt-2">Sign in to your merchant dashboard</p>
		</div>

		<form
			onsubmit={(e) => { e.preventDefault(); handleLogin(); }}
			class="bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-200 dark:border-gray-800 p-8 space-y-6"
		>
			{#if error}
				<div class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
					{error}
				</div>
			{/if}

			<div>
				<label for="email" class="block text-sm font-medium mb-1.5">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
					placeholder="you@company.com"
				/>
			</div>

			<div>
				<label for="password" class="block text-sm font-medium mb-1.5">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
					placeholder="••••••••"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-400 text-white rounded-lg font-medium transition"
			>
				{loading ? 'Signing in...' : 'Sign In'}
			</button>

			<p class="text-center text-sm text-gray-500">
				Don't have an account?
				<a href="/auth/register" class="text-purple-600 hover:text-purple-500 font-medium">Create one</a>
			</p>
		</form>
	</div>
</div>
