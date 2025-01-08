<script lang="ts">
	import type { PageData } from './$types';
	import DataTable from '$lib/components/display/DataTable.svelte';

	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];

	// Helper function to format metric names
	function formatMetricName(name: string): string {
		return (
			name
				// Skip fiscal date ending
				.replace(/([A-Z])/g, ' $1') // Add space before capital letters
				.split('_')
				.join(' ') // Replace underscores with spaces
				.trim() // Remove extra spaces
				.replace(/\b\w/g, (c) => c.toUpperCase())
		); // Capitalize first letter of each word
	}

	// Extract fiscal dates for the quarters prop
	const quarterDates = quarters.map((q) => q.fiscalDateEnding);

	// Transform for raw metrics (excluding YoY and QoQ)
	const rawData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							// Exclude these fields
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
			: [];

	// Transform for YoY metrics
	const yoyData =
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
			: [];

	// Transform for QoQ metrics
	const qoqData =
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
			: [];
</script>

<DataTable {rawData} {yoyData} {qoqData} quarters={quarterDates} title="Balance Sheet Metrics" />
