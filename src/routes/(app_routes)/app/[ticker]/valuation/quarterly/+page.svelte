<script lang="ts">
	import type { PageData } from './$types';
	import DataTable from '$lib/components/display/DataTable.svelte';

	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];

	function formatMetricName(name: string): string {
		const metricDisplayNames: { [key: string]: string } = {
			evtosales: 'EV/Sales',
			evtogrossprofit: 'EV/Gross Profit',
			evtoebit: 'EV/EBIT',
			evtoebitda: 'EV/EBITDA',
			evtonetincome: 'EV/Net Income',
			revenue_per_share_ttm: 'Revenue Per Share (TTM)',
			price_to_sales_ratio_ttm: 'Price to Sales Ratio (TTM)'
		};

		return (
			metricDisplayNames[name] ||
			name
				.replace(/([A-Z])/g, ' $1')
				.split('_')
				.join(' ')
				.trim()
				.replace(/\b\w/g, (c) => c.toUpperCase())
		);
	}
	const quarterDates = quarters.map((q) => q.fiscalDateEnding);

	// Define the metrics we want to display
	const valuationMetrics = [
		'evtosales',
		'evtogrossprofit',
		'evtoebit',
		'evtoebitda',
		'evtonetincome',
		'revenue_per_share_ttm',
		'price_to_sales_ratio_ttm'
	];

	const excludedKeys = [
		'_id',
		'symbol',
		'reportedCurrency',
		'__v',
		'fiscalDateEnding',
		'AnalystTargetPrice',
		'AnalystRatingStrongBuy',
		'AnalystRatingBuy',
		'AnalystRatingHold',
		'AnalystRatingSell',
		'AnalystRatingStrongSell',
		'TrailingPE',
		'ForwardPE',
		'Sector',
		'Industry'
	];

	// Create raw data structure for the DataTable
	const rawData =
		quarters.length > 0
			? valuationMetrics.map((metric) => ({
					metric: formatMetricName(metric),
					originalMetric: metric,
					...quarters.reduce(
						(acc, quarter) => ({
							...acc,
							[quarter.fiscalDateEnding]: quarter[metric].toFixed(2)
						}),
						{}
					)
				}))
			: [];

	// Since valuation metrics don't have YoY or QoQ, we'll pass empty arrays
	const yoyData = [];
	const qoqData = [];
	const marginsData = [];
</script>

<DataTable
	{rawData}
	quarters={quarterDates}
	title="Valuation Metrics"
	ratioMetrics={valuationMetrics}
/>
