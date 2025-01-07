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
		['operatingCashflow_YoY', 'Operating Cash Flow'],
		['changeInOperatingLiabilities_YoY', 'Change In Operating Liabilities'],
		['changeInOperatingAssets_YoY', 'Change In Operating Assets'],
		['depreciationDepletionAndAmortization_YoY', 'D&A'],
		['capitalExpenditures_YoY', 'Capital Expenditures'],
		['changeInReceivables_YoY', 'Change In Receivables'],
		['changeInInventory_YoY', 'Change in Inventory'],
		['cashflowFromInvestment_YoY', 'CF From Investment'],
		['cashflowFromFinancing_YoY', 'CF From Financing'],
		['dividendPayout_YoY', 'Dividend Payout'],
		['paymentsForRepurchaseOfCommonStock_YoY', 'Stock Repurchase'],
		['netIncome_YoY', 'Net Income'],
		['freeCashFlow_YoY', 'Free Cash Flow']
	]);

	const tableData: RowData[] = Array.from(metricsMap.entries()).map(([key, metric]) => ({
		metric,
		...data.quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[quarter.fiscalDateEnding]:
					quarter[key] === 'inf%' || quarter[key] === '-inf%' ? 'N/A' : quarter[key] || '0%'
			}),
			{} as Record<string, string>
		)
	}));

	const table = new TableHandler<RowData>(tableData, { rowsPerPage: 20 });
</script>

<div class="container mx-auto p-4">
	<h2 class="mb-4 text-2xl font-bold">Cash Flow (y/y)</h2>

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
					<tr class="hover:bg-slate-800">
						<td class="border-b border-slate-700 p-2">{row.metric}</td>
						{#each data.quarters as quarter}
							<td
								class="border-b border-slate-700 p-2 text-right {row[
									quarter.fiscalDateEnding
								].startsWith('-')
									? 'text-red-500'
									: row[quarter.fiscalDateEnding] === 'N/A'
										? 'text-gray-500'
										: 'text-green-500'}"
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
