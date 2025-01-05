<script lang="ts">
	import CashFlow from '$lib/components/cashflow/CashFlow.svelte';
	import type { PageData } from './$types';
	import CashFlowTutorial from '$lib/components/tutorial/cashflow/CashFlowTutorial.svelte';
	import { School } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

	let { data }: { data: PageData } = $props();
	let quarters_ = data.quarters || [];
	let recent_quarter = quarters_[0];

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
					<CashFlowTutorial />
					<button onclick={togglePopup} class="mt-2 text-sm text-slate-400 hover:text-slate-200">
						Close
					</button>
				</div>
			{/if}

			<Card.Title class="text-3xl font-extrabold tracking-tight md:text-4xl">
				Most Recent Cash Flow Statement
			</Card.Title>
			<Card.Description class="text-slate-300">
				Quarterly financial report for period ending {recent_quarter.fiscalDateEnding}
			</Card.Description>
		</Card.Header>

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
	</Card.Root>
</div>
