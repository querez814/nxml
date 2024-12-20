<script lang="ts">
	export let data: { balancesheet_qoq_data?: any };

	const bs_qoq_data = data?.balancesheet_qoq_data || [];

	const formattedData = Array.isArray(bs_qoq_data)
		? bs_qoq_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				totalCurrentAssets_QoQ: entry.totalCurrentAssets_QoQ || '0%',
				totalAssets_QoQ: entry.totalAssets_QoQ || '0%',
				totalCurrentLiabilities_QoQ: entry.totalCurrentLiabilities_QoQ || '0%',
				totalLiabilities_QoQ: entry.totalLiabilities_QoQ || '0%',
				working_capital_QoQ: entry.working_capital_QoQ || '0%',
				totalShareholderEquity_QoQ: entry.totalShareholderEquity_QoQ || '0%',
				commonStockSharesOutstanding_QoQ: entry.commonStockSharesOutstanding_QoQ || '0%',
				cashAndCashEquivalentsAtCarryingValue_QoQ:
					entry.cashAndCashEquivalentsAtCarryingValue_QoQ || '0%',
				inventory_QoQ: entry.inventory_QoQ || '0%',
				propertyPlantEquipment_QoQ: entry.propertyPlantEquipment_QoQ || '0%',
				deferredRevenue_QoQ: entry.deferredRevenue_QoQ || '0%',
				currentDebt_QoQ: entry.currentDebt_QoQ || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Balance Sheet Statement YoY</h1>

	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Total Current Assets YoY</th>
						<th class="border px-4 py-3">Total Assets YoY</th>
						<th class="border px-4 py-3">Total Current Liabilities YoY</th>
						<th class="border px-4 py-3">Total Liabilities YoY</th>
						<th class="border px-4 py-3">Working Capital YoY</th>
						<th class="border px-4 py-3">Total Shareholder Equity YoY</th>
						<th class="border px-4 py-3">Common Stock Shares Outstanding YoY</th>
						<th class="border px-4 py-3">Cash and Cash Equivalents YoY</th>
						<th class="border px-4 py-3">Inventory YoY</th>
						<th class="border px-4 py-3">Property, Plant, and Equipment YoY</th>
						<th class="border px-4 py-3">Deferred Revenue YoY</th>
						<th class="border px-4 py-3">Current Debt YoY</th>
					</tr>
				</thead>
				<tbody class="text-gray-700">
					{#each formattedData as entry, i}
						<tr
							class="{i % 2 === 0
								? 'bg-gray-50'
								: 'bg-white'} transition duration-200 hover:bg-yellow-100"
						>
							<td class="border px-4 py-3 text-center">{entry.fiscalDateEnding}</td>
							<td class="border px-4 py-3 text-right">{entry.totalCurrentAssets_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.totalAssets_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.totalCurrentLiabilities_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.totalLiabilities_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.working_capital_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.totalShareholderEquity_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.commonStockSharesOutstanding_QoQ}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.cashAndCashEquivalentsAtCarryingValue_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.inventory_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.propertyPlantEquipment_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.deferredRevenue_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.currentDebt_QoQ}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
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
