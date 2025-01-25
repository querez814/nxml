<script lang="ts">
	import type { PageData } from '../quarterly/$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import CashFlowTutorial from '$lib/components/tutorial/cashflow/CashFlowTutorial.svelte';
	let showTutorial = $state(false);
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];

	function formatMetricName(name: string): string {
		return name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase());
	}

	const quarterDates = quarters.map((q: any) => q.fiscalDateEnding);

	const marginMetrics = [
		'net_profit_margin',
		'ocf_margin',
		'fcf_margin',
		'roce',
		'cash_flow_adequacy_ratio',
		'capex_ratio'
	];

	const excludedKeys = [
		'_id',
		'symbol',
		'reportedCurrency',
		'__v',
		'fiscalDateEnding',
		...marginMetrics
	];

	const rawData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) => !excludedKeys.includes(key) && !key.endsWith('_YoY') && !key.endsWith('_QoQ')
					)
					.map((metric) => ({
						metric: formatMetricName(metric),
						originalMetric: metric,
						...quarters.reduce(
							(acc: any, quarter: any) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];

	const yoyData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) => key.endsWith('_YoY') && !marginMetrics.some((metric) => key.startsWith(metric))
					)
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_YoY', '')),
						originalMetric: metric.replace('_YoY', ''),
						...quarters.reduce(
							(acc: any, quarter: any) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];
	const qoqData =
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
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];
	const marginsData =
		quarters.length > 0
			? marginMetrics.map((metric) => ({
					metric: formatMetricName(metric),
					originalMetric: metric,
					...quarters.reduce(
						(acc: any, quarter: any) => ({
							...acc,
							[quarter.fiscalDateEnding]: quarter[metric]
						}),
						{}
					)
				}))
			: [];
</script>

<div class="mb-4 flex justify-end">
	{#if !showTutorial}
		<button
			class="rounded border border-green-400/20 px-3 py-1 font-mono text-xs text-green-400 hover:text-green-300"
			onclick={() => (showTutorial = true)}
		>
			📊 Learn about the Cash Flow Statement
		</button>
	{/if}
</div>
{#if showTutorial}
	<div class="mb-6">
		<div class="relative">
			<CashFlowTutorial />
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
	{marginsData}
	quarters={quarterDates}
	title="Cash Flow Statement - Quarterly"
	ratioMetrics={marginMetrics}
/>
