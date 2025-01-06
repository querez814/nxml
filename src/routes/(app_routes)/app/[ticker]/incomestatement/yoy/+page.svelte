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
		['grossProfit_YoY', 'Gross Profit'],
		['totalRevenue_YoY', 'Total Revenue'],
		['netRevenue_YoY', 'Net Revenue'],
		['costofGoodsAndServicesSold_YoY', 'Cost of Goods And Services Sold'],
		['operatingIncome_YoY', 'Operating Income'],
		['sellingGeneralAndAdministrative_YoY', 'Selling General And Administrative'],
		['researchAndDevelopment_YoY', 'Research And Development'],
		['operatingExpenses_YoY', 'Operating Expenses'],
		['interestIncome_YoY', 'Interest Income'],
		['interestExpense_YoY', 'Interest Expense'],
		['incomeBeforeTax_YoY', 'Income Before Tax'],
		['incomeTaxExpense_YoY', 'Income Tax Expense'],
		['interestAndDebtExpense_YoY', 'Interest And Debt Expense'],
		['ebit_YoY', 'EBIT'],
		['ebitda_YoY', 'EBITDA'],
		['netIncome_YoY', 'Net Income'],
		['reportedEPS_YoY', 'Reported EPS'],
		['estimatedEPS_YoY', 'Estimated EPS'],
		['surprise_YoY', 'Surprise'],
		['surprisePercentage_YoY', 'Surprise Percentage']
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

	const table = new TableHandler<RowData>(tableData, { rowsPerPage: 20 });
</script>

<div class="container mx-auto p-4">
	<h2 class="mb-4 text-2xl font-bold">Financial Metrics (Year over Year)</h2>

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
