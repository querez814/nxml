<script lang="ts">
	import type { PageData } from './$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import IncomeStatementTutorial from '$lib/components/tutorial/incomestatement/IncomeStatementTutorial.svelte';
	let showTutorial = $state(false);

	let { data }: { data: PageData } = $props();
	const quarters = $derived(data.quarters || []);

	function formatMetricName(name: string): string {
		return name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase());
	}

	const quarterDates = $derived(quarters.map((q: any) => q.fiscalDateEnding));

	const marginMetrics = ['grossMargin', 'ebitdaMargin', 'operatingMargin', 'netMargin'];

	const excludedKeys = [
		'_id',
		'symbol',
		'reportedCurrency',
		'__v',
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
								[quarter.fiscalDateEnding]: quarter[metric]
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
							[quarter.fiscalDateEnding]: quarter[metric]
						}),
						{}
					)
				}))
			: []
	);
</script>

<div class="mb-4 flex justify-end">
	{#if !showTutorial}
		<button
			class="rounded border border-green-400/20 px-3 py-1 font-mono text-xs text-green-400 hover:text-green-300"
			onclick={() => (showTutorial = true)}
		>
			📊 Learn about Income Statements
		</button>
	{/if}
</div>

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
	{rawData}
	{yoyData}
	{marginsData}
	quarters={quarterDates}
	title="Annual Income Statement"
	ratioMetrics={marginMetrics}
/>
