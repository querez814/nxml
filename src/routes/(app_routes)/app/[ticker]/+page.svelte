<script lang="ts">
	import type { PageData } from './$types';
	import * as Card from '$lib/components/ui/card';
	import { Progress } from '$lib/components/ui/progress/index';
	let { data }: { data: PageData } = $props();
	const ticker = $derived(data.ticker?.toLocaleUpperCase() ?? '');
	const valuation = $derived(data.valuation);

	const sentimentScore = $derived(
		valuation
			? ((valuation.AnalystRatingStrongBuy * 2 +
					valuation.AnalystRatingBuy -
					(valuation.AnalystRatingSell * 2 + valuation.AnalystRatingStrongSell)) /
					(valuation.AnalystRatingStrongBuy +
						valuation.AnalystRatingBuy +
						valuation.AnalystRatingHold +
						valuation.AnalystRatingSell +
						valuation.AnalystRatingStrongSell)) *
					100
			: 0
	);

	const getSentimentColor = $derived.by(() => {
		if (sentimentScore > 66) return 'bg-green-500';
		if (sentimentScore > 33) return 'bg-green-400';
		if (sentimentScore > 0) return 'bg-green-300';
		if (sentimentScore > -33) return 'bg-red-300';
		if (sentimentScore > -66) return 'bg-red-400';
		return 'bg-red-500';
	});

</script>

{#if valuation}
	<div class="min-h-screen bg-[#0a0b0d] p-4">
		<div class="grid grid-cols-1 gap-4">
			<div class="col-span-1">
				<Card.Root class="border-none bg-[#111215]">
					<div class="p-6">
						<!-- Header -->
						<div class="mb-8 grid grid-cols-2">
							<div class="font-mono text-5xl font-bold text-green-400">{ticker}</div>
							<div class="text-right">
								<div class="font-mono text-xs text-gray-500">TARGET PRICE</div>
								<div class="font-mono text-2xl text-green-400">
									${valuation.AnalystTargetPrice.toFixed(2)}
								</div>
							</div>
						</div>

						<!-- Metrics Grid -->
						<div class="mb-8 grid grid-cols-4 gap-8">
							<div>
								<div class="font-mono text-xs text-gray-500">EV/SALES</div>
								<div class="font-mono text-xl text-green-400">
									{valuation.evtosales.toFixed(2)}x
								</div>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">EV/EBITDA</div>
								<div class="font-mono text-xl text-green-400">
									{valuation.evtoebitda.toFixed(2)}x
								</div>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">EV/INCOME</div>
								<div class="font-mono text-xl text-green-400">
									{valuation.evtonetincome.toFixed(2)}x
								</div>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">SENTIMENT</div>
								<div class="relative mt-2">
									<div class="h-5 w-full bg-gray-800 text-base">
										<h1 class="mb-2"><Progress value={sentimentScore} /></h1>
									</div>
									<div
										class="mt-1 font-mono text-xs {sentimentScore >= 0
											? 'text-green-400'
											: 'text-red-400'}"
									>
										{sentimentScore.toFixed(2)}
									</div>
								</div>
							</div>
						</div>

					</div>
				</Card.Root>
			</div>
		</div>
	</div>
{:else}
	<div class="flex h-full items-center justify-center">
		<p class="text-gray-500">No data available for {ticker}</p>
	</div>
{/if}

<style>
	:global(body) {
		background-color: #0a0b0d;
		color: #ffffff;
	}
</style>
