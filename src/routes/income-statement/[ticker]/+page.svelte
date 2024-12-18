<script lang="ts">
	// Access the data returned from `+page.ts`
	export let data;

	// Destructure the income_data from data
	const { income_data } = data;

	// Helper function to format numbers into millions with commas
	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};
</script>

<main class="bg-gray-100 p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">Quarterly Financial Metrics</h1>

	<!-- Table Container -->
	<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
		<table class="w-full table-auto border-collapse text-sm">
			<!-- Table Header -->
			<thead class="sticky top-0 bg-yellow-800 text-white">
				<tr>
					<th class="border px-4 py-3">Fiscal Date Ending</th>
					<th class="border px-4 py-3">Gross Profit</th>
					<th class="border px-4 py-3">Total Revenue</th>
					<th class="border px-4 py-3">Cost of Revenue</th>
					<th class="border px-4 py-3">Operating Income</th>
					<th class="border px-4 py-3">SG&A</th>
					<th class="border px-4 py-3">R&D</th>
					<th class="border px-4 py-3">Operating Expenses</th>
					<th class="border px-4 py-3">Interest Income</th>
					<th class="border px-4 py-3">Interest Expense</th>
					<th class="border px-4 py-3">Income Before Tax</th>
					<th class="border px-4 py-3">Income Tax Expense</th>
					<th class="border px-4 py-3">EBIT</th>
					<th class="border px-4 py-3">EBITDA</th>
					<th class="border px-4 py-3">Net Income</th>
				</tr>
			</thead>

			<!-- Table Body -->
			<tbody class="text-gray-700">
				{#each income_data as entry, i}
					<tr
						class="{i % 2 === 0
							? 'bg-gray-50'
							: 'bg-white'} transition duration-200 hover:bg-yellow-100"
					>
						<td class="border px-4 py-3 text-center">{entry.fiscalDateEnding}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.grossProfit)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalRevenue)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.costOfRevenue)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.operatingIncome)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.sellingGeneralAndAdministrative)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.researchAndDevelopment)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.operatingExpenses)}</td>
						<td class="border px-4 py-3 text-right">{entry.interestIncome || '-'}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.interestExpense)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.incomeBeforeTax)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.incomeTaxExpense)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.ebit)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.ebitda)}</td>
						<td class="border px-4 py-3 text-right font-semibold"
							>{formatToMillions(entry.netIncome)}</td
						>
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
		white-space: nowrap;
	}
</style>
