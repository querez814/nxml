<script lang="ts">
	import { page } from '$app/stores';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';
	import type { PageData } from './$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import BalanceSheetTutorial from '$lib/components/tutorial/balancesheet/BalanceSheetTutorial.svelte';

	const apiUrl = import.meta.env.VITE_API_URL;

	let { data }: { data: PageData } = $props();
	const quarters = $derived(data.quarters || []);
	let showTutorial = $state(false);
	let analysisLoading = $state(false);
	let analysisError = $state<string | null>(null);
	let analysisText = $state<string | null>(null);
	let showAnalysis = $state(false);

	const ticker = $derived($page.params.ticker?.toUpperCase() ?? '');

	const analysisHtml = $derived(
		analysisText
			? DOMPurify.sanitize(marked.parse(analysisText) as string, { USE_PROFILES: { html: true } })
			: ''
	);

	async function runAIAnalysis() {
		if (!ticker) return;
		analysisLoading = true;
		analysisError = null;
		analysisText = null;
		showAnalysis = true;
		try {
			const res = await fetch(`${apiUrl}/analysis/balancesheet-statement/${ticker}`, {
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
	function formatMetricName(name: string): string {
		return name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase());
	}

	const quarterDates = $derived(quarters.map((q) => q.fiscalDateEnding));

	const rawData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							!['_id', 'symbol', 'reportedCurrency', '__v', 'fiscalDateEnding'].includes(key) &&
							!key.endsWith('_YoY') &&
							!key.endsWith('_QoQ')
					)
					.map((metric) => ({
						metric: formatMetricName(metric),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);

	const yoyData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter((key) => key.endsWith('_YoY'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_YoY', '')),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);

	const qoqData = $derived(
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter((key) => key.endsWith('_QoQ'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_QoQ', '')),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: []
	);
</script>

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
			📊 Learn about the Balance Sheet Statement
		</button>
	{/if}
</div>

{#if showAnalysis}
	<div class="mb-6 rounded-lg border border-gray-700/50 bg-gray-900/40 p-4">
		<div class="mb-2 flex items-center justify-between">
			<span class="font-mono text-sm text-amber-400">Balance Sheet AI Analysis</span>
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
			<BalanceSheetTutorial />
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
	{rawData}
	{yoyData}
	{qoqData}
	quarters={quarterDates}
	title="Balance Sheet - Quarterly"
/>
