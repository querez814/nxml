<script lang="ts">
	import CashFlow from '$lib/components/cashflow/CashFlow.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let quarters_ = data.quarters || [];
	let recent_quarter = quarters_[0];
</script>

<div class="cash-flow">
	<CashFlow
		fiscalDateEnding={recent_quarter.fiscalDateEnding}
		operatingCashflow={recent_quarter.operatingCashflow}
		capitalExpenditures={recent_quarter.capitalExpenditures}
		freeCashFlow={recent_quarter.freeCashFlow}
		changeInInventory={recent_quarter.changeInInventory}
		changeInReceivables={recent_quarter.changeInReceivables}
		cashFlowFromInvestment={recent_quarter.cashflowFromInvestment}
		cashFlowfromFinancing={recent_quarter.cashflowFromFinancing}
		paymentsForRepurchaseOfCommonStock={recent_quarter.paymentsForRepurchaseOfCommonStock}
		paymentsForRepurchaseOfEquity={recent_quarter.paymentsForRepurchaseOfEquity}
		dividendPayout={recent_quarter.dividendPayout}
	/>
</div>
