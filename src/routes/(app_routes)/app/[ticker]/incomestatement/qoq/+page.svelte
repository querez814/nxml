<script lang="ts">
	import type { PageData } from './$types';
	import { TableHandler, Datatable, ThSort, ThFilter } from '@vincjo/datatables';

	interface RowData {
		metric: string;
		[key: string]: string;
	}

	type Field<T> = keyof T;

	let { data }: { data: PageData } = $props();

	const metricsMap = new Map([
		['grossProfit_QoQ', 'Gross Profit'],
		['totalRevenue_QoQ', 'Total Revenue'],
		['netRevenue_QoQ', 'Net Revenue'],
		['costofGoodsAndServicesSold_QoQ', 'Cost of Goods And Services Sold'],
		['operatingIncome_QoQ', 'Operating Income'],
		['sellingGeneralAndAdministrative_QoQ', 'Selling General And Administrative'],
		['researchAndDevelopment_QoQ', 'Research And Development'],
		['operatingExpenses_QoQ', 'Operating Expenses'],
		['interestIncome_QoQ', 'Interest Income'],
		['interestExpense_QoQ', 'Interest Expense'],
		['incomeBeforeTax_QoQ', 'Income Before Tax'],
		['incomeTaxExpense_QoQ', 'Income Tax Expense'],
		['interestAndDebtExpense_QoQ', 'Interest And Debt Expense'],
		['ebit_QoQ', 'EBIT'],
		['ebitda_QoQ', 'EBITDA'],
		['netIncome_QoQ', 'Net Income'],
		['reportedEPS_QoQ', 'Reported EPS'],
		['estimatedEPS_QoQ', 'Estimated EPS'],
		['surprise_QoQ', 'Surprise'],
		['surprisePercentage_QoQ', 'Surprise Percentage']
	]);
	const tableData: RowData[] = Array.from(metricsMap.entries()).map(([key, metric]) => ({
		metric,
		...data.quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[quarter.fiscalDateEnding]: quarter[key] || '0%'
			}),
			{} as Record<string, string>
		)
	}));

	const table = new TableHandler<RowData>(tableData, { rowsPerPage: 40 });
</script>

<div class="container mx-auto p-4">
	<h2 class="mb-4 text-2xl font-bold">Financial Metrics (Quarter over Quarter)</h2>

	<Datatable basic {table}>
		<table class="w-full border-collapse">
			<thead>
				<tr>
					<ThSort {table} field={'metric' as Field<RowData>}>Metric</ThSort>
					{#each data.quarters as quarter}
						<ThSort {table} field={quarter.fiscalDateEnding as Field<RowData>}>
							{new Date(quarter.fiscalDateEnding).toLocaleDateString('en-US', {
								year: 'numeric',
								month: 'short'
							})}
						</ThSort>
					{/each}
				</tr>
				<tr>
					<ThFilter {table} field={'metric' as Field<RowData>} />
					{#each data.quarters as quarter}
						<ThFilter {table} field={quarter.fiscalDateEnding as Field<RowData>} />
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each table.rows as row (row.metric)}
					<tr>
						<td>{row.metric}</td>
						{#each data.quarters as quarter}
							<td
								class={String(row[quarter.fiscalDateEnding]).startsWith('-')
									? 'text-red-500'
									: 'text-green-500'}
							>
								{row[quarter.fiscalDateEnding]}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</Datatable>
</div>
