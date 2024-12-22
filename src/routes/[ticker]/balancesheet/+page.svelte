<script lang="ts">
	import BalanceSheet from '$lib/components/ui/balancesheetcard/BalanceSheet.svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
	const singlequarter = quarters[0];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-6 py-12">
	<!-- Title -->
	<h1 class="mb-8 text-center text-4xl font-bold text-slate-100">Balance Sheet Data</h1>

	<!-- Render each quarter's balance sheet -->

	<BalanceSheet
		fiscalDateEnding={singlequarter.fiscalDateEnding}
		totalCurrentAssets={singlequarter.totalCurrentAssets}
		totalAssets={singlequarter.totalAssets}
		totalCurrentLiabilities={singlequarter.totalCurrentLiabilities}
		totalLiabilities={singlequarter.totalLiabilities}
		working_capital={singlequarter.working_capital}
		totalShareholderEquity={singlequarter.totalShareholderEquity}
		commonStockSharesOutstanding={singlequarter.commonStockSharesOutstanding}
		cashAndCashEquivalentsAtCarryingValue={singlequarter.cashAndCashEquivalentsAtCarryingValue}
		inventory={singlequarter.inventory}
		propertyPlantEquipment={singlequarter.propertyPlantEquipment}
		deferredRevenue={singlequarter.deferredRevenue}
		currentDebt={singlequarter.currentDebt}
	/>
</div>
