<script lang="ts">
	export let data;
	const { valuation_data } = data;
	const valuationData = data?.valuation_data || [];
	const formattedData = Array.isArray(valuationData)
		? valuationData.map((entry: any) => ({
				fiscalDateEnding: entry.fiscalDateEnding || '-',
				symbol: entry.symbol || '-',
				evtosales: entry.evtosales || '-',
				evtoebit: entry.evtoebit || '-',
				evtoebitda: entry.evtoebitda || '-',
				evtonetincome: entry.evtonetincome || '-',
				AnalystTargetPrice: entry.AnalystTargetPrice || '-',
				AnalystRatingStrongBuy: entry.AnalystRatingStrongBuy || '-',
				AnalystRatingBuy: entry.AnalystRatingBuy || '-',
				AnalystRatingHold: entry.AnalystRatingHold || '-',
				AnalystRatingSell: entry.AnalystRatingSell || '-',
				AnalystRatingStrongSell: entry.AnalystRatingStrongSell || '-',
				TrailingPE: entry.TrailingPE || '-',
				ForwardPE: entry.ForwardPE || '-'
			}))
		: [];
</script>

<div class="min-h-screen bg-gray-100 p-6">
	<h1 class="mb-4 text-3xl font-bold text-gray-800">Ticker Valuation Dashboard</h1>
	<div class="overflow-x-auto">
		<table
			class="w-full table-auto border-collapse rounded-lg border border-gray-200 bg-white shadow-lg"
		>
			<thead>
				<tr class="bg-gray-200 text-gray-700">
					<th class="px-4 py-2">Fiscal Date</th>
					<th class="px-4 py-2">Symbol</th>
					<th class="px-4 py-2">EV to Sales</th>
					<th class="px-4 py-2">EV to EBIT</th>
					<th class="px-4 py-2">EV to EBITDA</th>
					<th class="px-4 py-2">EV to Net Income</th>
				</tr>
			</thead>
			<tbody>
				{#each formattedData as entry}
					<tr class="border-b border-gray-200 hover:bg-gray-100">
						<td class="px-4 py-2">{entry.fiscalDateEnding}</td>
						<td class="px-4 py-2">{entry.symbol}</td>
						<td class="px-4 py-2">{entry.evtosales}</td>
						<td class="px-4 py-2">{entry.evtoebit}</td>
						<td class="px-4 py-2">{entry.evtoebitda}</td>
						<td class="px-4 py-2">{entry.evtonetincome}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
