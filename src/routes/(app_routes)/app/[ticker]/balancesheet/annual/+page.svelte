<script lang="ts">
	import type { PageData } from '../$types';
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

	const rawData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							!['_id', 'symbol', 'reportedCurrency', '__v', 'fiscalDateEnding'].includes(key) &&
							!key.endsWith('_YoY')
					)
					.map((metric) => ({
						metric: formatMetricName(metric),
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
					.filter((key) => key.endsWith('_YoY'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_YoY', '')),
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
					.filter((key) => key.endsWith('_QoQ'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_QoQ', '')),
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

<DataTable {rawData} {yoyData} quarters={quarterDates} title="Balance Sheet - Annual" />
