<script lang="ts">
	import type { PageData } from '../$types';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-4 py-8">
	<h2 class="mb-4 text-3xl font-extrabold uppercase tracking-wide text-white">
		Quarterly Cash Flow Statements
	</h2>

	<div
		class="
      rounded-xl
      bg-gradient-to-br
      from-gray-800
      to-gray-900
      p-6
      shadow-xl ring-1
      ring-gray-700
    "
	>
		{#if quarters.length > 0}
			<div class="overflow-x-auto">
				<table
					class="
            w-full
            table-auto
            border-collapse
            text-left
            text-gray-100
          "
				>
					<caption
						class="
              caption-top
              p-3
              text-left
              text-lg
              font-bold
              text-white
            "
					>
						All Quarters (Newest First)
					</caption>

					<thead class="sticky top-0 z-10 bg-gray-700 text-sm uppercase tracking-wider">
						<tr>
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
						{#each quarters as row}
							<tr class="border-b border-gray-600/40 hover:bg-gray-800/40">
								<td class="px-4 py-3 text-left">{row.fiscalDateEnding}</td>
								<td class="px-4 py-3">{row.operatingCashflow}</td>
								<td class="px-4 py-3">{row.capitalExpenditures}</td>
								<td class="px-4 py-3">{row.freeCashFlow}</td>
								<td class="px-4 py-3">{row.changeInInventory}</td>
								<td class="px-4 py-3">{row.changeInReceivables}</td>
								<td class="px-4 py-3">{row.cashflowFromInvestment}</td>
								<td class="px-4 py-3">{row.cashflowFromFinancing}</td>
								<td class="px-4 py-3">{row.paymentsForRepurchaseOfCommonStock}</td>
								<td class="px-4 py-3">{row.dividendPayout}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<p class="mt-4 text-base text-white">No quarterly data found.</p>
		{/if}
	</div>
</div>

<style>
</style>
