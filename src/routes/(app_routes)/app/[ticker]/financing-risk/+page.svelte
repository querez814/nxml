<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		const t = $page.params.ticker;
		if (t) goto(`/app/${t}/financing-risk/analysis`, { replaceState: true });
	});
</script>

<p class="text-sm text-gray-500">Redirecting to Financing Risk Analysis...</p>
