<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-4 py-8">
	<h2 class="mb-4 text-3xl font-extrabold uppercase tracking-wide text-white">
		Quarterly Balance Sheet
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
							<th class="px-4 py-3">Current Assets (M)</th>
							<th class="px-4 py-3">Cash and Cash EQ (M)</th>
							<th class="px-4 py-3">Inventory (M)</th>
							<th class="px-4 py-3">PPE (M)</th>
							<th class="px-4 py-3">Total Assets (M)</th>
							<th class="px-4 py-3">Current Liabilities (M)</th>
							<th class="px-4 py-3">Total Liabilities (M)</th>
							<th class="px-4 py-3">Current Debt (M)</th>
							<th class="px-4 py-3">Deferred Revenue (M)</th>
							<th class="px-4 py-3">Working Capital (M)</th>
							<th class="px-4 py-3">Shareholder Equity (M)</th>
						</tr>
					</thead>

					<tbody>
						{#each quarters as row}
							<tr class="border-b border-gray-600/40 hover:bg-gray-800/40">
								<td class="px-4 py-3 text-left">{row.fiscalDateEnding}</td>
								<td class="px-4 py-3">{row.totalCurrentAssets}</td>
								<td class="px-4 py-3">{row.cashAndCashEquivalentsAtCarryingValue}</td>
								<td class="px-4 py-3">{row.inventory}</td>
								<td class="px-4 py-3">{row.propertyPlantEquipment}</td>
								<td class="px-4 py-3">{row.totalAssets}</td>
								<td class="px-4 py-3">{row.totalCurrentLiabilities}</td>
								<td class="px-4 py-3">{row.totalLiabilities}</td>
								<td class="px-4 py-3">{row.currentDebt}</td>
								<td class="px-4 py-3">{row.deferredRevenue}</td>
								<td class="px-4 py-3">{row.working_capital}</td>
								<td class="px-4 py-3">{row.totalShareholderEquity}</td>
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
