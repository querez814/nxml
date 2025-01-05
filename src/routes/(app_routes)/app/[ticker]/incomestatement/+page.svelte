<script lang="ts">
	import { School } from 'lucide-svelte';
	import IncomeStatementTutorial from '$lib/components/tutorial/incomestatement/IncomeStatementTutorial.svelte';
	import Mrq from '$lib/components/ui/MRQCARD/MRQ.svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	let new_data = data.data[0];
</script>

<div class="income-statement">
	<section>
		<Mrq
			fiscalDateEnding={new_data.fiscalDateEnding}
			totalRevenue={new_data.totalRevenue}
			grossProfit={new_data.grossProfit}
			costOfRevenue={new_data.costOfRevenue}
			costofGoodsAndServicesSold={new_data.costofGoodsAndServicesSold}
			operatingIncome={new_data.operatingIncome}
			sellingGeneralAndAdministrative={new_data.sellingGeneralAndAdministrative}
			researchAndDevelopment={new_data.researchAndDevelopment}
			operatingExpenses={new_data.operatingExpenses}
			interestIncome={new_data.interestIncome}
			interestExpense={new_data.interestExpense}
			incomeBeforeTax={new_data.incomeBeforeTax}
			incomeTaxExpense={new_data.incomeTaxExpense}
			interestAndDebtExpense={new_data.interestAndDebtExpense}
			ebit={new_data.ebit}
			ebitda={new_data.ebitda}
			netIncome={new_data.netIncome}
			reportedEPS={new_data.reportedEPS}
			estimatedEPS={new_data.estimatedEPS}
			surprise={new_data.surprise}
			surprisePercentage={new_data.surprisePercentage}
		/>
	</section>
</div>
