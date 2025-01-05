<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, Calculator } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';

	let revenue = $state(1000);
	let costOfGoods = $state(400);
	let operatingExpenses = $state(300);
	let depreciation = $state(50);
	let amortization = $state(30);
	let marketCap = $state(2000);
	let debt = $state(500);
	let cash = $state(200);

	let grossProfit = $derived(revenue - costOfGoods);
	let ebitda = $derived(grossProfit - operatingExpenses + depreciation + amortization);
	let ev = $derived(marketCap + debt - cash);
	let evToEbitda = $derived(ev / ebitda);

	const industryPatterns = {
		stable: {
			type: 'Stable Industries',
			range: '8-12x',
			examples: 'Utilities, Telecom',
			characteristics: ['Predictable cash flows', 'Low growth', 'High capital needs']
		},
		growth: {
			type: 'Growth Industries',
			range: '15-25x',
			examples: 'Technology, Healthcare',
			characteristics: ['High growth', 'Strong margins', 'Market leadership']
		},
		valueTrapped: {
			type: 'Value/Cyclical',
			range: '4-8x',
			examples: 'Manufacturing, Basic Materials',
			characteristics: ['Cyclical earnings', 'Asset-heavy', 'Commodity exposure']
		}
	};
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				Understanding EV/EBITDA
			</Card.Title>

			<Card.Description class="space-y-8">
				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">What is EV/EBITDA?</h2>
					<p class="mb-4 text-lg text-slate-300">
						EV/EBITDA is often called the "operating multiple" because it compares a company's total
						value to its operating earnings before accounting and financial adjustments.
					</p>
					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Includes Debt</h3>
							<p class="text-slate-300">
								By using Enterprise Value, it accounts for different debt levels between companies
							</p>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Operating Focus</h3>
							<p class="text-slate-300">
								EBITDA shows earnings from core operations, ignoring financing and accounting
								choices
							</p>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Building EBITDA</h2>
					<div class="space-y-4">
						<div class="rounded-lg bg-slate-700 p-4">
							<div class="grid grid-cols-2 gap-4">
								<div>
									<label class="text-slate-300">Revenue ($M)</label>
									<input
										type="number"
										bind:value={revenue}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label class="text-slate-300">Cost of Goods ($M)</label>
									<input
										type="number"
										bind:value={costOfGoods}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
							</div>
							<div class="mt-4">
								<p class="text-slate-300">Gross Profit: ${grossProfit}M</p>
								<p class="text-sm text-slate-400">Revenue minus Cost of Goods</p>
							</div>
						</div>

						<div class="rounded-lg bg-slate-700 p-4">
							<div class="grid grid-cols-3 gap-4">
								<div>
									<label class="text-slate-300">Operating Expenses ($M)</label>
									<input
										type="number"
										bind:value={operatingExpenses}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label class="text-slate-300">Depreciation ($M)</label>
									<input
										type="number"
										bind:value={depreciation}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label class="text-slate-300">Amortization ($M)</label>
									<input
										type="number"
										bind:value={amortization}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
							</div>
							<div class="mt-4">
								<p class="text-slate-300">EBITDA: ${ebitda}M</p>
								<p class="text-sm text-slate-400">
									Gross Profit - Operating Expenses + Depreciation + Amortization
								</p>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Enterprise Value Components</h2>
					<div class="grid grid-cols-3 gap-4">
						<div>
							<label class="text-slate-300">Market Cap ($M)</label>
							<input
								type="number"
								bind:value={marketCap}
								class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
							/>
						</div>
						<div>
							<label class="text-slate-300">Total Debt ($M)</label>
							<input
								type="number"
								bind:value={debt}
								class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
							/>
						</div>
						<div>
							<label class="text-slate-300">Cash ($M)</label>
							<input
								type="number"
								bind:value={cash}
								class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
							/>
						</div>
					</div>
					<div class="mt-4">
						<p class="text-slate-300">Enterprise Value: ${ev}M</p>
						<p class="text-sm text-slate-400">Market Cap + Debt - Cash</p>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">EV/EBITDA Multiple</h2>
					<div class="text-center">
						<div class="mb-2 text-3xl font-bold text-green-400">
							{evToEbitda.toFixed(1)}x
						</div>
						<p class="text-slate-300">Enterprise Value / EBITDA</p>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Typical Industry Ranges</h2>
					<div class="space-y-4">
						{#each Object.values(industryPatterns) as industry}
							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-2 text-green-400">{industry.type}</h3>
								<div class="grid grid-cols-2 gap-4">
									<div>
										<span class="text-slate-400">Typical Range:</span>
										<span class="ml-2 text-slate-300">{industry.range}</span>
									</div>
									<div>
										<span class="text-slate-400">Examples:</span>
										<span class="ml-2 text-slate-300">{industry.examples}</span>
									</div>
								</div>
								<div class="mt-2">
									<span class="text-slate-400">Key Characteristics:</span>
									<ul class="ml-6 mt-1 list-disc">
										{#each industry.characteristics as trait}
											<li class="text-slate-300">{trait}</li>
										{/each}
									</ul>
								</div>
							</div>
						{/each}
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">When to Use EV/EBITDA</h2>
					<div class="space-y-4">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Best For</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Capital-intensive businesses</li>
								<li class="text-slate-300">Companies with different debt levels</li>
								<li class="text-slate-300">Mature companies with positive EBITDA</li>
							</ul>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Less Useful For</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">High-growth companies with negative EBITDA</li>
								<li class="text-slate-300">Asset-light businesses</li>
								<li class="text-slate-300">Companies with minimal capital expenses</li>
							</ul>
						</div>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
