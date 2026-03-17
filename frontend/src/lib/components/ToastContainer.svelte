<script lang="ts">
	import { toast, type Toast, type ToastType } from '$lib/stores/toast';
	import { fly, fade } from 'svelte/transition';

	let toasts: Toast[] = $state([]);

	toast.subscribe((value) => {
		toasts = value;
	});

	const icons: Record<ToastType, string> = {
		success: 'M5 13l4 4L19 7',
		error: 'M6 18L18 6M6 6l12 12',
		warning: 'M12 9v4m0 4h.01M12 3L2 21h20L12 3z',
		info: 'M12 8v4m0 4h.01M12 2a10 10 0 110 20 10 10 0 010-20z'
	};

	const accentColors: Record<ToastType, string> = {
		success: 'text-emerald-400 border-emerald-500/40',
		error: 'text-red-400 border-red-500/40',
		warning: 'text-amber-400 border-amber-500/40',
		info: 'text-blue-400 border-blue-500/40'
	};
</script>

<div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
	{#each toasts as t (t.id)}
		<div
			class="pointer-events-auto flex items-start gap-3 rounded-lg border border-white/[0.06] bg-surface-900 px-4 py-3 shadow-lg min-w-[320px] max-w-[420px] {accentColors[t.type]}"
			in:fly={{ x: 80, duration: 300 }}
			out:fade={{ duration: 200 }}
		>
			<!-- Icon -->
			<svg
				class="mt-0.5 h-5 w-5 flex-shrink-0 {accentColors[t.type].split(' ')[0]}"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
			>
				<path d={icons[t.type]} />
			</svg>

			<!-- Message -->
			<span class="flex-1 text-sm text-white/90">{t.message}</span>

			<!-- Close button -->
			<button
				onclick={() => toast.remove(t.id)}
				class="mt-0.5 flex-shrink-0 text-white/40 hover:text-white/80 transition-colors cursor-pointer"
				aria-label="Close notification"
			>
				<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	{/each}
</div>
