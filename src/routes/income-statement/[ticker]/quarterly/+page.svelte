<script lang="ts">
	import TickerCard from '$lib/components/TickerCard.svelte';
	import { Popover } from 'svelte-ux';
	export let data;
	const { income_data } = data;

	const formatToMillions = (num: string) => {
		if (!num || num === 'None') return '-';
		const millions = (parseFloat(num) / 1_000_000).toFixed(2);
		return `${Number(millions).toLocaleString()}M`;
	};

	let openStates: { [key: string]: boolean } = {
		fiscalDateEnding: false,
		grossProfit: false,
		totalRevenue: false,
		costOfRevenue: false,
		operatingIncome: false,
		sgna: false,
		rd: false,
		operatingExpenses: false,
		interestIncome: false,
		interestExpense: false,
		incomeBeforeTax: false,
		incomeTaxExpense: false,
		ebit: false,
		ebitda: false,
		netIncome: false,
		eps: false,
		estimatedEPS: false,
		epsSurprise: false,
		surprisePercentage: false
	};
</script>

<main class="bg-gray-50 p-6 dark:bg-gray-900">
	<h1 class="mb-6 text-center text-3xl font-bold text-gray-800 dark:text-gray-100">
		Quarterly Financial Metrics
	</h1>
	<div
		class="relative max-h-[600px] overflow-x-auto overflow-y-auto rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800"
	>
		<table class="w-full border-collapse text-left text-sm text-gray-700 dark:text-gray-300">
			<thead
				class="sticky top-0 bg-gray-100 text-xs uppercase text-gray-700 dark:bg-gray-700 dark:text-gray-400"
			>
				<tr class="border-b border-gray-200 dark:border-gray-600">
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
										{:else if key === 'grossProfit'}
											Money left after subtracting production costs from total sales.
										{:else if key === 'totalRevenue'}
											All the money the company made from its business.
										{:else if key === 'costOfRevenue'}
											Costs directly related to making and selling products or services.
										{:else if key === 'operatingIncome'}
											Money earned from the business before paying interest or taxes.
										{:else if key === 'sgna'}
											Costs for running the business, like salaries, rent, and marketing.
										{:else if key === 'rd'}
											Money spent on creating new products or improving existing ones.
										{:else if key === 'operatingExpenses'}
											All costs to run the business, except for making products.
										{:else if key === 'interestIncome'}
											Money earned from investments or loans.
										{:else if key === 'interestExpense'}
											Money paid for borrowing, like on loans or bonds.
										{:else if key === 'incomeBeforeTax'}
											Money earned before subtracting taxes.
										{:else if key === 'incomeTaxExpense'}
											Money the company owes in taxes.
										{:else if key === 'ebit'}
											Money earned before paying interest and taxes.
										{:else if key === 'ebitda'}
											Money earned before interest, taxes, and deductions for equipment wear or
											loans.
										{:else if key === 'netIncome'}
											Final profit after all costs and taxes are paid.
										{:else if key === 'eps'}
											Profit divided by the number of shares, showing how much each share earned.
										{:else if key === 'estimatedEPS'}
											What experts guessed each share would earn.
										{:else if key === 'epsSurprise'}
											The difference between guessed and actual earnings per share.
										{:else if key === 'surprisePercentage'}
											How much the actual earnings per share beat or missed the guess (in
											percentage).
										{/if}
									</div>
								</Popover>

								<button
									class="p-2 transition duration-150 hover:outline hover:outline-2 hover:outline-yellow-500"
									on:click={() => (openStates[key] = !openStates[key])}
								>
									{#if key === 'sgna'}
										SG&A
									{:else if key === 'rd'}
										R&D
									{:else if key === 'eps'}
										EPS
									{:else if key === 'ebit'}
										EBIT
									{:else if key === 'ebitda'}
										EBITDA
									{:else}
										{key.replace(/([A-Z])/g, ' $1').replace(/^[a-z]/, (c) => c.toUpperCase())}
									{/if}
								</button>
							</div>
						</th>
					{/each}
				</tr>
			</thead>

			<tbody class="divide-y divide-gray-200 dark:divide-gray-700">
				{#each income_data as entry}
					<tr
						class="transition-colors duration-200 odd:bg-gray-50 even:bg-white hover:bg-yellow-100 dark:odd:bg-gray-800 dark:even:bg-gray-700 dark:hover:bg-yellow-200/20"
					>
						<td class="whitespace-nowrap px-4 py-3 text-left">{entry.fiscalDateEnding}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.grossProfit)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.totalRevenue)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.costOfRevenue)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.operatingIncome)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.sellingGeneralAndAdministrative)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.researchAndDevelopment)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.operatingExpenses)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right">{entry.interestIncome || '-'}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.interestExpense)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.incomeBeforeTax)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right"
							>{formatToMillions(entry.incomeTaxExpense)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right">{formatToMillions(entry.ebit)}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right">{formatToMillions(entry.ebitda)}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right font-semibold"
							>{formatToMillions(entry.netIncome)}</td
						>
						<td class="whitespace-nowrap px-4 py-3 text-right">{entry.reportedEPS || '-'}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right">{entry.estimatedEPS || '-'}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right">{entry.surprise || '-'}</td>
						<td class="whitespace-nowrap px-4 py-3 text-right">{entry.surprisePercentage || '-'}</td
						>
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
