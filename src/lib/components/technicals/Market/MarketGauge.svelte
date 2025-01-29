<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import type { MarketMomentum } from '$lib/types/types';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { TrendingUp, TrendingDown, Minus } from 'lucide-svelte';

	let marketData: MarketMomentum | null = null;
	let error: string | null = null;
	let loading = true;

	onMount(async () => {
		try {
			const response = await fetch(`${api_url}/technicals/marketmomentum`);
			marketData = await response.json();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to fetch market data';
		} finally {
			loading = false;
		}
	});

	function getConditionIcon(condition: string) {
		if (condition.includes('UPTREND')) return TrendingUp;
		if (condition.includes('DOWNTREND')) return TrendingDown;
		return Minus;
	}

	function getScoreColor(score: number): string {
		if (score > 50) return 'text-green-400';
		if (score < -50) return 'text-red-400';
		return 'text-blue-400';
	}
</script>

{#if loading}
	<div class="flex h-32 items-center justify-center">
		<div
			class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"
		></div>
	</div>
{:else if error}
	<div class="text-center text-red-400">{error}</div>
{:else if marketData}
	<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
		{#each Object.entries(marketData) as [symbol, data]}
			{@const Icon = getConditionIcon(data.market_condition)}
			<div
				class="group relative overflow-hidden rounded-lg border border-border/50 bg-card p-4 transition-all duration-300 hover:border-primary/50"
			>
				<div class="flex items-center justify-between">
					<h3 class="text-lg font-semibold">{symbol}</h3>
					<Icon class="h-5 w-5 text-primary" />
				</div>

				<div class="mt-2 space-y-2">
					<p class="flex items-center justify-between">
						<span class="text-sm text-muted-foreground">Momentum Score:</span>
						<span class={getScoreColor(data.momentum_score)}>
							{data.momentum_score.toFixed(1)}
						</span>
					</p>

					<p class="flex items-center justify-between">
						<span class="text-sm text-muted-foreground">Market Condition:</span>
						<span class="text-sm font-medium text-primary">
							{data.market_condition.replace('_', ' ')}
						</span>
					</p>

					<p class="flex items-center justify-between">
						<span class="text-sm text-muted-foreground">Trend Consistency:</span>
						<span class="text-sm">
							{data.trend_analysis.consistency.toFixed(1)}%
						</span>
					</p>
				</div>

				<div
					class="absolute bottom-0 left-0 h-1 w-full bg-gradient-to-r from-transparent via-primary/20 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100"
				></div>
			</div>
		{/each}
	</div>
{/if}
