<script lang="ts">
	export let data: { cashflow_qoq_data?: any };

	const cashflow_qoq_data = data?.cashflow_qoq_data || [];

	const formattedData = Array.isArray(cashflow_qoq_data)
		? cashflow_qoq_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				operatingCashflow_QoQ: entry.operatingCashflow_QoQ || '0%',
				paymentsForOperatingActivities_QoQ: entry.paymentsForOperatingActivities_QoQ || '0%',
				proceedsFromOperatingActivities_QoQ: entry.proceedsFromOperatingActivities_QoQ || '0%',
				changeInOperatingLiabilities_QoQ: entry.changeInOperatingLiabilities_QoQ || '0%',
				changeInOperatingAssets_QoQ: entry.changeInOperatingAssets_QoQ || '0%',
				depreciationDepletionAndAmortization_QoQ:
					entry.depreciationDepletionAndAmortization_QoQ || '0%',
				capitalExpenditures_QoQ: entry.capitalExpenditures_QoQ || '0%',
				changeInReceivables_QoQ: entry.changeInReceivables_QoQ || '0%',
				changeInInventory_QoQ: entry.changeInInventory_QoQ || '0%',
				profitLoss_QoQ: entry.profitLoss_QoQ || '0%',
				cashflowFromInvestment_QoQ: entry.cashflowFromInvestment_QoQ || '0%',
				cashflowFromFinancing_QoQ: entry.cashflowFromFinancing_QoQ || '0%',
				proceedsFromRepaymentsOfShortTermDebt_QoQ:
					entry.proceedsFromRepaymentsOfShortTermDebt_QoQ || '0%',
				paymentsForRepurchaseOfCommonStock_QoQ:
					entry.paymentsForRepurchaseOfCommonStock_QoQ || '0%',
				paymentsForRepurchaseOfEquity_QoQ: entry.paymentsForRepurchaseOfEquity_QoQ || '0%',
				paymentsForRepurchaseOfPreferredStock_QoQ:
					entry.paymentsForRepurchaseOfPreferredStock_QoQ || '0%',
				dividendPayout_QoQ: entry.dividendPayout_QoQ || '0%',
				dividendPayoutCommonStock_QoQ: entry.dividendPayoutCommonStock_QoQ || '0%',
				dividendPayoutPreferredStock_QoQ: entry.dividendPayoutPreferredStock_QoQ || '0%',
				proceedsFromRepurchaseOfEquity_QoQ: entry.proceedsFromRepurchaseOfEquity_QoQ || '0%',
				netIncome_QoQ: entry.netIncome_QoQ || '0%',
				freeCashFlow_QoQ: entry.freeCashFlow_QoQ || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Cash Flow Statement QoQ</h1>

	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Operating Cashflow QoQ</th>
						<th class="border px-4 py-3">Payments for Operating Activities QoQ</th>
						<th class="border px-4 py-3">Proceeds from Operating Activities QoQ</th>
						<th class="border px-4 py-3">Change in Operating Liabilities QoQ</th>
						<th class="border px-4 py-3">Change in Operating Assets QoQ</th>
						<th class="border px-4 py-3">Depreciation, Depletion, and Amortization QoQ</th>
						<th class="border px-4 py-3">Capital Expenditures QoQ</th>
						<th class="border px-4 py-3">Change in Receivables QoQ</th>
						<th class="border px-4 py-3">Change in Inventory QoQ</th>
						<th class="border px-4 py-3">Profit/Loss QoQ</th>
						<th class="border px-4 py-3">Cashflow from Investment QoQ</th>
						<th class="border px-4 py-3">Cashflow from Financing QoQ</th>
						<th class="border px-4 py-3">Proceeds from Repayments of Short-Term Debt QoQ</th>
						<th class="border px-4 py-3">Payments for Repurchase of Common Stock QoQ</th>
						<th class="border px-4 py-3">Payments for Repurchase of Equity QoQ</th>
						<th class="border px-4 py-3">Payments for Repurchase of Preferred Stock QoQ</th>
						<th class="border px-4 py-3">Dividend Payout QoQ</th>
						<th class="border px-4 py-3">Dividend Payout (Common Stock) QoQ</th>
						<th class="border px-4 py-3">Dividend Payout (Preferred Stock) QoQ</th>
						<th class="border px-4 py-3">Proceeds from Repurchase of Equity QoQ</th>
						<th class="border px-4 py-3">Net Income QoQ</th>
						<th class="border px-4 py-3">Free Cash Flow QoQ</th>
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
							<td class="border px-4 py-3 text-right">{entry.operatingCashflow_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.paymentsForOperatingActivities_QoQ}</td
							>
							<td class="border px-4 py-3 text-right"
								>{entry.proceedsFromOperatingActivities_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.changeInOperatingLiabilities_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInOperatingAssets_QoQ}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.depreciationDepletionAndAmortization_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.capitalExpenditures_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInReceivables_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInInventory_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.profitLoss_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.cashflowFromInvestment_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.cashflowFromFinancing_QoQ}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.proceedsFromRepaymentsOfShortTermDebt_QoQ}</td
							>
							<td class="border px-4 py-3 text-right"
								>{entry.paymentsForRepurchaseOfCommonStock_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.paymentsForRepurchaseOfEquity_QoQ}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.paymentsForRepurchaseOfPreferredStock_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.dividendPayout_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.dividendPayoutCommonStock_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.dividendPayoutPreferredStock_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.proceedsFromRepurchaseOfEquity_QoQ}</td
							>
							<td class="border px-4 py-3 text-right">{entry.netIncome_QoQ}</td>
							<td class="border px-4 py-3 text-right">{entry.freeCashFlow_QoQ}</td>
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
