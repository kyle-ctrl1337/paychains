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

	async function handleRegister() {
		error = '';
		loading = true;
		try {
			const result: any = await api.register({
				email,
				password,
				company_name: companyName || undefined
			});

			// Store the API keys to show them once
			apiKeys = { live: result.api_key_live, test: result.api_key_test };

			// Login to get JWT
			const loginResult = await api.login({ email, password });
			setAuth(loginResult.access_token, loginResult.merchant, result.api_key_live, result.api_key_test);
		} catch (e: any) {
			error = e.message || 'Registration failed';
		} finally {
			loading = false;
		}
	}

	function goToDashboard() {
		goto('/dashboard');
	}
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 px-4">
	<div class="w-full max-w-md">
		<div class="text-center mb-8">
			<a href="/" class="text-2xl font-bold">
				<span class="text-purple-600">Pay</span>Chains
			</a>
			<p class="text-gray-500 mt-2">Create your merchant account</p>
		</div>

		{#if apiKeys}
			<!-- Show API Keys (one time only) -->
			<div class="bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-200 dark:border-gray-800 p-8 space-y-6">
				<div class="text-center">
					<div class="text-4xl mb-3">&#127881;</div>
					<h2 class="text-xl font-bold">Account Created!</h2>
					<p class="text-sm text-gray-500 mt-1">Save your API keys — they won't be shown again.</p>
				</div>

				<div class="space-y-4">
					<div>
						<label class="block text-xs font-medium text-gray-500 mb-1">Live API Key</label>
						<div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg font-mono text-xs break-all select-all">
							{apiKeys.live}
						</div>
					</div>
					<div>
						<label class="block text-xs font-medium text-gray-500 mb-1">Test API Key</label>
						<div class="p-3 bg-gray-100 dark:bg-gray-800 rounded-lg font-mono text-xs break-all select-all">
							{apiKeys.test}
						</div>
					</div>
				</div>

				<button
					onclick={goToDashboard}
					class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg font-medium transition"
				>
					Go to Dashboard
				</button>
			</div>
		{:else}
			<form
				onsubmit={(e) => { e.preventDefault(); handleRegister(); }}
				class="bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-gray-200 dark:border-gray-800 p-8 space-y-6"
			>
				{#if error}
					<div class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
						{error}
					</div>
				{/if}

				<div>
					<label for="company" class="block text-sm font-medium mb-1.5">Company Name</label>
					<input
						id="company"
						type="text"
						bind:value={companyName}
						class="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
						placeholder="Acme Inc. (optional)"
					/>
				</div>

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
						minlength="8"
						class="w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition"
						placeholder="Min 8 characters"
					/>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-400 text-white rounded-lg font-medium transition"
				>
					{loading ? 'Creating account...' : 'Create Account'}
				</button>

				<p class="text-center text-sm text-gray-500">
					Already have an account?
					<a href="/auth/login" class="text-purple-600 hover:text-purple-500 font-medium">Sign in</a>
				</p>
			</form>
		{/if}
	</div>
</div>
