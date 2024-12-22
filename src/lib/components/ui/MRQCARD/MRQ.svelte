<script lang="ts">
	let {
		fiscalDateEnding,
		grossProfit,
		totalRevenue,
		costOfRevenue,
		costofGoodsAndServicesSold,
		operatingIncome,
		sellingGeneralAndAdministrative,
		researchAndDevelopment,
		operatingExpenses,
		interestIncome,
		interestExpense,
		incomeBeforeTax,
		incomeTaxExpense,
		interestAndDebtExpense,
		ebit,
		ebitda,
		netIncome,
		reportedEPS,
		estimatedEPS,
		surprise,
		surprisePercentage
	} = $props();
</script>

<div class="mx-auto w-full max-w-screen-2xl px-6 py-12">
	<div
		class="
		rounded-xl
		bg-gradient-to-br
		from-slate-800
		to-slate-900
		p-8
		shadow-xl
		ring-1
		ring-slate-700
	"
	>
		<h2 class="mb-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">
			Most Recent Income Statement
		</h2>
		<p class="mb-8 text-slate-300">Key figures from the latest quarterly report</p>

		<div class="overflow-x-auto rounded-lg">
			<table
				class="
					w-full
					table-auto
					border-separate
					border-spacing-x-3
					border-spacing-y-3
					text-left
					text-slate-100
				"
			>
				<thead>
					<tr class="bg-slate-700/80 text-sm uppercase md:text-base">
						<th class="px-4 py-3">Fiscal Date Ending</th>
						<th class="px-4 py-3">Total Revenue (M)</th>
						<th class="px-4 py-3">Cost of Revenue (M)</th>
						<th class="px-4 py-3">Cost of Goods and Services Sold (M)</th>
						<th class="px-4 py-3">Gross Profit (M)</th>

						<th class="px-4 py-3">Selling, General &amp; Admin (M)</th>
						<th class="px-4 py-3">Research &amp; Development (M)</th>
						<th class="px-4 py-3">Operating Expenses (M)</th>
						<th class="px-4 py-3">EBITDA (M)</th>
						<th class="px-4 py-3">Operating Income (M)</th>
						<th class="px-4 py-3">Interest Income (M)</th>
						<th class="px-4 py-3">Interest Expense (M)</th>
						<th class="px-4 py-3">Income Before Tax (M)</th>
						<th class="px-4 py-3">Income Tax Expense (M)</th>
						<th class="px-4 py-3">Interest &amp; Debt Expense (M)</th>

						<th class="px-4 py-3">Net Income (M)</th>
						<th class="px-4 py-3">Reported EPS</th>
						<th class="px-4 py-3">Estimated EPS</th>
						<th class="px-4 py-3">Surprise</th>
						<th class="px-4 py-3">Surprise %</th>
					</tr>
				</thead>

				<tbody>
					<tr
						class="
							rounded-md
							bg-slate-800/60
							transition-colors
							hover:bg-slate-700/70
						"
					>
						<td class="px-4 py-3">{fiscalDateEnding}</td>
						<td class="px-4 py-3">{totalRevenue}</td>
						<td class="px-4 py-3">{costOfRevenue}</td>
						<td class="px-4 py-3">{costofGoodsAndServicesSold}</td>
						<td class="px-4 py-3">{grossProfit}</td>
						<td class="px-4 py-3">{sellingGeneralAndAdministrative}</td>
						<td class="px-4 py-3">{researchAndDevelopment}</td>
						<td class="px-4 py-3">{operatingExpenses}</td>
						<td class="px-4 py-3">{ebitda}</td>
						<td class="px-4 py-3">{operatingIncome}</td>
						<td class="px-4 py-3">{interestIncome}</td>
						<td class="px-4 py-3">{interestExpense}</td>
						<td class="px-4 py-3">{incomeBeforeTax}</td>
						<td class="px-4 py-3">{incomeTaxExpense}</td>
						<td class="px-4 py-3">{interestAndDebtExpense}</td>

						<td class="px-4 py-3">{netIncome}</td>
						<td class="px-4 py-3">{reportedEPS}</td>
						<td class="px-4 py-3">{estimatedEPS}</td>
						<td class="px-4 py-3">{surprise}</td>
						<td class="px-4 py-3">{surprisePercentage}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</div>
