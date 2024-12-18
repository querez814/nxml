<script lang="ts">
	export let data: { income_qoq_data?: any };

	// Safely handle undefined or null data
	const income_qoq_data = data?.income_qoq_data || [];

	// Ensure the data is properly formatted and cleaned
	const formattedData = Array.isArray(income_qoq_data)
		? income_qoq_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				grossProfit_QoQ: entry.grossProfit_QoQ || '0%',
				totalRevenue_QoQ: entry.totalRevenue_QoQ || '0%',
				costOfRevenue_QoQ: entry.costOfRevenue_QoQ || '0%',
				operatingIncome_QoQ: entry.operatingIncome_QoQ || '0%',
				sellingGeneralAndAdministrative_QoQ: entry.sellingGeneralAndAdministrative_QoQ || '0%',
				researchAndDevelopment_QoQ: entry.researchAndDevelopment_QoQ || '0%',
				operatingExpenses_QoQ: entry.operatingExpenses_QoQ || '0%',
				interestIncome_QoQ: entry.interestIncome_QoQ || '0%',
				interestExpense_QoQ: entry.interestExpense_QoQ || '0%',
				incomeBeforeTax_QoQ: entry.incomeBeforeTax_QoQ || '0%',
				incomeTaxExpense_QoQ: entry.incomeTaxExpense_QoQ || '0%',
				ebit_QoQ: entry.ebit_QoQ || '0%',
				ebitda_QoQ: entry.ebitda_QoQ || '0%',
				netIncome_QoQ: entry.netIncome_QoQ || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Income Statement QoQ</h1>

	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Gross Profit QoQ</th>
						<th class="border px-4 py-3">Total Revenue QoQ</th>
						<th class="border px-4 py-3">Cost of Revenue QoQ</th>
						<th class="border px-4 py-3">Operating Income QoQ</th>
						<th class="border px-4 py-3">SG&A QoQ</th>
						<th class="border px-4 py-3">R&D QoQ</th>
						<th class="border px-4 py-3">Operating Expenses QoQ</th>
						<th class="border px-4 py-3">Interest Income QoQ</th>
						<th class="border px-4 py-3">Interest Expense QoQ</th>
						<th class="border px-4 py-3">Income Before Tax QoQ</th>
						<th class="border px-4 py-3">Income Tax Expense QoQ</th>
						<th class="border px-4 py-3">EBIT QoQ</th>
						<th class="border px-4 py-3">EBITDA QoQ</th>
						<th class="border px-4 py-3">Net Income QoQ</th>
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
							<td class="border px-4 py-3 text-right">{entry.grossProfit_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.totalRevenue_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.costOfRevenue_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.operatingIncome_QoQ}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.sellingGeneralAndAdministrative_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.researchAndDevelopment_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.operatingExpenses_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.interestIncome_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.interestExpense_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.incomeBeforeTax_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.incomeTaxExpense_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.ebit_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.ebitda_QoQ}</td>
							<td class="border px-4 py-3 text-right font-semibold">{entry.netIncome_QoQ}</td>
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
