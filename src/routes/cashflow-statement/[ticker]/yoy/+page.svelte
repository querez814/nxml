<script lang="ts">
	export let data: { cashflow_yoy_data?: any };

	// Safely handle undefined or null data
	const cashflow_yoy_data = data?.cashflow_yoy_data || [];

	// Ensure the data is properly formatted and cleaned
	const formattedData = Array.isArray(cashflow_yoy_data)
		? cashflow_yoy_data.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				operatingCashflow_YoY: entry.operatingCashflow_YoY || '0%',
				paymentsForOperatingActivities_YoY: entry.paymentsForOperatingActivities_YoY || '0%',
				proceedsFromOperatingActivities_YoY: entry.proceedsFromOperatingActivities_YoY || '0%',
				changeInOperatingLiabilities_YoY: entry.changeInOperatingLiabilities_YoY || '0%',
				changeInOperatingAssets_YoY: entry.changeInOperatingAssets_YoY || '0%',
				depreciationDepletionAndAmortization_YoY:
					entry.depreciationDepletionAndAmortization_YoY || '0%',
				capitalExpenditures_YoY: entry.capitalExpenditures_YoY || '0%',
				changeInReceivables_YoY: entry.changeInReceivables_YoY || '0%',
				changeInInventory_YoY: entry.changeInInventory_YoY || '0%',
				profitLoss_YoY: entry.profitLoss_YoY || '0%',
				cashflowFromInvestment_YoY: entry.cashflowFromInvestment_YoY || '0%',
				cashflowFromFinancing_YoY: entry.cashflowFromFinancing_YoY || '0%',
				proceedsFromRepaymentsOfShortTermDebt_YoY:
					entry.proceedsFromRepaymentsOfShortTermDebt_YoY || '0%',
				paymentsForRepurchaseOfCommonStock_YoY:
					entry.paymentsForRepurchaseOfCommonStock_YoY || '0%',
				paymentsForRepurchaseOfEquity_YoY: entry.paymentsForRepurchaseOfEquity_YoY || '0%',
				paymentsForRepurchaseOfPreferredStock_YoY:
					entry.paymentsForRepurchaseOfPreferredStock_YoY || '0%',
				dividendPayout_YoY: entry.dividendPayout_YoY || '0%',
				dividendPayoutCommonStock_YoY: entry.dividendPayoutCommonStock_YoY || '0%',
				dividendPayoutPreferredStock_YoY: entry.dividendPayoutPreferredStock_YoY || '0%',
				proceedsFromRepurchaseOfEquity_YoY: entry.proceedsFromRepurchaseOfEquity_YoY || '0%',
				netIncome_YoY: entry.netIncome_YoY || '0%',
				freeCashFlow_YoY: entry.freeCashFlow_YoY || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Cash Flow Statement YoY</h1>

	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Operating Cashflow YoY</th>
						<th class="border px-4 py-3">Payments for Operating Activities YoY</th>
						<th class="border px-4 py-3">Proceeds from Operating Activities YoY</th>
						<th class="border px-4 py-3">Change in Operating Liabilities YoY</th>
						<th class="border px-4 py-3">Change in Operating Assets YoY</th>
						<th class="border px-4 py-3">Depreciation, Depletion, and Amortization YoY</th>
						<th class="border px-4 py-3">Capital Expenditures YoY</th>
						<th class="border px-4 py-3">Change in Receivables YoY</th>
						<th class="border px-4 py-3">Change in Inventory YoY</th>
						<th class="border px-4 py-3">Profit/Loss YoY</th>
						<th class="border px-4 py-3">Cashflow from Investment YoY</th>
						<th class="border px-4 py-3">Cashflow from Financing YoY</th>
						<th class="border px-4 py-3">Proceeds from Repayments of Short-Term Debt YoY</th>
						<th class="border px-4 py-3">Payments for Repurchase of Common Stock YoY</th>
						<th class="border px-4 py-3">Payments for Repurchase of Equity YoY</th>
						<th class="border px-4 py-3">Payments for Repurchase of Preferred Stock YoY</th>
						<th class="border px-4 py-3">Dividend Payout YoY</th>
						<th class="border px-4 py-3">Dividend Payout (Common Stock) YoY</th>
						<th class="border px-4 py-3">Dividend Payout (Preferred Stock) YoY</th>
						<th class="border px-4 py-3">Proceeds from Repurchase of Equity YoY</th>
						<th class="border px-4 py-3">Net Income YoY</th>
						<th class="border px-4 py-3">Free Cash Flow YoY</th>
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
							<td class="border px-4 py-3 text-right">{entry.operatingCashflow_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.paymentsForOperatingActivities_YoY}</td
							>
							<td class="border px-4 py-3 text-right"
								>{entry.proceedsFromOperatingActivities_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.changeInOperatingLiabilities_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInOperatingAssets_YoY}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.depreciationDepletionAndAmortization_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.capitalExpenditures_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInReceivables_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.changeInInventory_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.profitLoss_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.cashflowFromInvestment_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.cashflowFromFinancing_YoY}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.proceedsFromRepaymentsOfShortTermDebt_YoY}</td
							>
							<td class="border px-4 py-3 text-right"
								>{entry.paymentsForRepurchaseOfCommonStock_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.paymentsForRepurchaseOfEquity_YoY}</td>
							<td class="border px-4 py-3 text-right"
								>{entry.paymentsForRepurchaseOfPreferredStock_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.dividendPayout_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.dividendPayoutCommonStock_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.dividendPayoutPreferredStock_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.proceedsFromRepurchaseOfEquity_YoY}</td
							>
							<td class="border px-4 py-3 text-right">{entry.netIncome_YoY}</td>
							<td class="border px-4 py-3 text-right">{entry.freeCashFlow_YoY}</td>
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
