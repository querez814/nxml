<!-- Screener.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Badge } from '$lib/components/ui/badge';
	import { SlidersHorizontal, ArrowUpDown, Building2 } from 'lucide-svelte';
	const api_url = import.meta.env.VITE_API_URL;

	interface Stock {
		symbol: string;
		company_name: string;
		market_cap: number;
		stock_price: number;
		percent_change: string;
		industry: string;
		volume: number;
		pe_ratio: number | null;
		ent_value: number | null;
		mc_group: string;
		sector: string;
		change_1w: string | null;
		change_1m: string | null;
		change_3m: string | null;
		change_6m: string | null;
		change_ytd: string | null;
		change_1y: string | null;
		change_5y: string | null;
		source_file: string;
		loaded_at: string;
	}

	interface SectorGroup {
		[key: string]: Stock[];
	}

	let stocks = $state<Stock[]>([]);
	let sectors = $state<string[]>([]);
	let loading = $state(false);
	let error = $state<string | null>(null);
	let stocksByIndustry = $state<SectorGroup>({});

	let filters = $state({
		minMarketCap: null as number | null,
		maxPeRatio: null as number | null,
		selectedSectors: [] as string[],
		minChange1m: null as number | null,
		maxChange1m: null as number | null
	});

	function formatMarketCap(marketCap: number): string {
		if (!marketCap) return '-';
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			notation: 'compact',
			maximumFractionDigits: 1
		}).format(marketCap);
	}

	function formatVolume(volume: number): string {
		return new Intl.NumberFormat('en-US', {
			notation: 'compact',
			maximumFractionDigits: 1
		}).format(volume);
	}

	function getChangeColor(change: string | null): string {
		if (!change) return '';
		return change.startsWith('-') ? 'text-red-400' : 'text-green-400';
	}

	onMount(async () => {
		try {
			loading = true;
			const response = await fetch(`${api_url}/screen/stocks/screen`);
			const data: Stock[] = await response.json();

			// Group stocks by sector
			stocksByIndustry = data.reduce((acc, stock) => {
				if (!acc[stock.industry]) {
					acc[stock.industry] = [];
				}
				acc[stock.industry].push(stock);
				return acc;
			}, {} as SectorGroup);

			// Extract unique sectors
			sectors = [...new Set(data.map((stock) => stock.sector))];
			stocks = data;
		} catch (err) {
			console.error('Error fetching stocks:', err);
			error = 'Failed to load sectors';
		} finally {
			loading = false;
		}
	});

	async function screenStocks() {
		try {
			loading = true;
			error = null;

			const params = new URLSearchParams();
			if (filters.minMarketCap) params.append('min_market_cap', filters.minMarketCap.toString());
			if (filters.maxPeRatio) params.append('max_pe_ratio', filters.maxPeRatio.toString());
			if (filters.selectedSectors.length) {
				filters.selectedSectors.forEach((sector) => params.append('sectors', sector));
			}
			if (filters.minChange1m) params.append('min_change_1m', filters.minChange1m.toString());
			if (filters.maxChange1m) params.append('max_change_1m', filters.maxChange1m.toString());

			const response = await fetch(`${api_url}/screen/stocks/screen?${params}`);
			const data: Stock[] = await response.json();

			// Update grouped data
			stocksByIndustry = data.reduce((acc, stock) => {
				if (!acc[stock.industry]) {
					acc[stock.industry] = [];
				}
				acc[stock.industry].push(stock);
				return acc;
			}, {} as SectorGroup);

			stocks = data;
		} catch (err) {
			console.error('Error screening stocks:', err);
			error = 'Failed to screen stocks';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-b from-background to-muted">
	<div class="container mx-auto px-4 py-8">
		<div class="mb-8">
			<h1
				class="bg-gradient-to-r from-primary to-primary/50 bg-clip-text text-3xl font-bold tracking-tighter text-transparent"
			>
				Stock Screener
			</h1>
			<p class="mt-2 text-muted-foreground">Filter and analyze stocks based on key metrics</p>
		</div>

		<Card.Root class="border-2 bg-background/95 backdrop-blur">
			<Card.Header>
				<Card.Title class="flex items-center gap-2">
					<SlidersHorizontal class="h-5 w-5" />
					Screening Filters
				</Card.Title>
				<Card.Description>Adjust parameters to find matching stocks</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
					<!-- Market Cap Filter -->
					<div class="space-y-2">
						<label for="marketCap" class="text-sm font-medium"> Minimum Market Cap ($) </label>
						<Input
							id="marketCap"
							type="number"
							bind:value={filters.minMarketCap}
							onchange={() => screenStocks()}
							placeholder="e.g. 1000000000"
						/>
					</div>

					<!-- P/E Ratio Filter -->
					<div class="space-y-2">
						<label for="peRatio" class="text-sm font-medium"> Maximum P/E Ratio </label>
						<Input
							id="peRatio"
							type="number"
							bind:value={filters.maxPeRatio}
							onchange={() => screenStocks()}
							placeholder="e.g. 30"
						/>
					</div>

					<!-- Monthly Change Filters -->
					<div class="space-y-2">
						<label class="text-sm font-medium"> 1 Month Change Range (%) </label>
						<div class="grid grid-cols-2 gap-2">
							<Input
								id="changeMin"
								type="number"
								bind:value={filters.minChange1m}
								onchange={() => screenStocks()}
								placeholder="Min %"
							/>
							<Input
								id="changeMax"
								type="number"
								bind:value={filters.maxChange1m}
								onchange={() => screenStocks()}
								placeholder="Max %"
								aria-label="Maximum 1 Month Change Percentage"
							/>
						</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<!-- Results -->
		{#if loading}
			<div class="mt-8 flex items-center justify-center py-8">
				<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-primary"></div>
			</div>
		{:else if error}
			<div
				class="mt-8 rounded border border-destructive/50 bg-destructive/10 px-4 py-3 text-destructive"
				role="alert"
			>
				{error}
			</div>
		{:else}
			{#each Object.entries(stocksByIndustry) as [industry, industryStocks]}
				<Card.Root class="mt-6 border-2 bg-background/95 backdrop-blur">
					<Card.Header>
						<Card.Title class="flex items-center gap-2">
							<Building2 class="h-5 w-5" />
							{industry}
						</Card.Title>
						<Card.Description>
							{industryStocks.length} stocks | Average Market Cap: {formatMarketCap(
								industryStocks.reduce((sum, stock) => sum + stock.market_cap, 0) /
									industryStocks.length
							)}
						</Card.Description>
					</Card.Header>
					<Card.Content>
						<div class="overflow-x-auto">
							<table class="w-full">
								<thead>
									<tr class="border-b border-border">
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>Symbol</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>Company</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>Market Cap</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>Price</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>Volume</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>P/E</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground">1M</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground">3M</th
										>
										<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground"
											>YTD</th
										>
									</tr>
								</thead>
								<tbody class="divide-y divide-border">
									{#each industryStocks as stock}
										<tr class="group transition-colors hover:bg-muted/50">
											<td class="whitespace-nowrap px-4 py-3">
												<div class="flex items-center gap-2">
													<span class="font-medium">{stock.symbol}</span>
													<Badge variant="outline" class="text-xs">{stock.mc_group}</Badge>
												</div>
											</td>
											<td class="whitespace-nowrap px-4 py-3">{stock.company_name}</td>
											<td class="whitespace-nowrap px-4 py-3"
												>{formatMarketCap(stock.market_cap)}</td
											>
											<td class="whitespace-nowrap px-4 py-3">${stock.stock_price}</td>
											<td class="whitespace-nowrap px-4 py-3">{formatVolume(stock.volume)}</td>
											<td class="whitespace-nowrap px-4 py-3"
												>{stock.pe_ratio?.toFixed(1) ?? '-'}</td
											>
											<td class="whitespace-nowrap px-4 py-3">
												<span class={getChangeColor(stock.change_1m)}>{stock.change_1m ?? '-'}</span
												>
											</td>
											<td class="whitespace-nowrap px-4 py-3">
												<span class={getChangeColor(stock.change_3m)}>{stock.change_3m ?? '-'}</span
												>
											</td>
											<td class="whitespace-nowrap px-4 py-3">
												<span class={getChangeColor(stock.change_ytd)}
													>{stock.change_ytd ?? '-'}</span
												>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</Card.Content>
				</Card.Root>
			{/each}
		{/if}
	</div>
</div>
