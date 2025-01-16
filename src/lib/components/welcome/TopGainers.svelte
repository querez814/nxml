<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { fade, fly } from 'svelte/transition';

	interface MoversData {
		ticker: string;
		price: string;
		change: string;
		volume: string;
	}

	interface Props {
		fetchGainers: () => Promise<MoversData[]>;
	}

	let props = $props();
	let { fetchGainers } = props satisfies Props;

	let error: string | null = null;

	const gainersPromise = $state(async () => {
		try {
			return await fetchGainers();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to fetch gainers';
			return [];
		}
	});

	const gainers = $derived(gainersPromise());
</script>

<Card.Root class="border-0 bg-black/40 backdrop-blur-xl">
	<Card.Header class="pb-2">
		<Card.Title class="text-lg tracking-tight">Top Gainers</Card.Title>
	</Card.Header>
	<Card.Content>
		{#await gainers}
			<div class="p-4 text-center text-gray-400">Loading gainers data...</div>
		{:then data}
			<div class="space-y-4">
				{#each data.slice(0, 5) as gainer, i}
					<div class="group relative" in:fly={{ y: 20, delay: i * 100 }}>
						<div
							class="flex items-center justify-between gap-4 rounded-lg bg-black/20 p-4 transition-all hover:bg-black/40"
						>
							<div class="space-y-1">
								<div class="font-medium text-green-400">
									{gainer.ticker}
								</div>
								<div class="text-sm text-gray-400">
									${gainer.price}
								</div>
							</div>
							<div class="text-right">
								<div class="text-green-400">
									{gainer.change}%
								</div>
								<div class="text-sm text-gray-400">
									Vol: {gainer.volume}
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{:catch error}
			<div class="p-4 text-center text-red-400">
				{error}
			</div>
		{/await}
	</Card.Content>
</Card.Root>
