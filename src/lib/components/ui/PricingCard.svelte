<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Check } from 'lucide-svelte';

	export let tier: {
		name: string;
		price: string;
		frequency: 'month' | 'year' | 'once';
		description: string;
		features: string[];
		cta: string;
		ctaLink: string;
	};
</script>

<div class="flex flex-col rounded-lg bg-white p-6 shadow-lg">
	<h3 class="text-2xl font-bold">{tier.name}</h3>
	<div class="mt-4">
		<span class="text-4xl font-bold">{tier.price}</span>
		{#if tier.frequency !== 'once'}
			<span class="ml-1 text-gray-500">
				/{tier.frequency === 'month' ? 'mo' : 'yr'}
			</span>
		{/if}
	</div>
	<p class="mt-4 text-gray-500">{tier.description}</p>
	<ul class="mt-6 flex-grow space-y-4">
		{#each tier.features as feature}
			<li class="flex items-center">
				<Check class="mr-2 h-5 w-5 text-green-500" />
				<span>{feature}</span>
			</li>
		{/each}
	</ul>
	<a href={tier.ctaLink} target="_blank" rel="noopener noreferrer">
		<Button class="mt-8 w-full">{tier.cta}</Button>
	</a>
</div>
