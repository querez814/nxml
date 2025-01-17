<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import IncomeStatementTutorial from '$lib/components/tutorial/incomestatement/IncomeStatementTutorial.svelte';
	import type { PageData } from '../quarterly/$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import { frontPageNews } from '../../../../../../api/media/generalnews';

	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];

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

	const quarterDates = quarters.map((q: any) => q.fiscalDateEnding);

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

	const rawData =
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
			: [];

	const yoyData =
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

<div class="relative z-10">
	<DataTable
		class="relative z-10"
		{rawData}
		{yoyData}
		{qoqData}
		{marginsData}
		quarters={quarterDates}
		title="Quarterly Income Statement"
		ratioMetrics={marginMetrics}
	/>
</div>
