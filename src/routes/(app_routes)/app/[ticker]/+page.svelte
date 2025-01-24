<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import * as Card from '$lib/components/ui/card';
	import { Progress } from '$lib/components/ui/progress/index';
	import { Badge } from '$lib/components/ui/badge';
	let { data }: { data: PageData } = $props();
	let coverage = data.analystCoverage || [];
	let ticker = data.ticker.toLocaleUpperCase();
	let newsReports = data.news?.slice(0, 10) || [];
	let valuation = data.valuation;

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

	const getSentimentColor = $derived(() => {
		if (sentimentScore > 66) return 'bg-green-500';
		if (sentimentScore > 33) return 'bg-green-400';
		if (sentimentScore > 0) return 'bg-green-300';
		if (sentimentScore > -33) return 'bg-red-300';
		if (sentimentScore > -66) return 'bg-red-400';
		return 'bg-red-500';
	});

	function formatDate(dateString: string): string {
		// Handle "Invalid Date" case
		if (dateString === 'Invalid Date') {
			return 'Not Available';
		}

		try {
			const date = new Date(dateString);

			// Check if the date is valid
			if (isNaN(date.getTime())) {
				return 'Not Available';
			}

			return date.toLocaleDateString('en-US', {
				month: 'short',
				day: 'numeric',
				year: 'numeric'
			});
		} catch (error) {
			return 'Not Available';
		}
	}
</script>

{#if valuation}
	<div class="min-h-screen bg-[#0a0b0d] p-4">
		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
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

						<!-- News Section -->
						<div class="space-y-6">
							<div class="font-mono text-xs text-gray-500">LATEST NEWS</div>
							{#each newsReports as news}
								<div class="group border-b border-gray-800 pb-4 last:border-b-0">
									<div class="flex items-start gap-4">
										<div class="w-24 flex-shrink-0">
											<img
												src={news.image_url}
												alt={news.title}
												class="h-24 w-24 rounded-md object-cover"
											/>
										</div>

										<div class="flex-1 space-y-2">
											<div class="flex items-start justify-between">
												<div class="font-mono text-sm font-medium text-gray-300">
													{news.title}
												</div>
												<div class="ml-4 whitespace-nowrap font-mono text-xs text-gray-600">
													{formatDate(news.date)}
												</div>
											</div>

											<details class="group cursor-pointer">
												<summary class="list-none">
													<div class="line-clamp-2 font-mono text-xs text-gray-500"></div>
													<span class="mt-1 text-xs text-blue-400 group-open:hidden"
														>Read summary...</span
													>
												</summary>
												<div class="mt-2 font-mono text-xs text-gray-500">
													{news.text}
												</div>
											</details>

											<div class="flex items-center gap-3">
												<Badge variant="outline">
													<div class="font-mono text-xs text-slate-300">{news.sentiment}</div>
												</Badge>
												<div class="flex flex-wrap gap-2">
													{#each news.tickers as ticker}
														<span class="font-mono text-xs text-slate-500">${ticker}</span>
													{/each}
												</div>
											</div>

											<a
												href={news.news_url}
												target="_blank"
												rel="noopener noreferrer"
												class="inline-block text-xs text-blue-500 hover:underline"
											>
												Read full article →
											</a>
										</div>
									</div>
								</div>
							{/each}
						</div>
					</div>
				</Card.Root>
			</div>

			<!-- Analyst Ratings Column -->
			<div class="col-span-1">
				<Card.Root class="border-none bg-[#111215]">
					<div class="p-6">
						<div class="mb-6 font-mono text-xl text-green-400">LATEST ANALYST RATINGS</div>
						<div class="space-y-4">
							{#each coverage as rate}
								<Card.Root class="bg-[#1a1b1e]">
									<div class="p-4">
										<div class="mb-3 flex items-center justify-between">
											<p class="font-mono text-sm font-medium text-slate-300">
												{rate['Analyst Firm']}
											</p>
											<div class="font-mono text-xs text-gray-500">
												{rate['Date']}
											</div>
										</div>
										<p class="mb-3 font-mono text-sm text-slate-300">{rate.Type}</p>
										<div class="grid grid-cols-2 gap-3">
											<div>
												<div class="font-mono text-xs text-gray-500">Current Rating</div>
												<div class="font-mono text-sm text-slate-300">{rate['Current Rating']}</div>
											</div>
											<div>
												<div class="font-mono text-xs text-gray-500">Previous Rating</div>
												<div class="font-mono text-sm text-slate-300">
													{rate['Previous Rating']}
												</div>
											</div>
											<div>
												<div class="font-mono text-xs text-gray-500">Current Target</div>
												<div class="font-mono text-sm text-slate-300">
													{rate['Current Price Target']}
												</div>
											</div>
											<div>
												<div class="font-mono text-xs text-gray-500">Previous Target</div>
												<div class="font-mono text-sm text-slate-300">
													{rate['Previous Price Target']}
												</div>
											</div>
										</div>
									</div>
								</Card.Root>
							{/each}
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
