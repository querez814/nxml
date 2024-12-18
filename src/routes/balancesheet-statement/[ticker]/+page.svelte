<script lang="ts">
	// Access the data returned from `+page.ts`
	export let data;

	// Destructure the income_data from data
	const { balancesheet_data } = data;

	// Helper function to format numbers into millions with commas
	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};
</script>

<main class="bg-gray-100 p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">
		Quarterly Balance Sheet Statements
	</h1>
	<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
		<table class="auto table w-full border-collapse text-sm">
			<thead class="bg-yellow-80 sticky top-0 text-white">
				<tr>
					<th class="border px-4 py-3">Fiscal Date Ending</th>
					<th class="border px-4 py-3">Current Assets</th>
					<th class="border px-4 py-3">Total Assets</th>
					<th class="border px-4 py-3">Current Liabilities</th>
					<th class="border px-4 py-3">Total Liabilities</th>
					<th class="border px-4 py-3">Working Capital</th>
					<th class="border px-4 py-3">Shareholder Equity</th>
					<th class="border px-4 py-3">Shares Outstanding</th>
					<th class="border px-4 py-3">Cash and Cash Equivalents</th>
					<th class="border px-4 py-3">Inventory</th>
					<th class="border px-4 py-3">Property Plant and Equipment</th>
					<th class="border px-4 py-3">Deferred Revenue</th>
					<th class="border px-4 py-3">Current Debt</th>
				</tr>
			</thead>

			<tbody class="text-gray-700">
				{#each balancesheet_data as entry, i}
					<tr
						class="{i % 2 === 0
							? 'bg-gray-50'
							: 'bg-white'} transition duration-200 hover:bg-yellow-100"
					>
						<td class="border px-4 py-3 text-center">{entry.fiscalDateEnding}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalCurrentAssets)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalAssets)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.totalCurrentLiabilities)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalLiabilities)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.working_capital)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.totalShareholderEquity)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.commonStockSharesOutstanding)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.cashAndCashEquivalentsAtCarryingValue)}</td
						>

						<td class="border px-4 py-3 text-right">{formatToMillions(entry.inventory)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.propertyPlantEquipment)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.deferredRevenue)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.currentDebt)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</main>

<style>
	table {
		font-family: Arial, sans-serif;
	}
	th,
	td {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8px;
	}
</style>
