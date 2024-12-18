<script lang="ts">
	export let data;
	const { cashflow_data } = data;
	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};
</script>

<main class="bg-gray-100 p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">Quarterly Cash Flow Statements</h1>
	<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
		<table class="auto table w-full border-collapse text-sm">
			<thead class="bg-yellow-80 sticky top-0 text-white">
				<tr>
					<th class="border px-4 py-3">Fiscal Date Ending</th>
					<th class="border px-4 py-3">Operating Cash Flow</th>
					<th class="border px-4 py-3">D&A</th>
					<th class="border px-4 py-3">Cap-Ex</th>
					<th class="border px-4 py-3">Change in Receivables</th>
					<th class="border px-4 py-3">Change in Inventory</th>
					<th class="border px-4 py-3">Payments for Stock Repurchase</th>
					<th class="border px-4 py-3">Free Cash Flow</th>
				</tr>
			</thead>

			<tbody class="text-gray-700">
				{#each cashflow_data as entry, i}
					<tr
						class="{i % 2 === 0
							? 'bg-gray-50'
							: 'bg-white'} transition duration-200 hover:bg-yellow-100"
					>
						<td class="border px-4 py-3 text-center">{entry.fiscalDateEnding}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.operatingCashflow)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.depreciationDepletionAndAmortization)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.capitalExpenditures)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.changeInReceivables)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.changeInInventory)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.paymentsForRepurchaseOfCommonStock)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.freeCashFlow)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</main>

<style>
	table {
		font-family: Arial, sans-serif;
	}
	th,
	td {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8px;
	}
</style>
