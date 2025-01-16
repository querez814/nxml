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
		fetchLosers: () => Promise<MoversData[]>;
	}

	let props = $props();
	let { fetchLosers } = props satisfies Props;

	let error: string | null = null;

	const losersPromise = $state(async () => {
		try {
			return await fetchLosers();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to fetch losers';
			return [];
		}
	});

	const losers = $derived(losersPromise());
</script>

<Card.Root class="border-0 bg-black/40 backdrop-blur-xl">
	<Card.Header class="pb-2">
		<Card.Title class="text-lg tracking-tight">Top Losers</Card.Title>
	</Card.Header>
	<Card.Content>
		{#await losers}
			<div class="p-4 text-center text-gray-400">Loading losers data...</div>
		{:then data}
			<div class="space-y-4">
				{#each data.slice(0, 5) as loser, i}
					<div class="group relative" in:fly={{ y: 20, delay: i * 100 }}>
						<div
							class="flex items-center justify-between gap-4 rounded-lg bg-black/20 p-4 transition-all hover:bg-black/40"
						>
							<div class="space-y-1">
								<div class="font-medium text-red-400">
									{loser.ticker}
								</div>
								<div class="text-sm text-gray-400">
									${loser.price}
								</div>
							</div>
							<div class="text-right">
								<div class="text-red-400">
									{loser.change}%
								</div>
								<div class="text-sm text-gray-400">
									Vol: {loser.volume}
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
