<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import * as Table from '$lib/components/ui/table';
	import { Badge } from '$lib/components/ui/badge';
	import { Separator } from '$lib/components/ui/separator';
	import { TrendingUp, TrendingDown, Minus } from 'lucide-svelte';

	let {
		fiscalDateEnding,
		grossProfit,
		totalRevenue,
		costOfRevenue,
		costofGoodsAndServicesSold,
		operatingIncome,
		sellingGeneralAndAdministrative,
		researchAndDevelopment,
		operatingExpenses,
		interestIncome,
		interestExpense,
		incomeBeforeTax,
		incomeTaxExpense,
		interestAndDebtExpense,
		ebit,
		ebitda,
		netIncome,
		reportedEPS,
		estimatedEPS,
		surprise,
		surprisePercentage
	} = $props();
</script>

<div class="mx-auto w-full max-w-screen-2xl px-6 py-12">
	<Card.Root class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100">
		<Card.Header>
			<Card.Title class="text-3xl font-extrabold tracking-tight md:text-4xl">
				Most Recent Income Statement
			</Card.Title>
			<Card.Description class="text-slate-300">
				Quarterly financial report for period ending {fiscalDateEnding}
			</Card.Description>
		</Card.Header>

		<Card.Content>
			<div class="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
				<div class="rounded-lg bg-slate-800/60 p-4">
					<p class="text-sm text-slate-400">Revenue</p>
					<p class="text-2xl font-bold">{totalRevenue}M</p>
				</div>
				<div class="rounded-lg bg-slate-800/60 p-4">
					<p class="text-sm text-slate-400">Net Income</p>
					<p class="text-2xl font-bold">{netIncome}M</p>
				</div>
				<div class="rounded-lg bg-slate-800/60 p-4">
					<p class="text-sm text-slate-400">EPS</p>
					<div class="flex items-center gap-2">
						<p class="text-2xl font-bold">${reportedEPS}</p>
						<Badge
							variant={surprise > 0 ? 'secondary' : surprise < 0 ? 'destructive' : 'outline'}
							class="flex items-center gap-1"
						>
							{#if surprise > 0}
								<TrendingUp class="h-3 w-3" />
							{:else if surprise < 0}
								<TrendingDown class="h-3 w-3" />
							{:else}
								<Minus class="h-3 w-3" />
							{/if}
							{surprise > 0 ? '+' : ''}{surprisePercentage}% vs est.
						</Badge>
					</div>
				</div>
			</div>

			<Separator class="my-6" />

			<div class="overflow-x-auto rounded-lg">
				<Table.Root>
					<Table.Header>
						<Table.Row>
							<Table.Head class="text-slate-300">Metric</Table.Head>
							<Table.Head class="text-right text-slate-300">Amount (M)</Table.Head>
						</Table.Row>
					</Table.Header>
					<Table.Body>
						<Table.Row>
							<Table.Cell>Total Revenue</Table.Cell>
							<Table.Cell class="text-right">{totalRevenue}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell>Cost of Revenue</Table.Cell>
							<Table.Cell class="text-right">{costOfRevenue}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell class="font-medium">Gross Profit</Table.Cell>
							<Table.Cell class="text-right font-medium">{grossProfit}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell>Operating Expenses</Table.Cell>
							<Table.Cell class="text-right">{operatingExpenses}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell>Operating Income</Table.Cell>
							<Table.Cell class="text-right">{operatingIncome}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell class="font-medium">EBITDA</Table.Cell>
							<Table.Cell class="text-right font-medium">{ebitda}</Table.Cell>
						</Table.Row>
						<Table.Row>
							<Table.Cell class="font-medium">Net Income</Table.Cell>
							<Table.Cell class="text-right font-medium">{netIncome}</Table.Cell>
						</Table.Row>
					</Table.Body>
				</Table.Root>
			</div>

			<div class="mt-8">
				<h3 class="mb-4 text-xl font-semibold">Earnings Performance</h3>
				<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
					<div class="rounded-lg bg-slate-800/60 p-4">
						<p class="text-sm text-slate-400">Reported EPS</p>
						<p class="text-2xl font-bold">${reportedEPS}</p>
					</div>
					<div class="rounded-lg bg-slate-800/60 p-4">
						<p class="text-sm text-slate-400">vs Estimated</p>
						<div class="flex items-center gap-2">
							<p class="text-2xl font-bold">${estimatedEPS}</p>
							<Badge
								variant={surprise > 0 ? 'secondary' : surprise < 0 ? 'destructive' : 'outline'}
								class="flex items-center gap-1"
							>
								{#if surprise > 0}
									<TrendingUp class="h-3 w-3" />
								{:else if surprise < 0}
									<TrendingDown class="h-3 w-3" />
								{:else}
									<Minus class="h-3 w-3" />
								{/if}
								{surprise > 0 ? '+' : ''}{surprisePercentage}%
							</Badge>
						</div>
					</div>
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
