<script lang="ts">
	let { size = 28, showText = true, textClass = '' }: { size?: number; showText?: boolean; textClass?: string } = $props();
</script>

<span class="inline-flex items-center gap-2.5">
	<span
		class="relative flex items-center justify-center rounded-xl"
		style="width: {size}px; height: {size}px; background: linear-gradient(135deg, #7c6aff, #6347ff);"
	>
		<svg
			width={size * 0.6}
			height={size * 0.6}
			viewBox="0 0 24 24"
			fill="none"
			xmlns="http://www.w3.org/2000/svg"
		>
			<!-- Vertical bar of P -->
			<path
				d="M7 4V20"
				stroke="white"
				stroke-width="2.5"
				stroke-linecap="round"
			/>
			<!-- Chain-link loop forming the P bowl -->
			<rect
				x="7"
				y="4"
				width="10.5"
				height="9"
				rx="4.5"
				stroke="white"
				stroke-width="2.5"
				fill="none"
			/>
			<!-- Small chain break detail -->
			<circle cx="17" cy="8.5" r="1" fill="white" opacity="0.6" />
		</svg>
		<span class="absolute inset-0 rounded-xl" style="box-shadow: 0 0 {size * 0.5}px rgba(99, 71, 255, 0.3);"></span>
	</span>
	{#if showText}
		<span class="font-semibold tracking-[-0.02em] {textClass}">
			Pay<span class="text-brand-400">Chains</span>
		</span>
	{/if}
</span>
