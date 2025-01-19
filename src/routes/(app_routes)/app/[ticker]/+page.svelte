<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import type { PageData } from './$types';
	import { formatDistance } from 'date-fns';

	let { data } = $props<{ data: PageData }>();
	let ticker = data.ticker;

	function formatDate(utcDate: string): string {
		return formatDistance(new Date(utcDate), new Date(), { addSuffix: true });
	}

	function getSentimentColor(sentiment: string): string {
		switch (sentiment.toLowerCase()) {
			case 'positive':
				return 'text-green-600';
			case 'negative':
				return 'text-red-600';
			default:
				return 'text-gray-600';
		}
	}
</script>

<div class="container mx-auto p-4">
	<Card.Root class="mb-6">
		<Card.Header>
			<Card.Title>Market Metrics - {ticker}</Card.Title>
		</Card.Header>
		<Card.Content>
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Analyst Ratings</h3>
					<div class="mt-1 flex gap-2">
						<span class="text-green-600"
							>{valuation.AnalystRatingStrongBuy + valuation.AnalystRatingBuy} Buy</span
						>
						<span class="text-gray-600">{valuation.AnalystRatingHold} Hold</span>
						<span class="text-red-600"
							>{valuation.AnalystRatingSell + valuation.AnalystRatingStrongSell} Sell</span
						>
					</div>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Target Price</h3>
					<p class="text-xl font-bold">${valuation.AnalystTargetPrice.toFixed(2)}</p>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">EV/EBITDA</h3>
					<p class="text-xl font-bold">{valuation.evtoebitda.toFixed(2)}x</p>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">P/E Ratios</h3>
					<div class="flex gap-2">
						<span>TTM: {valuation.TrailingPE.toFixed(2)}</span>
						<span>FWD: {valuation.ForwardPE.toFixed(2)}</span>
					</div>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<div class="grid gap-4">
		{#each news as item}
			<Card.Root class="transition-shadow duration-200 hover:shadow-lg">
				<Card.Content class="p-4">
					<div class="flex flex-col gap-2">
						<div class="flex items-start justify-between">
							<h2 class="flex-1 pr-4 text-lg font-semibold">{item.title}</h2>
							<span class="whitespace-nowrap text-sm text-gray-500">
								{formatDate(item.published_utc)}
							</span>
						</div>

						<p class="line-clamp-2 text-gray-600">{item.description}</p>

						{#if item.insights?.length > 0}
							<div class="mt-1 flex flex-wrap gap-2">
								{#each item.insights as insight}
									{#if insight.ticker === ticker}
										<span class={`text-sm ${getSentimentColor(insight.sentiment)}`}>
											{insight.sentiment.toUpperCase()}
										</span>
									{/if}
								{/each}
							</div>
						{/if}

						{#if item.keywords?.length > 0}
							<div class="mt-1 flex flex-wrap gap-2">
								{#each item.keywords as keyword}
									<span class="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600">
										{keyword}
									</span>
								{/each}
							</div>
						{/if}

						<div class="mt-2 flex items-center justify-between border-t border-gray-100 pt-2">
							<div class="flex items-center gap-2">
								{#if item.publisher.favicon_url}
									<img src={item.publisher.favicon_url} alt={item.publisher.name} class="h-4 w-4" />
								{/if}
								<span class="text-sm text-gray-500">{item.publisher.name}</span>
							</div>

							<a
								href={item.article_url}
								target="_blank"
								rel="noopener noreferrer"
								class="text-sm text-blue-500 hover:underline"
							>
								Read more →
							</a>
						</div>
					</div>
				</Card.Content>
			</Card.Root>
		{:else}
			<Card.Root>
				<Card.Content class="text-center py-8">
					<p class="text-lg text-gray-500">No news available for {ticker}</p>
					<p class="text-sm mt-2 text-gray-400">Check back later for updates</p>
				</Card.Content>
			</Card.Root>
		{/each}
	</div>
</div>
