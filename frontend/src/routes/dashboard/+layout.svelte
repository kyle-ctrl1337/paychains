<script lang="ts">
	import { auth, clearAuth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let { children } = $props();
	let merchant = $state<any>(null);
	let currentPath = $state('');

	const navItems = [
		{ href: '/dashboard', label: 'Overview', icon: '&#9632;' },
		{ href: '/dashboard/payments', label: 'Payments', icon: '&#8594;' },
		{ href: '/dashboard/subscriptions', label: 'Subscriptions', icon: '&#8634;' },
		{ href: '/dashboard/payment-links', label: 'Payment Links', icon: '&#128279;' },
		{ href: '/dashboard/payouts', label: 'Payouts', icon: '&#128181;' },
		{ href: '/dashboard/settings', label: 'Settings', icon: '&#9881;' }
	];

	onMount(() => {
		const unsub = auth.subscribe((state) => {
			if (!state.token) {
				goto('/auth/login');
				return;
			}
			merchant = state.merchant;
		});

		const pageUnsub = page.subscribe((p) => {
			currentPath = p.url.pathname;
		});

		return () => {
			unsub();
			pageUnsub();
		};
	});

	function handleLogout() {
		clearAuth();
		goto('/auth/login');
	}
</script>

<div class="min-h-screen flex bg-gray-50 dark:bg-gray-950">
	<!-- Sidebar -->
	<aside class="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
		<div class="p-6 border-b border-gray-200 dark:border-gray-800">
			<a href="/dashboard" class="text-xl font-bold">
				<span class="text-purple-600">Pay</span>Chains
			</a>
			{#if merchant}
				<p class="text-xs text-gray-500 mt-1 truncate">{merchant.company_name || merchant.email}</p>
			{/if}
		</div>

		<nav class="flex-1 p-4 space-y-1">
			{#each navItems as item}
				<a
					href={item.href}
					class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition
						{currentPath === item.href
							? 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300'
							: 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'}"
				>
					<span class="text-base">{@html item.icon}</span>
					{item.label}
				</a>
			{/each}
		</nav>

		<div class="p-4 border-t border-gray-200 dark:border-gray-800">
			<div class="flex items-center justify-between px-3 py-2">
				<span class="text-xs font-medium text-gray-500 uppercase">{merchant?.plan || 'free'} plan</span>
				<button
					onclick={handleLogout}
					class="text-xs text-gray-500 hover:text-red-500 font-medium transition"
				>
					Log Out
				</button>
			</div>
		</div>
	</aside>

	<!-- Main Content -->
	<main class="flex-1 p-8 overflow-auto">
		{@render children()}
	</main>
</div>
