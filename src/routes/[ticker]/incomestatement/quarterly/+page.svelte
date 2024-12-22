<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-4 py-8">
	<h2 class="mb-4 text-3xl font-extrabold uppercase tracking-wide text-white">
		Quarterly Income Statement
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
							<th class="px-4 py-3 text-left">Period</th>
							<th class="px-4 py-3">Total Revenue (M)</th>
							<th class="px-4 py-3">Cost of Revenue (M)</th>
							<th class="px-4 py-3">Cost of Goods (M)</th>
							<th class="px-4 py-3">Gross Profit (M)</th>
							<th class="px-4 py-3">Op Income (M)</th>
							<th class="px-4 py-3">SG&A (M)</th>
							<th class="px-4 py-3">R&D (M)</th>
							<th class="px-4 py-3">Op Ex (M)</th>
							<th class="px-4 py-3">Interest Income (M)</th>
							<th class="px-4 py-3">Interest Expense (M)</th>
							<th class="px-4 py-3">Pre-Tax (M)</th>
							<th class="px-4 py-3">Tax Loss (M)</th>
							<th class="px-4 py-3">EBITDA (M)</th>
							<th class="px-4 py-3">Net Income (M)</th>
							<th class="px-4 py-3">EPS Non-GAAP</th>
							<th class="px-4 py-3">EPS est</th>
						</tr>
					</thead>

					<tbody>
						{#each quarters as row}
							<tr class="border-b border-gray-600/40 hover:bg-gray-800/40">
								<td class="px-4 py-3 text-left">{row.fiscalDateEnding}</td>
								<td class="px-4 py-3">{row.totalRevenue}</td>
								<td class="px-4 py-3">{row.costOfRevenue}</td>
								<td class="px-4 py-3">{row.costofGoodsAndServicesSold}</td>
								<td class="px-4 py-3">{row.grossProfit}</td>
								<td class="px-4 py-3">{row.operatingIncome}</td>
								<td class="px-4 py-3">{row.sellingGeneralAndAdministrative}</td>
								<td class="px-4 py-3">{row.researchAndDevelopment}</td>
								<td class="px-4 py-3">{row.operatingExpenses}</td>
								<td class="px-4 py-3">{row.interestIncome}</td>
								<td class="px-4 py-3">{row.interestExpense}</td>
								<td class="px-4 py-3">{row.incomeBeforeTax}</td>
								<td class="px-4 py-3">{row.incomeTaxExpense}</td>
								<td class="px-4 py-3">{row.ebitda}</td>
								<td class="px-4 py-3">{row.netIncome}</td>
								<td class="px-4 py-3">{row.reportedEPS}</td>
								<td class="px-4 py-3">{row.estimatedEPS}</td>
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
