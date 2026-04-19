<script lang="ts">
	import type { PageData } from './$types';
	import type { NewsRecapPayload } from '$lib/api/newsRecap';
	import HeroBar from '$lib/components/app/HeroBar.svelte';
	import VitalsStrip from '$lib/components/app/VitalsStrip.svelte';
	import PulseCard from '$lib/components/app/PulseCard.svelte';
	import AiIntel from '$lib/components/app/AiIntel.svelte';
	import StatementDrawer from '$lib/components/app/StatementDrawer.svelte';
	import type { StatementKind } from '$lib/types/statementKind';
	import {
		buildVitalsStrip,
		buildIncomePulse,
		buildBalancePulse,
		buildCashFlowPulse,
		buildValuationPulse
	} from '$lib/utils/tickerPulse';

	let { data }: { data: PageData } = $props();

	const ticker = $derived(data.ticker?.toLocaleUpperCase() ?? '');
	const layout = $derived(data.layout);
	const incomeQuarters = $derived((data.incomeQuarters ?? []) as Record<string, unknown>[]);
	const incomeAnnual = $derived((data.incomeAnnual ?? []) as Record<string, unknown>[]);
	const balanceQuarters = $derived((data.balanceQuarters ?? []) as Record<string, unknown>[]);
	const balanceAnnual = $derived((data.balanceAnnual ?? []) as Record<string, unknown>[]);
	const cashQuarters = $derived((data.cashQuarters ?? []) as Record<string, unknown>[]);
	const cashAnnual = $derived((data.cashAnnual ?? []) as Record<string, unknown>[]);
	const valuationQuarters = $derived((data.valuationQuarters ?? []) as Record<string, unknown>[]);

	let drawerOpen = $state(false);
	let drawerKind = $state<StatementKind>('income');

	const latestPrice = $derived(layout?.latest?.latest_closing_price ?? layout?.latest?.adjusted_price ?? null);

	const vitals = $derived(buildVitalsStrip(incomeQuarters, cashQuarters, layout));
	const incomePulse = $derived(buildIncomePulse(incomeQuarters));
	const balancePulse = $derived(buildBalancePulse(balanceQuarters));
	const cashPulse = $derived(buildCashFlowPulse(cashQuarters));
	const valPulse = $derived(
		buildValuationPulse(layout, latestPrice, layout?.latest?.analyst_target_price ?? null)
	);

	const valFooter = $derived(
		valPulse.upsidePct != null
			? `Target vs spot ${valPulse.upsidePct >= 0 ? '+' : ''}${valPulse.upsidePct.toFixed(1)}%`
			: ''
	);

	function openDrawer(kind: StatementKind) {
		drawerKind = kind;
		drawerOpen = true;
	}
</script>

<div class="min-h-screen bg-[#0a0b0d] pb-16 pt-2">
	<div class="mb-4">
		<a
			href="/app"
			class="inline-flex items-center rounded border border-gray-800 bg-[#111215] px-3 py-1.5 font-mono text-xs uppercase tracking-wide text-gray-300 transition hover:border-gray-700 hover:text-white"
		>
			Home
		</a>
	</div>

	<div class="mx-auto flex max-w-6xl flex-col gap-4">
		<HeroBar {ticker} {layout} latestPrice={latestPrice} dayChangePct={null} />

		<VitalsStrip lines={vitals} />

		<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
			<PulseCard
				title="Income statement"
				kpis={incomePulse.kpis}
				sparklineData={incomePulse.sparkline}
				health={incomePulse.health}
				onOpen={() => openDrawer('income')}
			/>
			<PulseCard
				title="Balance sheet"
				kpis={balancePulse.kpis}
				sparklineData={balancePulse.sparkline}
				health={balancePulse.health}
				onOpen={() => openDrawer('balance')}
			/>
			<PulseCard
				title="Cash flow"
				kpis={cashPulse.kpis}
				sparklineData={cashPulse.sparkline}
				health={cashPulse.health}
				onOpen={() => openDrawer('cashflow')}
			/>
			<PulseCard
				title="Valuation"
				kpis={valPulse.kpis}
				sparklineData={undefined}
				showSparkline={false}
				health={valPulse.health}
				footerExtra={valFooter}
				onOpen={() => openDrawer('valuation')}
			/>
		</div>

		{#await data.streamed.newsRecap}
			<AiIntel {ticker} newsRecap={null} newsLoading={true} newsError={null} />
		{:then recap}
			<AiIntel
				{ticker}
				newsRecap={recap as NewsRecapPayload | null}
				newsLoading={false}
				newsError={recap == null ? 'News recap is temporarily unavailable.' : null}
			/>
		{/await}
	</div>
</div>

<StatementDrawer
	bind:open={drawerOpen}
	kind={drawerKind}
	{ticker}
	{incomeQuarters}
	{incomeAnnual}
	{balanceQuarters}
	{balanceAnnual}
	{cashQuarters}
	{cashAnnual}
	valuationSnapshots={valuationQuarters}
/>

<style>
	:global(body) {
		background-color: #0a0b0d;
		color: #ffffff;
	}
</style>
