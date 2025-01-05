<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	let quarters = data.quarters || [];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-4 py-8">
	<h2 class="mb-4 text-3xl font-extrabold uppercase tracking-wide text-white">
		Quarterly Valuation Metrics (ttm)
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
							<th class="px-4 py-3">EV/Sales</th>
							<th class="px-4 py-3">EV/Gross Profit</th>
							<th class="px-4 py-3">EV/EBITDA </th>
							<th class="px-4 py-3">EV/Net Income</th>
							<th class="px-4 py-3">Revenue/Share</th>
							<th class="px-4 py-3">P/S Ratio</th>
						</tr>
					</thead>

					<tbody>
						{#each quarters as row}
							<tr class="border-b border-gray-600/40 hover:bg-gray-800/40">
								<td class="px-4 py-3 text-left">{row.fiscalDateEnding}</td>
								<td class="px-4 py-3">{row.evtosales}</td>
								<td class="px-4 py-3">{row.evtogrossprofit}</td>
								<td class="px-4 py-3">{row.evtoebitda}</td>
								<td class="px-4 py-3">{row.evtonetincome}</td>
								<td class="px-4 py-3">{row.revenue_per_share_ttm}</td>
								<td class="px-4 py-3">{row.price_to_sales_ratio_ttm}</td>
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
