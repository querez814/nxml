<script lang="ts">
	export let data: { bs_yoy_data?: any };

	const bs_yoy_data = data?.bs_yoy_data || [];

	const formattedData = Array.isArray(bs_yoy_data)
		? bs_yoy_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				totalCurrentAssets_YoY: entry.totalCurrentAssets_YoY || '0%',
				totalAssets_YoY: entry.totalAssets_YoY || '0%',
				totalCurrentLiabilities_YoY: entry.totalCurrentLiabilities_YoY || '0%',
				totalLiabilities_YoY: entry.totalLiabilities_YoY || '0%',
				working_capital_YoY: entry.working_capital_YoY || '0%',
				totalShareholderEquity_YoY: entry.totalShareholderEquity_YoY || '0%',
				commonStockSharesOutstanding_YoY: entry.commonStockSharesOutstanding_YoY || '0%',
				cashAndCashEquivalentsAtCarryingValue_YoY:
					entry.cashAndCashEquivalentsAtCarryingValue_YoY || '0%',
				inventory_YoY: entry.inventory_YoY || '0%',
				propertyPlantEquipment_YoY: entry.propertyPlantEquipment_YoY || '0%',
				deferredRevenue_YoY: entry.deferredRevenue_YoY || '0%',
				currentDebt_YoY: entry.currentDebt_YoY || '0%'
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
							<td class="border px-4 py-3 text-right">{entry.totalCurrentAssets_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.totalAssets_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.totalCurrentLiabilities_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.totalLiabilities_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.working_capital_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.totalShareholderEquity_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.commonStockSharesOutstanding_YoY}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.cashAndCashEquivalentsAtCarryingValue_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.inventory_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.propertyPlantEquipment_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.deferredRevenue_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.currentDebt_YoY}</td>
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
