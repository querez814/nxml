<script lang="ts">
	import Fwdpe from '$lib/components/tutorial/FWDPE.svelte';
	import TrailingPe from '$lib/components/tutorial/TrailingPE.svelte';
	import PSales from '$lib/components/tutorial/PSales.svelte';
	import ValuationCard from '$lib/components/ui/valuationcard/ValuationCard.svelte';
	import Tutorial from '$lib/components/tutorial/Tutorial.svelte';
	import EVtoEbitda from '$lib/components/tutorial/EVtoEbitda.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import type { PageData } from './$types';

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

	let cardTitle = $state('EV to Sales');
	let desc1 = $state('We can break it down into two components');
	let desc2 = $state('Enterprise Value & Revenue (ttm)');
	let content1 = $state('Enterprise Value');
	let content2 = $state('Revenue (ttm)');

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
			component: Tutorial,
			description: 'Learn how Enterprise Value to Sales helps value growth companies'
		},
		{
			id: 'evToEbitda',
			title: 'EV to EBITDA',
			component: EVtoEbitda,
			description: 'Understand operating performance valuation using EV/EBITDA'
		},
		{
			id: 'priceToSales',
			title: 'Price to Sales (ttm)',
			component: PSales,
			description: 'Explore revenue-based valuation metrics'
		},
		{
			id: 'trailingPE',
			title: 'Trailing P/E',
			component: TrailingPe,
			description: 'Learn about historical earnings-based valuation'
		},
		{
			id: 'forwardPE',
			title: 'Forward P/E',
			component: Fwdpe,
			description: 'Understand future earnings expectations and valuation'
		}
	] as const;

	onMount(() => {
		mounted = true;
		if (pageDataRef.data) {
			new_data = pageDataRef.data;
		}
	});

	const ActiveComponent = $derived(
		metrics.find((m) => m.id === activeMetric)?.component ?? Tutorial
	);
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	{#if mounted && new_data}
		<div class="mb-8">
			<ValuationCard
				symbol={new_data.symbol}
				AnalystTargetPrice={new_data.AnalystTargetPrice}
				AnalystRatingStrongBuy={new_data.AnalystRatingStrongBuy}
				AnalystRatingBuy={new_data.AnalystRatingBuy}
				AnalystRatingHold={new_data.AnalystRatingHold}
				AnalystRatingSell={new_data.AnalystRatingSell}
				AnalystRatingStrongSell={new_data.AnalystRatingStrongSell}
				evtosales={new_data.evtosales}
				evtoebitda={new_data.evtoebitda}
				revenue_per_share_ttm={new_data.revenue_per_share_ttm}
				price_to_sales_ratio_ttm={new_data.price_to_sales_ratio_ttm}
				TrailingPE={new_data.TrailingPE}
				ForwardPE={new_data.ForwardPE}
			/>
		</div>
	{/if}

	{#if mounted}
		<div class="grid grid-cols-1 gap-6 p-6 md:grid-cols-2 lg:grid-cols-3">
			{#each metrics as metric}
				<Dialog.Root>
					<Dialog.Trigger>
						<button
							class="w-full rounded-lg p-4 text-3xl text-green-700 transition-all duration-300 ease-in-out hover:scale-105 hover:bg-green-50/10 hover:text-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 motion-safe:animate-pulse"
							onclick={() => (activeMetric = metric.id)}
						>
							{metric.title}
						</button>
					</Dialog.Trigger>

					<Dialog.Portal>
						<Dialog.Overlay class="fixed inset-0 bg-black/50 backdrop-blur-sm" />
						<Dialog.Content
							class="fixed left-[50%] top-[50%] h-[90vh] w-[95vw] max-w-[1400px] translate-x-[-50%] translate-y-[-50%] overflow-y-auto rounded-lg bg-white p-8 shadow-xl"
						>
							<div class="mx-auto flex h-full max-w-[1200px] flex-col">
								<Dialog.Title class="mb-2 text-2xl font-bold text-green-700">
									{metric.title}
								</Dialog.Title>

								<Dialog.Description class="mb-6 text-slate-600">
									{metric.description}
								</Dialog.Description>

								<div class="flex-grow overflow-y-auto py-4">
									{#if ActiveComponent}
										<ActiveComponent />
									{/if}
								</div>

								<div class="flex justify-end border-t border-slate-200 pt-6">
									<Dialog.Close
										class="rounded-lg bg-green-700 px-4 py-2 text-white transition-colors hover:bg-green-600"
									>
										Close Tutorial
									</Dialog.Close>
								</div>
							</div>
						</Dialog.Content>
					</Dialog.Portal>
				</Dialog.Root>
			{/each}
		</div>
	{/if}
</div>
