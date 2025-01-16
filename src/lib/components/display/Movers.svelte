<script lang="ts">
	import { fetchGainers, fetchLosers, fetchMostTraded } from '../../../api/movers/movers';

	interface Mover {
		ticker: string;
		price: string;
		change_amount: string;
		change_percentage: string;
		volume: string;
	}

	let gainers = $state<Mover[]>([]);
	let losers = $state<Mover[]>([]);
	let mostTraded = $state<Mover[]>([]);

	let isLoading = $state(true);
	let error = $state<string | null>(null);

	async function fetchAllData() {
		try {
			isLoading = true;
			error = null;

			const [gainersData, losersData, tradedData] = await Promise.all([
				fetchGainers(),
				fetchLosers(),
				fetchMostTraded()
			]);

			gainers = gainersData;
			losers = losersData;
			mostTraded = tradedData;
		} catch (e) {
			error = e instanceof Error ? e.message : 'An error occurred while fetching data';
			console.error('Error fetching market data:', e);
		} finally {
			isLoading = false;
		}
	}

	fetchAllData();
</script>

{#if isLoading}
	<div class="flex items-center justify-center p-8">
		<p class="text-lg text-gray-600">Loading market data...</p>
	</div>
{:else if error}
	<div class="flex flex-col items-center justify-center p-8 text-center">
		<p class="mb-4 text-red-600">{error}</p>
		<button
			onclick={fetchAllData}
			class="rounded bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600"
		>
			Retry
		</button>
	</div>
{:else}
	<div class="grid grid-cols-1 gap-8 p-4 md:grid-cols-2 lg:grid-cols-3">
		<section class="space-y-4">
			<h2 class="text-xl font-bold text-gray-800">Top Gainers</h2>
			{#each gainers as gainer}
				<div
					class="rounded-lg border border-gray-200 p-4 shadow-sm transition-shadow hover:shadow-md"
				>
					<h3 class="text-lg font-semibold">{gainer.ticker}</h3>
					<p class="text-gray-700">${gainer.price}</p>
					<p class="text-green-500">+{gainer.change_percentage}%</p>
					<p class="text-sm text-gray-600">Vol: {gainer.volume}</p>
				</div>
			{/each}
		</section>

		<section class="space-y-4">
			<h2 class="text-xl font-bold text-gray-800">Top Losers</h2>
			{#each losers as loser}
				<div
					class="rounded-lg border border-gray-200 p-4 shadow-sm transition-shadow hover:shadow-md"
				>
					<h3 class="text-lg font-semibold">{loser.ticker}</h3>
					<p class="text-gray-700">${loser.price}</p>
					<p class="text-red-500">{loser.change_percentage}%</p>
					<p class="text-sm text-gray-600">Vol: {loser.volume}</p>
				</div>
			{/each}
		</section>

		<section class="space-y-4">
			<h2 class="text-xl font-bold text-gray-800">Most Traded</h2>
			{#each mostTraded as stock}
				<div
					class="rounded-lg border border-gray-200 p-4 shadow-sm transition-shadow hover:shadow-md"
				>
					<h3 class="text-lg font-semibold">{stock.ticker}</h3>
					<p class="text-gray-700">${stock.price}</p>
					<p class="text-green-500">
						{stock.change_percentage}
					</p>
					<p class="text-sm text-gray-600">Vol: {stock.volume}</p>
				</div>
			{/each}
		</section>
	</div>
{/if}
