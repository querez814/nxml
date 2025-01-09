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
	import { TableHandler, Datatable } from '@vincjo/datatables';
</script>
