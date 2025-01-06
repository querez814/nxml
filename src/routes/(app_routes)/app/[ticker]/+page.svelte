<script lang="ts">
	import Fwdpe from '$lib/components/tutorial/valuation/FWDPE.svelte';
	import TrailingPe from '$lib/components/tutorial/valuation/TrailingPE.svelte';
	import PSales from '$lib/components/tutorial/valuation/PSales.svelte';
	import ValuationCard from '$lib/components/ui/valuationcard/ValuationCard.svelte';
	import Tutorial from '$lib/components/tutorial/valuation/Tutorial.svelte';
	import EVtoEbitda from '$lib/components/tutorial/valuation/EVtoEbitda.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Card from '$lib/components/ui/card';
	import { ChartBar, TrendingUp, DollarSign, Calculator, LineChart } from 'lucide-svelte';

	type FinancialData = {
		symbol: string;
		AnalystTargetPrice: number;
		AnalystRatingStrongBuy: number;
		AnalystRatingBuy: number;
		AnalystRatingHold: number;
		AnalystRatingSell: number;
		AnalystRatingStrongSell: number;
		evtosales: number;
		evtoebitda: number;
		revenue_per_share_ttm: number;
		price_to_sales_ratio_ttm: number;
		TrailingPE: number;
		ForwardPE: number;
	};

	let mounted = $state(false);
	let new_data = $state<FinancialData | null>(null);
	let activeMetric = $state('');

	const pageDataRef = $derived({
		data: $page.data.data[0] as FinancialData
	});

	$effect(() => {
		if (mounted && pageDataRef.data) {
			new_data = pageDataRef.data;
		}
	});

	const metrics = [
		{
			id: 'evToSales',
			title: 'EV to Sales (ttm)',
			Icon: ChartBar,
			Component: Tutorial,
			description: 'Learn how Enterprise Value to Sales helps value growth companies',
			color: 'from-emerald-500 to-green-600',
			bgHover: 'hover:bg-emerald-500/10'
		},
		{
			id: 'evToEbitda',
			title: 'EV to EBITDA',
			Icon: Calculator,
			Component: EVtoEbitda,
			description: 'Understand operating performance valuation using EV/EBITDA',
			color: 'from-green-500 to-emerald-600',
			bgHover: 'hover:bg-green-500/10'
		},
		{
			id: 'priceToSales',
			title: 'Price to Sales (ttm)',
			Icon: DollarSign,
			Component: PSales,
			description: 'Explore revenue-based valuation metrics',
			color: 'from-teal-500 to-green-600',
			bgHover: 'hover:bg-teal-500/10'
		},
		{
			id: 'trailingPE',
			title: 'Trailing P/E',
			Icon: TrendingUp,
			Component: TrailingPe,
			description: 'Learn about historical earnings-based valuation',
			color: 'from-green-600 to-emerald-500',
			bgHover: 'hover:bg-green-600/10'
		},
		{
			id: 'forwardPE',
			title: 'Forward P/E',
			Icon: LineChart,
			Component: Fwdpe,
			description: 'Understand future earnings expectations and valuation',
			color: 'from-emerald-600 to-green-500',
			bgHover: 'hover:bg-emerald-600/10'
		}
	] as const;

	onMount(() => {
		mounted = true;
		if (pageDataRef.data) {
			new_data = pageDataRef.data;
		}
	});
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	{#if mounted && new_data}
		<div class="mb-8">
			<ValuationCard {...new_data} />
		</div>
	{/if}

	{#if mounted}
		<div class="space-y-6">
			<div class="text-center">
				<h2 class="text-2xl font-bold tracking-tight text-primary">
					Understanding Valuation Metrics
				</h2>
				<p class="mt-2 text-muted-foreground">
					Click any metric below to learn more about how it works and why it matters
				</p>
			</div>

			<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
				{#each metrics as metric}
					<Dialog.Root>
						<Dialog.Trigger>
							<Card.Root
								class="hover:scale-102 group h-full overflow-hidden transition-all duration-300"
							>
								<Card.Header class="space-y-1">
									<div class="flex items-center justify-between">
										<div class={`rounded-full p-2 ${metric.bgHover}`}>
											<metric.Icon
												class={`h-6 w-6 bg-gradient-to-r ${metric.color} bg-clip-text text-transparent`}
											/>
										</div>
										<span class="text-sm text-muted-foreground">Click to learn more</span>
									</div>
									<Card.Title
										class={`bg-gradient-to-r ${metric.color} bg-clip-text text-xl font-semibold text-transparent transition-colors group-hover:bg-clip-text`}
									>
										{metric.title}
									</Card.Title>
								</Card.Header>
								<Card.Content>
									<p class="text-sm text-muted-foreground">{metric.description}</p>
								</Card.Content>
							</Card.Root>
						</Dialog.Trigger>

						<Dialog.Portal>
							<Dialog.Overlay class="fixed inset-0 bg-black/80 backdrop-blur-sm" />
							<Dialog.Content
								class="fixed left-[50%] top-[50%] flex h-[90vh] w-[95vw] max-w-[1400px] -translate-x-1/2 -translate-y-1/2 flex-col rounded-xl border bg-background shadow-2xl"
							>
								<div class={`w-full bg-gradient-to-r ${metric.color} flex-shrink-0 p-6`}>
									<Dialog.Title class="text-4xl font-bold text-white">
										{metric.title}
									</Dialog.Title>
									<Dialog.Description class="mt-2 text-white/90">
										{metric.description}
									</Dialog.Description>
								</div>

								<div class="flex-1 overflow-y-auto p-6">
									<div class="tutorial-content">
										<metric.Component />
									</div>
								</div>

								<div
									class="flex-shrink-0 border-t bg-background/95 p-6 backdrop-blur supports-[backdrop-filter]:bg-background/50"
								>
									<Dialog.Close
										class="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
									>
										Close Tutorial
									</Dialog.Close>
								</div>
							</Dialog.Content>
						</Dialog.Portal>
					</Dialog.Root>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.tutorial-content {
		max-height: calc(90vh - 200px);
		overflow-y: auto;
	}

	.tutorial-content::-webkit-scrollbar {
		width: 8px;
	}

	.tutorial-content::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
	}

	.tutorial-content::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.2);
		border-radius: 4px;
	}

	.tutorial-content::-webkit-scrollbar-thumb:hover {
		background: rgba(0, 0, 0, 0.3);
	}
</style>
