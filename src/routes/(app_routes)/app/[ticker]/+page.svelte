<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { fade, fly } from 'svelte/transition';
	import type { PageData } from './$types';

	let { data } = $props<{ data: PageData }>();

	const ticker = $derived(data.newsData?.ticker);
	const analystTargetPrice = $derived(data.newsData?.ttm_display?.AnalystTargetPrice);
	const metrics = $derived([
		{ label: 'EV/Sales', value: data.newsData?.ttm_display?.evtosales.toFixed(2), trend: 'up' },
		{
			label: 'EV/EBITDA',
			value: data.newsData?.ttm_display?.evtoebitda.toFixed(2),
			trend: 'neutral'
		},
		{
			label: 'EV/Income',
			value: data.newsData?.ttm_display?.evtonetincome.toFixed(2),
			trend: 'up'
		},
		{ label: 'Latest Close', value: data.newsData?.latest_price?.close.toFixed(2), trend: 'down' }
	]);
	const sentimentData = $derived({
		positive: data.newsData?.summary?.sentiment_distribution?.positive || 0,
		neutral: data.newsData?.summary?.sentiment_distribution?.neutral || 0,
		negative: data.newsData?.summary?.sentiment_distribution?.negative || 0,
		total:
			(data.newsData?.summary?.sentiment_distribution?.positive || 0) +
			(data.newsData?.summary?.sentiment_distribution?.neutral || 0) +
			(data.newsData?.summary?.sentiment_distribution?.negative || 0)
	});
	const getPercentage = (value: number) => ((value / sentimentData.total) * 100).toFixed(1);
</script>

<div
	class="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black px-4 py-6 font-mono text-gray-100 md:px-8"
>
	<div class="relative mx-auto max-w-7xl">
		<div class="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
			<div
				class="relative left-[calc(50%-20rem)] aspect-[1155/678] w-[72.1875rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-green-500 to-green-900 opacity-20 sm:left-[calc(50%-30rem)]"
			/>
		</div>

		<header class="mb-12 space-y-1">
			<div class="flex items-baseline justify-between">
				<h1 class="text-5xl font-bold tracking-tight text-green-400 md:text-6xl xl:text-7xl">
					{ticker}
				</h1>
				<div class="text-right">
					<div class="text-xs uppercase tracking-widest text-gray-500">Target Price</div>
					<div class="text-2xl font-bold text-green-400">${analystTargetPrice}</div>
				</div>
			</div>
		</header>
		<div class="grid gap-6"></div>
		<div class="grid gap-6">
			<Card.Root class="border-0 bg-black/40 backdrop-blur-xl">
				<Card.Content class="p-6">
					<div class="grid grid-cols-2 gap-8 md:grid-cols-4">
						{#each metrics as { label, value, trend }}
							<div class="relative overflow-hidden rounded-lg bg-black/20 p-4" in:fade>
								<div class="space-y-2">
									<div class="text-xs uppercase tracking-widest text-gray-500">{label}</div>
									<div class="flex items-baseline gap-2">
										<div class="text-2xl font-bold tracking-tight text-green-400">{value}</div>
										<div
											class="text-xs {trend === 'up'
												? 'text-green-500'
												: trend === 'down'
													? 'text-red-500'
													: 'text-gray-500'}"
										>
											{trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'}
										</div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</Card.Content>
			</Card.Root>

			<div class="grid gap-6 lg:grid-cols-2">
				<Card.Root class="border-0 bg-black/40 backdrop-blur-xl">
					<Card.Header class="pb-2">
						<div class="flex items-baseline justify-between">
							<Card.Title class="text-lg tracking-tight">Market Sentiment</Card.Title>
							<div class="text-2xl font-bold tracking-tight text-green-400">
								{data.newsData?.market_sentiment?.score.toFixed(2)}
							</div>
						</div>
					</Card.Header>
					<Card.Content class="space-y-6">
						<div>
							<div class="mb-2 flex items-baseline justify-between">
								<div class="text-xl font-bold text-green-400">
									{data.newsData?.market_sentiment?.overall}
								</div>
								<div class="text-xs uppercase tracking-widest text-gray-500">
									{data.newsData?.market_sentiment?.confidence}
								</div>
							</div>
							<div class="h-2 overflow-hidden rounded-full bg-black/40">
								<div class="relative h-full w-full">
									<div
										class="absolute h-full bg-green-500/80"
										style="width: {getPercentage(sentimentData.positive)}%"
									/>
									<div
										class="absolute h-full bg-gray-500/80"
										style="left: {getPercentage(sentimentData.positive)}%; width: {getPercentage(
											sentimentData.neutral
										)}%"
									/>
									<div
										class="absolute h-full bg-red-500/80"
										style="left: {parseFloat(getPercentage(sentimentData.positive)) +
											parseFloat(getPercentage(sentimentData.neutral))}%; width: {getPercentage(
											sentimentData.negative
										)}%"
									/>
								</div>
							</div>
							<div class="mt-2 flex justify-between text-xs tracking-wider">
								<div class="text-green-400">+{sentimentData.positive}</div>
								<div class="text-gray-400">{sentimentData.neutral}</div>
								<div class="text-red-400">-{sentimentData.negative}</div>
							</div>
						</div>
					</Card.Content>
				</Card.Root>

				<Card.Root class="border-0 bg-black/40 backdrop-blur-xl">
					<Card.Header class="pb-2">
						<Card.Title class="text-lg tracking-tight">Latest News</Card.Title>
					</Card.Header>
					<Card.Content>
						<div class="space-y-4">
							{#each data.newsData?.top_articles || [] as article, i}
								<div class="group relative" in:fly={{ y: 20, delay: i * 100 }}>
									<div
										class="flex items-start justify-between gap-4 rounded-lg bg-black/20 p-4 transition-all hover:bg-black/40"
									>
										<div class="space-y-2">
											<a href={article.url} class="block" target="_blank" rel="noopener noreferrer">
												<h3
													class="line-clamp-2 font-medium text-green-400 transition-colors group-hover:text-green-300"
												>
													{article.title}
												</h3>
											</a>
											<p class="line-clamp-2 text-sm text-gray-400">{article.summary}</p>
											<div class="flex items-center justify-between text-xs text-gray-500">
												<span>{article.source}</span>
												<time>{article.published_at}</time>
											</div>
										</div>
										<div class="shrink-0">
											<span
												class="rounded-full px-2 py-1 text-xs tracking-wider {article.sentiment_label?.includes(
													'Bullish'
												)
													? 'bg-green-500/20 text-green-400'
													: article.sentiment_label?.includes('Bearish')
														? 'bg-red-500/20 text-red-400'
														: 'bg-gray-500/20 text-gray-400'}"
											>
												{article.sentiment_label}
											</span>
										</div>
									</div>
								</div>
							{/each}
						</div>
					</Card.Content>
				</Card.Root>
			</div>
		</div>
	</div>
</div>
