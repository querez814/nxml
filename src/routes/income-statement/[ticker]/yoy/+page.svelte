<script lang="ts">
	export let data: { income_yoy_data?: any };

	const income_yoy_data = data?.income_yoy_data || [];

	const formattedData = Array.isArray(income_yoy_data)
		? income_yoy_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				grossProfit_YoY: entry.grossProfit_YoY || '0%',
				totalRevenue_YoY: entry.totalRevenue_YoY || '0%',
				costOfRevenue_YoY: entry.costOfRevenue_YoY || '0%',
				operatingIncome_YoY: entry.operatingIncome_YoY || '0%',
				sellingGeneralAndAdministrative_YoY: entry.sellingGeneralAndAdministrative_YoY || '0%',
				researchAndDevelopment_YoY: entry.researchAndDevelopment_YoY || '0%',
				operatingExpenses_YoY: entry.operatingExpenses_YoY || '0%',
				interestIncome_YoY: entry.interestIncome_YoY || '0%',
				interestExpense_YoY: entry.interestExpense_YoY || '0%',
				incomeBeforeTax_YoY: entry.incomeBeforeTax_YoY || '0%',
				incomeTaxExpense_YoY: entry.incomeTaxExpense_YoY || '0%',
				ebit_YoY: entry.ebit_YoY || '0%',
				ebitda_YoY: entry.ebitda_YoY || '0%',
				netIncome_YoY: entry.netIncome_YoY || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Income Statement YoY</h1>

	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Gross Profit YoY</th>
						<th class="border px-4 py-3">Total Revenue YoY</th>
						<th class="border px-4 py-3">Cost of Revenue YoY</th>
						<th class="border px-4 py-3">Operating Income YoY</th>
						<th class="border px-4 py-3">SG&A YoY</th>
						<th class="border px-4 py-3">R&D YoY</th>
						<th class="border px-4 py-3">Operating Expenses YoY</th>
						<th class="border px-4 py-3">Interest Income YoY</th>
						<th class="border px-4 py-3">Interest Expense YoY</th>
						<th class="border px-4 py-3">Income Before Tax YoY</th>
						<th class="border px-4 py-3">Income Tax Expense YoY</th>
						<th class="border px-4 py-3">EBIT YoY</th>
						<th class="border px-4 py-3">EBITDA YoY</th>
						<th class="border px-4 py-3">Net Income YoY</th>
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
							<td class="border px-4 py-3 text-right">{entry.grossProfit_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.totalRevenue_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.costOfRevenue_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.operatingIncome_YoY}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.sellingGeneralAndAdministrative_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.researchAndDevelopment_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.operatingExpenses_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.interestIncome_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.interestExpense_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.incomeBeforeTax_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.incomeTaxExpense_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.ebit_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.ebitda_YoY}</td>
							<td class="border px-4 py-3 text-right font-semibold">{entry.netIncome_YoY}</td>
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
