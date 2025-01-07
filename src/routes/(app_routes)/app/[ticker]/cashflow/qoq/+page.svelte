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
		['operatingCashflow_QoQ', 'Operating Cash Flow (q/q)'],
		['changeInOperatingLiabilities_QoQ', 'Change In Operating Liabilities (q/q)'],
		['changeInOperatingAssets_QoQ', 'Change In Operating Assets (q/q)'],
		['depreciationDepletionAndAmortization_QoQ', 'D&A (q/q)'],
		['capitalExpenditures_QoQ', 'Capital Expenditures (q/q)'],
		['changeInReceivables_QoQ', 'Change In Receivables (q/q)'],
		['changeInInventory_QoQ', 'Change in Inventory (q/q)'],
		['cashflowFromInvestment_QoQ', 'CF From Investment (q/q)'],
		['cashflowFromFinancing_QoQ', 'CF From Financing (q/q)'],
		['dividendPayout_QoQ', 'Dividend Payout (q/q)'],
		['paymentsForRepurchaseOfCommonStock_QoQ', 'Stock Repurchase (q/q)'],
		['netIncome_QoQ', 'Net Income (q/q)'],
		['freeCashFlow_QoQ', 'Free Cash Flow (q/q)']
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
	<h2 class="mb-4 text-2xl font-bold">Cash Flow (q/q)</h2>

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
