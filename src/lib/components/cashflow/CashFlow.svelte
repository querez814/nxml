<script lang="ts">
	let {
		fiscalDateEnding,
		operatingCashflow,
		capitalExpenditures,
		freeCashFlow,
		changeInInventory,
		changeInReceivables,
		cashFlowFromInvestment,
		cashFlowfromFinancing,
		paymentsForRepurchaseOfCommonStock,
		paymentsForRepurchaseOfEquity,
		dividendPayout
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
						<th class="px-4 py-3">Operating Cash Flow (M)</th>
						<th class="px-4 py-3">CapEx (M)</th>
						<th class="px-4 py-3"> Free Cash Flow (M)</th>
						<th class="px-4 py-3">Change In Inventory (M)</th>
						<th class="px-4 py-3">Change In AR (M)</th>
						<th class="px-4 py-3">CF From Investment (M)</th>
						<th class="px-4 py-3">CF From Financing (M)</th>
						<th class="px-4 py-3">Payments for Stock Buybacks (M)</th>
						<th class="px-4 py-3">Dividend Payout (M)</th>
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
						<td class="px-4 py-3">{operatingCashflow}</td>
						<td class="px-4 py-3">{capitalExpenditures}</td>
						<td class="px-4 py-3">{freeCashFlow}</td>
						<td class="px-4 py-3">{changeInInventory}</td>
						<td class="px-4 py-3">{changeInReceivables}</td>
						<td class="px-4 py-3">{cashFlowFromInvestment}</td>
						<td class="px-4 py-3">{cashFlowfromFinancing}</td>
						<td class="px-4 py-3">{paymentsForRepurchaseOfCommonStock}</td>
						<td class="px-4 py-3">{dividendPayout}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</div>
