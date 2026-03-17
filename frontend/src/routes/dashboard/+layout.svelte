<script lang="ts">
	import { auth, clearAuth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Logo from '$lib/components/Logo.svelte';

	let { children } = $props();
	let merchant = $state<any>(null);
	let currentPath = $state('');
	let sidebarOpen = $state(false);

	const baseNavItems = [
		{
			href: '/dashboard',
			label: 'Overview',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		},
		{
			href: '/dashboard/payments',
			label: 'Payments',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		},
		{
			href: '/dashboard/subscriptions',
			label: 'Subscriptions',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		},
		{
			href: '/dashboard/payment-links',
			label: 'Payment Links',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.553-3.554l4.5-4.5a4.5 4.5 0 016.364 6.364l-4.5 4.5a4.5 4.5 0 01-7.244-1.242" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		},
		{
			href: '/dashboard/payouts',
			label: 'Payouts',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		},
		{
			href: '/dashboard/settings',
			label: 'Settings',
			icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
		}
	];

	const adminNavItem = {
		href: '/dashboard/admin',
		label: 'Admin',
		icon: `<svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
	};

	let navItems = $derived(
		merchant?.is_admin ? [...baseNavItems, adminNavItem] : baseNavItems
	);

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

<style>
	.sidebar-overlay {
		animation: fadeIn 200ms ease-out;
	}
	.sidebar-drawer {
		animation: slideIn 250ms cubic-bezier(0.16, 1, 0.3, 1);
	}
	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}
	@keyframes slideIn {
		from { transform: translateX(-100%); }
		to { transform: translateX(0); }
	}
</style>

<div class="min-h-screen flex bg-surface-950">
	<!-- Desktop Sidebar -->
	<aside class="hidden md:flex w-[240px] flex-col border-r border-white/[0.06] bg-surface-950 shrink-0">
		<div class="px-5 h-14 flex items-center border-b border-white/[0.06]">
			<a href="/" class="group">
				<Logo size={24} textClass="text-[14px] group-hover:text-brand-400 transition-colors" />
			</a>
		</div>

		<nav class="flex-1 px-3 py-4 space-y-0.5">
			{#each navItems as item}
				<a
					href={item.href}
					class="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[13px] font-medium transition-colors
						{currentPath === item.href
							? 'bg-white/[0.06] text-white'
							: 'text-surface-400 hover:text-surface-200 hover:bg-white/[0.03]'}"
				>
					<span class="{currentPath === item.href ? 'text-brand-400' : 'text-surface-500'}">{@html item.icon}</span>
					{item.label}
				</a>
			{/each}
		</nav>

		<div class="px-3 py-4 border-t border-white/[0.06]">
			{#if merchant}
				<div class="px-2.5 py-2 mb-2">
					<div class="text-[13px] font-medium text-surface-200 truncate">{merchant.company_name || merchant.email}</div>
					<div class="text-[11px] text-surface-500 capitalize">{merchant.plan} plan</div>
				</div>
			{/if}
			<button
				onclick={handleLogout}
				class="flex items-center gap-2 w-full px-2.5 py-2 rounded-lg text-[13px] text-surface-500 hover:text-red-400 hover:bg-red-500/[0.06] transition-colors"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" stroke-linecap="round" stroke-linejoin="round"/></svg>
				Log out
			</button>
		</div>
	</aside>

	<!-- Mobile header -->
	<div class="md:hidden fixed top-0 left-0 right-0 z-50 bg-surface-950/80 backdrop-blur-xl border-b border-white/[0.06]">
		<div class="flex items-center justify-between px-4 h-14">
			<a href="/">
				<Logo size={24} textClass="text-[14px]" />
			</a>
			<button onclick={() => sidebarOpen = !sidebarOpen} class="w-8 h-8 flex items-center justify-center text-surface-400 hover:text-white transition-colors">
				{#if sidebarOpen}
					<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/></svg>
				{:else}
					<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3.75 6.75h16.5M3.75 12h16.5M12 17.25h8.25" stroke-linecap="round" stroke-linejoin="round"/></svg>
				{/if}
			</button>
		</div>
	</div>

	<!-- Mobile sidebar drawer -->
	{#if sidebarOpen}
		<div class="md:hidden fixed inset-0 z-40">
			<div class="sidebar-overlay absolute inset-0 bg-black/60 backdrop-blur-sm" onclick={() => sidebarOpen = false}></div>
			<aside class="sidebar-drawer absolute top-14 left-0 bottom-0 w-[280px] bg-surface-950 border-r border-white/[0.06] flex flex-col overflow-y-auto shadow-2xl shadow-black/40">
				<nav class="flex-1 px-3 py-4 space-y-0.5">
					{#each navItems as item}
						<a
							href={item.href}
							onclick={() => sidebarOpen = false}
							class="flex items-center gap-2.5 px-2.5 py-2.5 rounded-lg text-[13px] font-medium transition-colors
								{currentPath === item.href
									? 'bg-white/[0.06] text-white'
									: 'text-surface-400 hover:text-surface-200 hover:bg-white/[0.03]'}"
						>
							<span class="{currentPath === item.href ? 'text-brand-400' : 'text-surface-500'}">{@html item.icon}</span>
							{item.label}
						</a>
					{/each}
				</nav>

				<div class="px-3 py-4 border-t border-white/[0.06]">
					{#if merchant}
						<div class="px-2.5 py-2 mb-2">
							<div class="text-[13px] font-medium text-surface-200 truncate">{merchant.company_name || merchant.email}</div>
							<div class="text-[11px] text-surface-500 capitalize">{merchant.plan} plan</div>
						</div>
					{/if}
					<button
						onclick={() => { sidebarOpen = false; handleLogout(); }}
						class="flex items-center gap-2 w-full px-2.5 py-2.5 rounded-lg text-[13px] text-surface-500 hover:text-red-400 hover:bg-red-500/[0.06] transition-colors"
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" stroke-linecap="round" stroke-linejoin="round"/></svg>
						Log out
					</button>
				</div>
			</aside>
		</div>
	{/if}

	<!-- Main Content -->
	<main class="flex-1 min-w-0 overflow-auto">
		<div class="max-w-6xl mx-auto px-6 pt-20 pb-8 md:pt-10 md:pb-10">
			{@render children()}
		</div>
	</main>
</div>
