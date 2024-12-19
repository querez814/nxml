<script lang="ts">
	export let data;
	const { margin_data } = data;
	const marginData = data?.margin_data || [];

	const formattedData = Array.isArray(marginData)
		? marginData.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				grossMargin: entry.grossMargin || '0%',
				operatingMargin: entry.operatingMargin || '0%',
				ebitMargin: entry.ebitMargin || '0%',
				ebitdaMargin: entry.ebitdaMargin || '0%',
				netMargin: entry.netMargin || '0%'
			}))
		: [];
</script>

<main>
	<h1 class="text-center text-3xl font-bold text-gray-800">Income Statement Margins</h1>
	<div class="bg-gray-100 p-6">
		<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
			<table class="auto table w-full border-collapse text-sm">
				<thead class="sticky top-0 bg-yellow-800 text-white">
					<tr>
						<th class="border px-4 py-3">Fiscal Date Ending</th>
						<th class="border px-4 py-3">Gross Margin</th>
						<th class="border px-4 py-3">Operating Margin</th>
						<th class="border px-4 py-3">EBIT Margin</th>
						<th class="border px-4 py-3">EBITDA Margin</th>
						<th class="border px-4 py-3">Net Margin</th>
					</tr>
				</thead>
				<tbody class="text-gray-700">
					{#each formattedData as entry, i}
						<tr
							class="{i % 2 === 0
								? 'bg-gray-50'
								: 'bg-white'} transition duration-200 hover:bg-yellow-100"
						>
							<td class="border px-4 py-3">{entry.fiscalDateEnding}</td>
							<td class="border px-4 py-3">{entry.grossMargin}</td>
							<td class="border px-4 py-3">{entry.operatingMargin}</td>
							<td class="border px-4 py-3">{entry.ebitMargin}</td>
							<td class="border px-4 py-3">{entry.ebitdaMargin}</td>
							<td class="border px-4 py-3">{entry.netMargin}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</main>
