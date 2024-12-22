<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
</script>

<div class="mx-auto w-full max-w-screen-2xl px-4 py-8">
	<h2 class="mb-4 text-3xl font-extrabold uppercase tracking-wide text-white">
		Quarterly Balance Sheet Ratios
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
							<th class="px-4 py-3">Current Ratio</th>
							<th class="px-4 py-3"> Quick (Acid-Test) Ratio</th>
							<th class="px-4 py-3">Cash Ratio</th>
							<th class="px-4 py-3">Debt to Equity Ratio</th>
							<th class="px-4 py-3">Debt to Asset Ratio</th>
							<th class="px-4 py-3">Book Value Per Share</th>
						</tr>
					</thead>

					<tbody>
						{#each quarters as row}
							<tr class="border-b border-gray-600/40 hover:bg-gray-800/40">
								<td class="px-4 py-3 text-left">{row.fiscalDateEnding}</td>
								<td class="px-4 py-3">{row.current_ratio}</td>
								<td class="px-4 py-3">{row.quick_ratio}</td>
								<td class="px-4 py-3">{row.cash_ratio}</td>
								<td class="px-4 py-3">{row.debt_to_equity_ratio}</td>
								<td class="px-4 py-3">{row.debt_to_asset_ratio}</td>
								<td class="px-4 py-3">{row.book_value_per_share}</td>
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
