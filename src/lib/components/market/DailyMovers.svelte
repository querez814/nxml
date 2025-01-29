<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import * as Card from '$lib/components/ui/card';
	import { onMount } from 'svelte';
	import { TrendingUp, TrendingDown, Plus } from 'lucide-svelte';
	import type { MarketDataResponse, TickerData } from '$lib/types/dailys/movers';

	let rawDailyMovers: MarketDataResponse;
	let parsedDailyMovers: ReturnType<typeof parseMarketData> | null = null;
	let error: string | null = null;
	let loading = true;

	function parseTickerData(data: TickerData) {
		return {
			ticker: data.ticker,
			price: parseFloat(data.price),
			change_amount: parseFloat(data.change_amount),
			change_percentage: parseFloat(data.change_percentage.replace('%', '')),
			volume: parseInt(data.volume, 10)
		};
	}

	function parseMarketData(response: MarketDataResponse) {
		return {
			metadata: response.metadata,
			last_updated: response.last_updated,
			top_gainers: response.top_gainers.map(parseTickerData),
			top_losers: response.top_losers.map(parseTickerData),
			most_actively_traded: response.most_actively_traded.map(parseTickerData)
		};
	}

	function formatVolume(volume: number): string {
		if (volume >= 1_000_000) return `${(volume / 1_000_000).toFixed(1)}M`;
		if (volume >= 1_000) return `${(volume / 1_000).toFixed(1)}K`;
		return volume.toString();
	}

	function formatPercentage(percentage: number): string {
		return `${percentage >= 0 ? '+' : ''}${percentage.toFixed(2)}%`;
	}

	function formatPrice(price: number): string {
		return price.toFixed(2);
	}

	onMount(async () => {
		try {
			const response = await fetch(`${api_url}/current/cgl`);
			if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
			rawDailyMovers = await response.json();
			parsedDailyMovers = parseMarketData(rawDailyMovers);
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to fetch market data';
		} finally {
			loading = false;
		}
	});
</script>

<div class="h-full max-h-[600px] overflow-y-auto">
	{#if loading}
		<div class="flex h-64 items-center justify-center">
			<p>Loading market data...</p>
		</div>
	{:else if error}
		<div class="p-4 text-red-500">
			<p>Error: {error}</p>
		</div>
	{:else if parsedDailyMovers}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			<Card.Root class="bg-black/20">
				<Card.Header class="pb-2">
					<Card.Title class="flex items-center gap-2">
						<TrendingUp class="text-green-500" />
						Top Gainers
					</Card.Title>
				</Card.Header>
				<Card.Content>
					{#each parsedDailyMovers.top_gainers as stock}
						<div class="flex items-center justify-between py-1">
							<span class="font-bold">{stock.ticker}</span>
							<div class="text-right">
								<div>${formatPrice(stock.price)}</div>
								<div class="text-green-500">
									{formatPercentage(stock.change_percentage)}
								</div>
								<div class="text-sm text-gray-500">
									Vol: {formatVolume(stock.volume)}
								</div>
							</div>
						</div>
					{/each}
				</Card.Content>
			</Card.Root>

			<Card.Root class="bg-black/20">
				<Card.Header class="pb-2">
					<Card.Title class="flex items-center gap-2">
						<TrendingDown class="text-red-500" />
						Top Losers
					</Card.Title>
				</Card.Header>
				<Card.Content>
					{#each parsedDailyMovers.top_losers as stock}
						<div class="flex items-center justify-between py-1">
							<span class="font-bold">{stock.ticker}</span>
							<div class="text-right">
								<div>${formatPrice(stock.price)}</div>
								<div class="text-red-500">
									{formatPercentage(stock.change_percentage)}
								</div>
								<div class="text-sm text-gray-500">
									Vol: {formatVolume(stock.volume)}
								</div>
							</div>
						</div>
					{/each}
				</Card.Content>
			</Card.Root>

			<Card.Root class="bg-black/20">
				<Card.Header class="pb-2">
					<Card.Title class="flex items-center gap-2">
						<Plus class="text-blue-500" />
						Most Active
					</Card.Title>
				</Card.Header>
				<Card.Content>
					{#each parsedDailyMovers.most_actively_traded as stock}
						<div class="flex items-center justify-between py-1">
							<span class="font-bold">{stock.ticker}</span>
							<div class="text-right">
								<div>${formatPrice(stock.price)}</div>
								<div class={stock.change_percentage >= 0 ? 'text-green-500' : 'text-red-500'}>
									{formatPercentage(stock.change_percentage)}
								</div>
								<div class="text-sm text-gray-500">
									Vol: {formatVolume(stock.volume)}
								</div>
							</div>
						</div>
					{/each}
				</Card.Content>
			</Card.Root>
		</div>
	{/if}
</div>
