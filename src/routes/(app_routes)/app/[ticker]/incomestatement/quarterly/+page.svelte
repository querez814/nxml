<script lang="ts">
	import { page } from '$app/stores';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';
	import * as Button from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Dialog from '$lib/components/ui/dialog';
	import IncomeStatementTutorial from '$lib/components/tutorial/incomestatement/IncomeStatementTutorial.svelte';
	import type { PageData } from '../quarterly/$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import { formatFiscalQuarterLabel } from '$lib/utils/fiscalQuarterDates';

	const apiUrl = import.meta.env.VITE_API_URL;

	let showTutorial = $state(false);
	let analysisLoading = $state(false);
	let analysisError = $state<string | null>(null);
	let analysisText = $state<string | null>(null);
	let showAnalysis = $state(false);
	let revenueSegments = $state<Record<string, unknown> | null>(null);
	let revenueSegmentsLoading = $state(false);

	const ticker = $derived($page.params.ticker?.toUpperCase() ?? '');

	const analysisHtml = $derived(
		analysisText
			? DOMPurify.sanitize(marked.parse(analysisText) as string, { USE_PROFILES: { html: true } })
			: ''
	);

	let { data }: { data: PageData } = $props();
	const quarters = $derived(data.quarters || []);

	function formatMetricName(name: string): string {
		const specialCases: any = {
			costofGoodsAndServicesSold: 'Cost of Goods and Services Sold',
			sellingGeneralAndAdministrative: 'Selling, General and Administrative',
			researchAndDevelopment: 'Research and Development',
			interestAndDebtExpense: 'Interest and Debt Expense',
			ebit: 'EBIT',
			ebitda: 'EBITDA',
			reportedEPS: 'Reported EPS ',
			estimatedEPS: 'Estimated EPS',
			surprise: 'EPS Surprise'
		};

		if (specialCases[name]) {
			return specialCases[name];
		}
		return name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase());
	}

	const quarterDates = $derived(
		quarters.map((q: any) => formatFiscalQuarterLabel(q.fiscalDateEnding))
	);

	const marginMetrics = ['grossMargin', 'ebitdaMargin', 'operatingMargin', 'netMargin'];

	const excludedKeys = [
		'_id',
		'symbol',
		'reportedCurrency',
		'__v',
		'surprisePercentage',
		'ebitMargin',
		'fiscalDateEnding',
		...marginMetrics
	];

	const rawData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							!excludedKeys.includes(key) &&
							!key.includes('_Derivative') &&
							!key.endsWith('_YoY') &&
							!key.endsWith('_QoQ')
					)
					.map((metric) => ({
						metric: formatMetricName(metric),
						originalMetric: metric,
						...quarters.reduce(
							(acc: any, quarter: any) => ({
								...acc,
								[formatFiscalQuarterLabel(quarter.fiscalDateEnding)]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);

	const yoyData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							key.endsWith('_YoY') &&
							!key.includes('_Derivative') &&
							!marginMetrics.some((metric) => key.startsWith(metric))
					)
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_YoY', '')),
						originalMetric: metric.replace('_YoY', ''),
						...quarters.reduce(
							(acc: any, quarter: any) => ({
								...acc,
								[formatFiscalQuarterLabel(quarter.fiscalDateEnding)]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);
	const qoqData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							key.endsWith('_QoQ') &&
							!key.includes('_Derivative') &&
							!marginMetrics.some((metric) => key.startsWith(metric))
					)
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_QoQ', '')),
						originalMetric: metric.replace('_QoQ', ''),
						...quarters.reduce(
							(acc: any, quarter: any) => ({
								...acc,
								[formatFiscalQuarterLabel(quarter.fiscalDateEnding)]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);
	const marginsData = $derived(
		quarters.length > 0
			? marginMetrics.map((metric) => ({
					metric: formatMetricName(metric),
					originalMetric: metric,
					...quarters.reduce(
						(acc: any, quarter: any) => ({
							...acc,
							[formatFiscalQuarterLabel(quarter.fiscalDateEnding)]: quarter[metric]
						}),
						{}
					)
				}))
			: []
	);

	async function runAIAnalysis() {
		if (!ticker) return;
		analysisLoading = true;
		analysisError = null;
		analysisText = null;
		showAnalysis = true;
		try {
			const res = await fetch(`${apiUrl}/analysis/income-statement/${ticker}`, {
				method: 'POST'
			});
			const json = await res.json();
			if (!res.ok) {
				throw new Error(json.detail ?? `Request failed: ${res.status}`);
			}
			analysisText = json.analysis ?? '';
		} catch (e) {
			analysisError = e instanceof Error ? e.message : 'Failed to fetch analysis';
		} finally {
			analysisLoading = false;
		}
	}

	async function fetchRevenueSegments() {
		if (!ticker) return;
		revenueSegmentsLoading = true;
		revenueSegments = null;
		try {
			const res = await fetch(`${apiUrl}/analysis/revenue-segments/${ticker}`, {
				method: 'POST'
			});
			const json = await res.json();
			if (!res.ok) {
				throw new Error(json.detail ?? `Request failed: ${res.status}`);
			}
			revenueSegments = json;
		} catch (e) {
			revenueSegments = {
				has_segment_disclosure: false,
				segments: [],
				no_segment_reason:
					e instanceof Error ? e.message : 'Failed to fetch revenue segments'
			};
		} finally {
			revenueSegmentsLoading = false;
		}
	}
</script>

<div class="relative z-10">
	<div class="mb-4 flex justify-end gap-2">
		<button
			class="rounded border border-amber-400/30 px-3 py-1 font-mono text-xs text-amber-400 hover:text-amber-300 disabled:opacity-50"
			onclick={runAIAnalysis}
			disabled={analysisLoading || !ticker || quarters.length === 0}
		>
			{analysisLoading ? '⏳ Analyzing...' : '🤖 AI Analysis'}
		</button>
		{#if !showTutorial}
			<button
				class="rounded border border-green-400/20 px-3 py-1 font-mono text-xs text-green-400 hover:text-green-300"
				onclick={() => (showTutorial = true)}
			>
				📊 Learn about Income Statements
			</button>
		{/if}
	</div>

	{#if showAnalysis}
		<div class="mb-6 rounded-lg border border-gray-700/50 bg-gray-900/40 p-4">
			<div class="mb-2 flex items-center justify-between">
				<span class="font-mono text-sm text-amber-400">Income Statement AI Analysis</span>
				<button
					class="text-xs text-gray-400 hover:text-gray-300"
					onclick={() => (showAnalysis = false)}
				>
					✕ Close
				</button>
			</div>
			{#if analysisLoading}
				<p class="text-sm text-gray-400">Fetching data and generating analysis...</p>
			{:else if analysisError}
				<p class="text-sm text-red-400">{analysisError}</p>
			{:else if analysisText}
				<div
					class="prose prose-invert prose-sm max-w-none text-gray-300 [&_h3]:mt-4 [&_h3]:text-amber-400 [&_h4]:mt-3 [&_h4]:text-amber-300/90 [&_ul]:list-disc [&_ul]:pl-5"
				>
					{@html analysisHtml}
				</div>
			{/if}
		</div>
	{/if}

	{#if showTutorial}
		<div class="mb-6">
			<div class="relative">
				<IncomeStatementTutorial />
				<button
					class="absolute right-4 top-4 font-mono text-xs text-gray-400 hover:text-gray-300"
					onclick={() => (showTutorial = false)}
				>
					✕ Close
				</button>
			</div>
		</div>
	{/if}

	<DataTable
		class="relative z-10"
		{rawData}
		{yoyData}
		{qoqData}
		{marginsData}
		quarters={quarterDates}
		title="Quarterly Income Statement"
		ratioMetrics={marginMetrics}
		revenueSegments={revenueSegments}
		revenueSegmentsLoading={revenueSegmentsLoading}
		onFetchRevenueSegments={fetchRevenueSegments}
	/>
</div>
