<script>
	import '../app.css';
	import ToastContainer from '$lib/components/ToastContainer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<meta name="color-scheme" content="dark" />
</svelte:head>

{@render children()}
<ToastContainer />
