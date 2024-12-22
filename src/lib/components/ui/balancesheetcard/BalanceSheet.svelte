<script lang="ts">
	let {
		fiscalDateEnding,
		totalCurrentAssets,
		totalAssets,
		totalCurrentLiabilities,
		totalLiabilities,
		working_capital,
		totalShareholderEquity,
		commonStockSharesOutstanding,
		cashAndCashEquivalentsAtCarryingValue,
		inventory,
		propertyPlantEquipment,
		deferredRevenue,
		currentDebt
	} = $props();
</script>

<div class="mx-auto w-full max-w-screen-2xl px-6 py-12">
	<!-- A 'card-like' container with gradient background, ring, and shadow -->
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
		<!-- Title & subtitle -->
		<h2 class="mb-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">
			Most Recent Income Statement
		</h2>
		<p class="mb-8 text-slate-300">Key figures from the latest quarterly report</p>

		<!-- Table wrapper: handle overflow if columns exceed screen width -->
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
				<!-- Table Head -->
				<thead>
					<tr class="bg-slate-700/80 text-sm uppercase md:text-base">
						<th class="px-4 py-3">Fiscal Date Ending</th>
						<th class="px-4 py-3">Current Assets (M)</th>
						<th class="px-4 py-3">Cash And Cash Eq (M)</th>
						<th class="px-4 py-3"> Inventory (M)</th>
						<th class="px-4 py-3">PPE (M)</th>
						<th class="px-4 py-3">Total Assets (M)</th>
						<th class="px-4 py-3">Current Liabilities (M)</th>
						<th class="px-4 py-3">Total Liabilties (M)</th>
						<th class="px-4 py-3">Current Debt (M)</th>
						<th class="px-4 py-3">Deferred Revenue (M)</th>
						<th class="px-4 py-3">Working Capital (M)</th>
						<th class="px-4 py-3">Shareholder Equity (M)</th>
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
						<td class="px-4 py-3">{totalCurrentAssets}</td>
						<td class="px-4 py-3">{cashAndCashEquivalentsAtCarryingValue}</td>
						<td class="px-4 py-3">{inventory}</td>
						<td class="px-4 py-3">{propertyPlantEquipment}</td>
						<td class="px-4 py-3">{totalAssets}</td>
						<td class="px-4 py-3">{totalCurrentLiabilities}</td>
						<td class="px-4 py-3">{totalLiabilities}</td>
						<td class="px-4 py-3">{currentDebt}</td>
						<td class="px-4 py-3">{deferredRevenue}</td>
						<td class="px-4 py-3">{working_capital}</td>
						<td class="px-4 py-3">{totalShareholderEquity}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</div>
