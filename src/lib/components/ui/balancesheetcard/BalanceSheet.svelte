<script lang="ts">
	import BalanceSheetTutorial from '$lib/components/tutorial/balancesheet/BalanceSheetTutorial.svelte';
	import { School } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

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

	let showPopup = $state(false);
	let popupRef = $state<HTMLDivElement | null>(null);

	const togglePopup = () => {
		showPopup = !showPopup;
	};

	const handleClickOutside = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		if (showPopup && popupRef && !popupRef.contains(target) && !target.closest('button')) {
			showPopup = false;
		}
	};
</script>

<svelte:window on:click={handleClickOutside} />

<div class="mx-auto w-full max-w-screen-2xl px-6 py-12">
	<Card.Root class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100">
		<Card.Header>
			<button
				onclick={togglePopup}
				class="rounded-full p-2 transition-colors hover:bg-slate-100/10"
				aria-label="Tutorial"
			>
				<School />
			</button>

			{#if showPopup}
				<div
					bind:this={popupRef}
					class="absolute left-4 top-16 z-50 rounded-lg border border-slate-700 bg-slate-900 p-4 shadow-lg"
					role="dialog"
					aria-label="Tutorial popup"
				>
					<BalanceSheetTutorial />
					<button onclick={togglePopup} class="mt-2 text-sm text-slate-400 hover:text-slate-200">
						Close
					</button>
				</div>
			{/if}

			<Card.Title class="text-3xl font-extrabold tracking-tight md:text-4xl">
				Most Recent Balance Sheet
			</Card.Title>
			<Card.Description class="text-slate-300">
				Key figures from the latest quarterly report
			</Card.Description>
		</Card.Header>

		<div class="overflow-x-auto rounded-lg">
			<table
				class="w-full table-auto border-separate border-spacing-x-3 border-spacing-y-3 text-left text-slate-100"
			>
				<thead>
					<tr class="bg-slate-700/80 text-sm uppercase md:text-base">
						<th class="px-4 py-3">Fiscal Date Ending</th>
						<th class="px-4 py-3">Current Assets (M)</th>
						<th class="px-4 py-3">Cash And Cash Eq (M)</th>
						<th class="px-4 py-3">Inventory (M)</th>
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
					<tr class="rounded-md bg-slate-800/60 transition-colors hover:bg-slate-700/70">
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
	</Card.Root>
</div>
