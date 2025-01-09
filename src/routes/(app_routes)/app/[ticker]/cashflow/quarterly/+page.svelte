<script lang="ts">
	import type { PageData } from '../quarterly/$types';
	import DataTable from '$lib/components/display/DataTable.svelte';

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

<DataTable
	{rawData}
	{yoyData}
	{marginsData}
	quarters={quarterDates}
	title="Cash Flow Statement - Quarterly"
	ratioMetrics={marginMetrics}
/>
