<script lang="ts">
	import { Popover } from 'svelte-ux';
	export let data;

	const { balancesheet_data } = data;

	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};

	let openStates: { [key: string]: boolean } = {
		fiscalDateEnding: false,
		totalCurrentAssets: false,
		totalAssets: false,
		totalCurrentLiabilities: false,
		totalLiabilities: false,
		working_capital: false,
		totalShareholderEquity: false,
		commonStockSharesOutstanding: false,
		cashAndCashEquivalentsAtCarryingValue: false,
		inventory: false,
		propertyPlantEquipment: false,
		deferredRevenue: false,
		currentDebt: false
	};
</script>

<main class="bg-gray-100 p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">
		Quarterly Balance Sheet Statements
	</h1>
	<div class="max-h-[600px] overflow-auto rounded-lg border bg-white shadow-lg">
		<table class="auto table w-full border-collapse text-sm">
			<thead class="bg-yellow-80 sticky top-0 text-white">
				<tr>
					{#each Object.entries(openStates) as [key, isOpen]}
						<th class="relative whitespace-nowrap px-4 py-3 text-left font-medium">
							<div class="inline-block">
								<Popover bind:open={openStates[key]}>
									<div
										class="rounded border border-gray-600 bg-gray-800 p-2 text-sm text-white shadow"
										style="position: absolute; left: 0; top: 100%; transform: translateY(10px); max-width: 400px;"
									>
										{#if key === 'fiscalDateEnding'}
											The last date of the company's reporting period (like the end of a quarter or
											year).
										{:else if key === 'totalCurrentAssets'}
											Things the company owns that it can quickly turn into cash.
										{:else if key === 'totalAssets'}
											Everything the company owns, including cash, property, and equipment.
										{:else if key === 'totalCurrentLiabilities'}
											Short-term bills or money the company owes, due soon.
										{:else if key === 'totalLiabilities'}
											All the money the company owes, like loans or unpaid bills.
										{:else if key === 'working_capital'}
											Money left after subtracting short-term bills from short-term assets.
										{:else if key === 'totalShareholderEquity'}
											The value left for shareholders if the company sold everything and paid all
											debts.
										{:else if key === 'commonStockSharesOutstanding'}
											How many shares of the company's stock are owned by people.
										{:else if key === 'cashAndCashEquivalentsAtCarryingValue'}
											Money the company has in the bank or as cash.
										{:else if key === 'inventory'}
											Items the company plans to sell but hasn’t sold yet.
										{:else if key === 'propertyPlantEquipment'}
											Big things the company owns, like buildings, machines, or land.
										{:else if key === 'deferredRevenue'}
											Money the company has received but hasn’t yet earned (like prepayments).
										{:else if key === 'currentDebt'}
											Loans or money the company must repay soon.
										{/if}
									</div>
								</Popover>

								<button
									class="p-2 transition duration-150 hover:outline hover:outline-2 hover:outline-yellow-500"
									on:click={() => (openStates[key] = !openStates[key])}
								>
									{key.replace(/([A-Z])/g, ' $1').replace(/^[a-z]/, (c) => c.toUpperCase())}
								</button>
							</div>
						</th>
					{/each}
				</tr>
			</thead>

			<tbody class="text-gray-700">
				{#each balancesheet_data as entry, i}
					<tr
						class="{i % 2 === 0
							? 'bg-gray-50'
							: 'bg-white'} transition duration-200 hover:bg-yellow-100"
					>
						<td class="border px-4 py-3 text-center">{entry.fiscalDateEnding}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalCurrentAssets)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalAssets)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.totalCurrentLiabilities)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.totalLiabilities)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.working_capital)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.totalShareholderEquity)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.commonStockSharesOutstanding)}</td
						>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.cashAndCashEquivalentsAtCarryingValue)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.inventory)}</td>
						<td class="border px-4 py-3 text-right"
							>{formatToMillions(entry.propertyPlantEquipment)}</td
						>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.deferredRevenue)}</td>
						<td class="border px-4 py-3 text-right">{formatToMillions(entry.currentDebt)}</td>
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
