<script lang="ts">
	import { Drawer } from 'vaul-svelte';
	import { createQuery } from '@tanstack/svelte-query';
	import { writable } from 'svelte/store';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import ValuationSplitDisplay from '$lib/components/display/ValuationSplitDisplay.svelte';
	import LineChart from '$lib/components/display/LineChart.svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import {
		fetchStatementAnalysis,
		type StatementAnalysisType
	} from '$lib/api/analysisClient';
	import {
		buildIncomeStatementTables,
		buildBalanceSheetTables,
		buildCashFlowTables,
		buildValuationTable
	} from '$lib/utils/statementTableData';
	import { parseLocaleNumber, sortQuartersDesc } from '$lib/utils/tickerPulse';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';
	import { ExternalLink, Maximize2 } from 'lucide-svelte';
	import type { StatementKind } from '$lib/types/statementKind';

	let {
		kind,
		ticker,
		open = $bindable(false),
		incomeQuarters = [],
		incomeAnnual = [],
		balanceQuarters = [],
		balanceAnnual = [],
		cashQuarters = [],
		cashAnnual = [],
		valuationSnapshots = []
	}: {
		kind: StatementKind;
		ticker: string;
		open?: boolean;
		incomeQuarters?: Record<string, unknown>[];
		incomeAnnual?: Record<string, unknown>[];
		balanceQuarters?: Record<string, unknown>[];
		balanceAnnual?: Record<string, unknown>[];
		cashQuarters?: Record<string, unknown>[];
		cashAnnual?: Record<string, unknown>[];
		valuationSnapshots?: Record<string, unknown>[];
	} = $props();

	let period = $state<'quarterly' | 'annual'>('quarterly');
	let mainTab = $state<'data' | 'ai'>('data');
	/** Slightly wider default so more panel sticks out (easier to grab). */
	let activeSnapPoint = $state<string | number | null>(0.78);
	let mobile = $state(
		typeof window !== 'undefined' && window.matchMedia('(max-width: 767px)').matches
	);

	let revenueSegments = $state<Record<string, unknown> | null>(null);
	let revenueSegmentsLoading = $state(false);

	$effect(() => {
		if (typeof window === 'undefined') return;
		const mq = window.matchMedia('(max-width: 767px)');
		mobile = mq.matches;
		const fn = () => (mobile = mq.matches);
		mq.addEventListener('change', fn);
		return () => mq.removeEventListener('change', fn);
	});

	$effect(() => {
		if (!open) return;
		void kind;
		mainTab = 'data';
		period = 'quarterly';
	});

	$effect(() => {
		if (kind !== 'income') revenueSegments = null;
	});

	const direction = $derived(mobile ? 'bottom' : 'right');
	const snapPoints = $derived<(number | string)[]>(mobile ? [0.88, 1] : [0.62, 0.78, 1]);

	const rows = $derived.by(() => {
		if (kind === 'income') return period === 'quarterly' ? incomeQuarters : incomeAnnual;
		if (kind === 'balance') return period === 'quarterly' ? balanceQuarters : balanceAnnual;
		if (kind === 'cashflow') return period === 'quarterly' ? cashQuarters : cashAnnual;
		return valuationSnapshots;
	});

	const tables = $derived.by(() => {
		if (kind === 'income') return buildIncomeStatementTables(rows);
		if (kind === 'balance') return buildBalanceSheetTables(rows);
		if (kind === 'cashflow') return buildCashFlowTables(rows);
		return { ...buildValuationTable(rows), yoyData: undefined, qoqData: undefined, marginsData: undefined };
	});

	const chartSeries = $derived.by(() => {
		if (!rows.length || kind === 'valuation') return [];
		const sorted = sortQuartersDesc(rows as { fiscalDateEnding: string }[]).slice(0, 12).reverse();
		if (kind === 'income') {
			return sorted.map((q) => ({
				date: q.fiscalDateEnding,
				value: parseLocaleNumber((q as Record<string, unknown>).totalRevenue) ?? 0
			}));
		}
		if (kind === 'balance') {
			return sorted.map((q) => ({
				date: q.fiscalDateEnding,
				value: parseLocaleNumber((q as Record<string, unknown>).current_ratio) ?? 0
			}));
		}
		return sorted.map((q) => ({
			date: q.fiscalDateEnding,
			value: parseLocaleNumber((q as Record<string, unknown>).freeCashFlow) ?? 0
		}));
	});

	const chartTitle = $derived(
		kind === 'income' ? 'Revenue ($M)' : kind === 'balance' ? 'Current ratio' : 'Free cash flow ($M)'
	);

	const analysisType = $derived.by((): StatementAnalysisType | null => {
		if (kind === 'income') return 'income-statement';
		if (kind === 'balance') return 'balancesheet-statement';
		if (kind === 'cashflow') return 'cashflow-statement';
		return null;
	});

	const analysisOpts = writable({
		queryKey: ['analysis', 'income-statement', ''] as [string, StatementAnalysisType, string],
		queryFn: () => fetchStatementAnalysis('income-statement', ''),
		enabled: false,
		staleTime: 5 * 60 * 1000
	});

	$effect(() => {
		const st = analysisType;
		const ty: StatementAnalysisType = st ?? 'income-statement';
		const en = open && mainTab === 'ai' && st !== null;
		analysisOpts.set({
			queryKey: ['analysis', ty, ticker],
			queryFn: () => fetchStatementAnalysis(ty, ticker),
			enabled: en,
			staleTime: 5 * 60 * 1000
		});
	});

	const analysisQuery = createQuery(analysisOpts);

	const analysisHtml = $derived.by(() => {
		const text = $analysisQuery.data?.analysis;
		if (!text) return '';
		return DOMPurify.sanitize(marked.parse(text) as string, { USE_PROFILES: { html: true } });
	});

	const fullPageHref = $derived.by(() => {
		const p = period === 'quarterly' ? 'quarterly' : 'annual';
		if (kind === 'income') return `/app/${ticker}/incomestatement/${p}`;
		if (kind === 'balance') return `/app/${ticker}/balancesheet/${p}`;
		if (kind === 'cashflow') return `/app/${ticker}/cashflow/${p}`;
		return `/app/${ticker}/valuation/quarterly`;
	});

	const drawerTitle = $derived.by(() => {
		if (kind === 'income') return 'Income statement';
		if (kind === 'balance') return 'Balance sheet';
		if (kind === 'cashflow') return 'Cash flow statement';
		return 'Valuation';
	});

	async function fetchRevenueSegments() {
		if (!ticker) return;
		revenueSegmentsLoading = true;
		revenueSegments = null;
		try {
			const res = await fetch(`${import.meta.env.VITE_API_URL}/analysis/revenue-segments/${ticker}`, {
				method: 'POST'
			});
			const json = await res.json();
			if (!res.ok) throw new Error(json.detail ?? `Request failed: ${res.status}`);
			revenueSegments = json;
		} catch (e) {
			revenueSegments = {
				has_segment_disclosure: false,
				segments: [],
				no_segment_reason: e instanceof Error ? e.message : 'Failed to fetch revenue segments'
			};
		} finally {
			revenueSegmentsLoading = false;
		}
	}

	function snapFull() {
		activeSnapPoint = 1;
	}
</script>

<Drawer.Root
	bind:open
	{direction}
	snapPoints={[...snapPoints]}
	bind:activeSnapPoint
	shouldScaleBackground={false}
	modal={true}
>
	<Drawer.Portal>
		<Drawer.Overlay class="fixed inset-0 z-[60] bg-black/50" />
		<Drawer.Content
			class="fixed z-[61] flex max-h-[96vh] flex-col border-gray-800 bg-[#0a0b0d] p-0 outline-none data-[vaul-drawer-direction=bottom]:rounded-t-xl data-[vaul-drawer-direction=right]:inset-y-0 data-[vaul-drawer-direction=right]:right-0 data-[vaul-drawer-direction=right]:h-full data-[vaul-drawer-direction=right]:max-w-none data-[vaul-drawer-direction=right]:border-l data-[vaul-drawer-direction=bottom]:inset-x-0 data-[vaul-drawer-direction=bottom]:bottom-0 data-[vaul-drawer-direction=bottom]:border-t md:flex-row"
		>
			{#if mobile}
				<Drawer.Handle
					class="mx-auto mt-3 h-1.5 w-14 shrink-0 rounded-full bg-gray-600 hover:bg-gray-500"
				/>
			{:else}
				<div
					class="flex w-7 shrink-0 flex-col items-center border-r border-gray-800 bg-[#101114] py-8"
					title="Drag to resize the panel"
				>
					<Drawer.Handle
						class="flex min-h-[120px] w-2 cursor-grab rounded-full bg-gray-600 hover:bg-gray-500 active:bg-gray-400"
					/>
					<span
						class="pointer-events-none mt-2 rotate-180 font-mono text-[8px] uppercase leading-3 text-gray-500 [writing-mode:vertical-rl]"
					>Drag</span>
				</div>
			{/if}
			<div class="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
			<div class="flex items-center justify-between gap-2 border-b border-gray-800 px-4 py-3">
				<div class="min-w-0">
					<h2 class="truncate font-mono text-sm font-semibold text-white">
						{drawerTitle}
						<span class="text-gray-500">· {ticker}</span>
					</h2>
					<div class="mt-1 flex flex-wrap items-center gap-2">
						{#if kind !== 'valuation'}
							<div class="flex rounded border border-gray-700 p-0.5 font-mono text-[10px]">
								<button
									type="button"
									class="rounded px-2 py-0.5 {period === 'quarterly'
										? 'bg-gray-800 text-emerald-400'
										: 'text-gray-500'}"
									onclick={() => (period = 'quarterly')}
								>
									Quarterly
								</button>
								<button
									type="button"
									class="rounded px-2 py-0.5 {period === 'annual'
										? 'bg-gray-800 text-emerald-400'
										: 'text-gray-500'}"
									onclick={() => (period = 'annual')}
								>
									Annual
								</button>
							</div>
						{/if}
					</div>
				</div>
				<div class="flex shrink-0 items-center gap-1">
					<button
						type="button"
						class="rounded p-2 text-gray-500 hover:bg-gray-800 hover:text-white"
						onclick={snapFull}
						title="Full width"
					>
						<Maximize2 class="h-4 w-4" />
					</button>
					<a
						href={fullPageHref}
						class="inline-flex items-center gap-1 rounded px-2 py-1 font-mono text-[10px] text-emerald-400 hover:bg-emerald-500/10"
					>
						Open full page
						<ExternalLink class="h-3 w-3" />
					</a>
				</div>
			</div>

			<div class="min-h-0 flex-1 overflow-y-auto px-2 py-4 md:px-4">
				{#if kind === 'valuation'}
					<ValuationSplitDisplay
						compact
						rawData={tables.rawData}
						quarterDates={tables.quarterDates}
						ratioMetrics={'ratioMetrics' in tables && tables.ratioMetrics ? tables.ratioMetrics : []}
						staticRows={'staticRows' in tables && tables.staticRows ? tables.staticRows : []}
						byPeriodTitle="By period"
					/>
				{:else}
					<Tabs.Root bind:value={mainTab} class="w-full">
						<Tabs.List class="mb-4 flex gap-1 rounded-lg border border-gray-800 bg-[#111215] p-1">
							<Tabs.Trigger
								value="data"
								class="rounded-md px-3 py-1.5 font-mono text-xs text-gray-400 data-[state=active]:bg-gray-800 data-[state=active]:text-white"
							>
								All data
							</Tabs.Trigger>
							<Tabs.Trigger
								value="ai"
								class="rounded-md px-3 py-1.5 font-mono text-xs text-gray-400 data-[state=active]:bg-gray-800 data-[state=active]:text-white"
							>
								AI summary
							</Tabs.Trigger>
						</Tabs.List>

						<Tabs.Content value="data" class="space-y-6">
							<DataTable
								class="relative z-10"
								rawData={tables.rawData}
								yoyData={'yoyData' in tables ? tables.yoyData : []}
								qoqData={'qoqData' in tables ? tables.qoqData : []}
								marginsData={'marginsData' in tables ? tables.marginsData : undefined}
								quarters={tables.quarterDates}
								title={drawerTitle}
								ratioMetrics={
									kind === 'income'
										? ['grossMargin', 'ebitdaMargin', 'operatingMargin', 'netMargin']
										: kind === 'cashflow' && 'marginMetrics' in tables
											? tables.marginMetrics
											: []
								}
								revenueSegments={revenueSegments}
								{revenueSegmentsLoading}
								onFetchRevenueSegments={kind === 'income' ? fetchRevenueSegments : null}
							/>
							{#if chartSeries.length}
								<div class="h-56 w-full rounded-lg border border-gray-800 bg-[#111215] p-2">
									<LineChart
										data={chartSeries}
										xKey="date"
										yKey="value"
										title={chartTitle}
									/>
								</div>
							{/if}
						</Tabs.Content>

						<Tabs.Content value="ai" class="min-h-[200px]">
							{#if $analysisQuery.isPending}
								<p class="text-sm text-gray-400">Fetching data and generating analysis…</p>
							{:else if $analysisQuery.isError}
								<p class="text-sm text-red-400">
									{$analysisQuery.error instanceof Error
										? $analysisQuery.error.message
										: 'Analysis failed'}
								</p>
							{:else if analysisHtml}
								<div class="max-h-[min(55vh,520px)] overflow-x-auto overflow-y-auto rounded border border-gray-800/50">
									<div
										class="prose prose-invert prose-sm min-w-0 max-w-none p-3 text-gray-300 [&_table]:block [&_table]:w-max [&_table]:min-w-full [&_table]:border-collapse [&_table]:border [&_table]:border-gray-700 [&_td]:border [&_td]:border-gray-700 [&_td]:px-2 [&_td]:py-1 [&_th]:border [&_th]:border-gray-700 [&_th]:px-2 [&_th]:py-1 [&_h3]:mt-4 [&_h3]:text-amber-400 [&_h4]:mt-3 [&_h4]:text-amber-300/90 [&_ul]:list-disc [&_ul]:pl-5"
									>
										<!-- eslint-disable-next-line svelte/no-at-html-tags -->
										{@html analysisHtml}
									</div>
								</div>
							{:else}
								<p class="text-sm text-gray-500">No analysis returned.</p>
							{/if}
						</Tabs.Content>
					</Tabs.Root>
				{/if}
			</div>
			</div>
		</Drawer.Content>
	</Drawer.Portal>
</Drawer.Root>
