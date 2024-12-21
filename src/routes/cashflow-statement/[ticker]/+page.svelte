<script lang="ts">
	import { Popover } from 'svelte-ux';
	export let data;

	const { cashflow_data } = data;

	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};

	let openStates: { [key: string]: boolean } = {
		fiscalDateEnding: false,
		operatingCashflow: false,
		depreciationDepletionAndAmortization: false,
		capitalExpenditures: false,
		changeInReceivables: false,
		changeInInventory: false,
		paymentsForRepurchaseOfCommonStock: false,
		freeCashFlow: false
	};
</script>

<main class="bg-gray-100 p-6">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">Quarterly Cash Flow Statements</h1>
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
										{:else if key === 'operatingCashflow'}
											Money from the company's core operations, showing if it’s making cash from its
											business.
										{:else if key === 'depreciationDepletionAndAmortization'}
											The gradual reduction in value of assets over time, like machines or natural
											resources.
										{:else if key === 'capitalExpenditures'}
											Money spent to buy or improve long-term assets like buildings or equipment.
										{:else if key === 'changeInReceivables'}
											Difference in money owed to the company by customers.
										{:else if key === 'changeInInventory'}
											Difference in the cost of items the company has but hasn't sold yet.
										{:else if key === 'paymentsForRepurchaseOfCommonStock'}
											Money spent by the company to buy back its own shares.
										{:else if key === 'freeCashFlow'}
											Cash left after paying for operations and investments, available for dividends
											or growth.
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
