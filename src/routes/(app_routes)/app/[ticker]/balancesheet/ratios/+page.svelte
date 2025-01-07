<script lang="ts">
	import type { PageData } from './$types';
	import { TableHandler, Datatable, ThSort, ThFilter } from '@vincjo/datatables';

	interface RowData {
		metric: string;
		[key: string]: string | number;
	}

	type Field<T> = keyof T;

	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];

	const metricsMap = new Map([
		['current_ratio', 'Current Ratio'],
		['quick_ratio', 'Quick Ratio'],
		['cash_ratio', 'Cash Ratio'],
		['debt_to_equity_ratio', 'Debt To Equity Ratio'],
		['debt_to_asset_ratio', 'Debt to Asset Ratio'],
		['book_value_per_share', 'Book Value Per Share']
	]);

	const tableData: RowData[] = Array.from(metricsMap.entries()).map(([key, metric]) => ({
		metric,
		...quarters.reduce(
			(acc, quarter) => ({
				...acc,
				[quarter.fiscalDateEnding]: quarter[key] || 'N/A'
			}),
			{} as Record<string, string | number>
		)
	}));

	const table = new TableHandler<RowData>(tableData, { rowsPerPage: 20 });

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short'
		});
	}

	function formatValue(value: string | number): string {
		if (typeof value === 'number') {
			return value.toLocaleString('en-US', {
				maximumFractionDigits: 2
			});
		}
		return String(value);
	}

	function getValueColor(value: string | number): string {
		if (typeof value === 'number') {
			return value < 0 ? 'text-red-500' : 'text-emerald-400';
		}
		return 'text-gray-300';
	}
</script>

<div class="mx-auto w-full max-w-screen-2xl p-6">
	<div class="mb-6 flex items-center justify-between">
		<h2 class="text-2xl font-medium tracking-wide text-emerald-400">
			Quarterly Balance Sheet Ratios
		</h2>
		<div class="text-sm text-gray-400">
			Last updated: {formatDate(quarters[0]?.fiscalDateEnding || '')}
		</div>
	</div>

	<div class="rounded-lg bg-gray-900/50 backdrop-blur-sm">
		{#if quarters.length > 0}
			<div class="overflow-x-auto">
				<Datatable basic {table}>
					<table class="w-full table-auto border-collapse text-left">
						<thead>
							<tr class="border-b border-gray-800">
								<th class="bg-gray-900/80 p-4 text-sm font-medium text-emerald-400"> Metric </th>
								{#each quarters as quarter}
									<th class="bg-gray-900/80 p-4 text-right text-sm font-medium text-emerald-400">
										{formatDate(quarter.fiscalDateEnding)}
									</th>
								{/each}
							</tr>
							<tr class="border-b border-gray-800">
								<th class="p-2">
									<input
										type="text"
										placeholder="Filter metrics..."
										class="w-full rounded bg-gray-800 px-3 py-1 text-sm text-gray-300 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-emerald-500"
									/>
								</th>
								{#each quarters as quarter}
									<th class="p-2">
										<input
											type="text"
											placeholder="Filter..."
											class="w-full rounded bg-gray-800 px-3 py-1 text-right text-sm text-gray-300 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-emerald-500"
										/>
									</th>
								{/each}
							</tr>
						</thead>
						<tbody>
							{#each table.rows as row}
								<tr class="border-b border-gray-800/50 transition-colors hover:bg-gray-800/30">
									<td class="p-4 font-medium text-gray-300">
										{row.metric}
									</td>
									{#each quarters as quarter}
										<td class="p-4 text-right">
											<span class={getValueColor(row[quarter.fiscalDateEnding])}>
												{formatValue(row[quarter.fiscalDateEnding])}
											</span>
										</td>
									{/each}
								</tr>
							{/each}
						</tbody>
					</table>
				</Datatable>
			</div>
		{:else}
			<div class="flex h-48 items-center justify-center">
				<p class="text-gray-500">No quarterly data available</p>
			</div>
		{/if}
	</div>
</div>
