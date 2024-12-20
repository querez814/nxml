<script lang="ts">
	import { propAccessor } from 'svelte-ux/utils/object';
	import Card from '$lib/components/ui/card/card.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import type { PageData } from '../$types';
	let { valuation_data }: { valuation_data: PageData } = $props();
</script>
