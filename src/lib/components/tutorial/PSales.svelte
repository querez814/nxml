<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, CircleDollarSign } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

	let annualRevenue = $state(100);
	let stockPrice = $state(20);
	let sharesOutstanding = $state(10);
	let grossMargin = $state(75);
	let growthRate = $state(40);

	let marketCap = $derived(stockPrice * sharesOutstanding);
	let priceToSales = $derived(marketCap / annualRevenue);

	const industryRanges = {
		softwareHighGrowth: {
			type: 'High-Growth Software',
			range: '15-30x+',
			margins: '75-85%',
			growth: '40%+',
			keyFactors: [
				'Exceptional revenue growth',
				'High gross margins',
				'Strong net revenue retention',
				'Rule of 40 compliance'
			]
		},
		softwareMidGrowth: {
			type: 'Mid-Growth Software',
			range: '5-15x',
			margins: '70-80%',
			growth: '20-40%',
			keyFactors: [
				'Solid revenue growth',
				'Good margins',
				'Established market position',
				'Path to profitability'
			]
		},
		consumer: {
			type: 'Consumer Products',
			range: '1-3x',
			margins: '40-60%',
			growth: '10-20%',
			keyFactors: ['Brand strength', 'Moderate margins', 'Competitive moat', 'Market share gains']
		},
		retail: {
			type: 'Retail',
			range: '0.3-1.5x',
			margins: '20-40%',
			growth: '5-15%',
			keyFactors: ['Low margins', 'High competition', 'Capital intensive', 'Scale advantages']
		}
	};
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				Price to Sales (P/S) Ratio
			</Card.Title>

			<Card.Description class="space-y-8">
				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">The Growth Company Metric</h2>
					<p class="mb-4 text-lg text-slate-300">
						Price to Sales has become one of the most important metrics for evaluating growth
						companies, especially those not yet showing profits. Unlike profit-based metrics, it
						lets us value companies investing heavily in growth.
					</p>
					<div class="mt-4 rounded-lg bg-slate-700 p-4">
						<p class="mb-2 font-semibold text-green-400">Key Formula:</p>
						<p class="text-slate-300">P/S Ratio = Market Cap / Annual Revenue</p>
						<p class="text-slate-300">= (Stock Price × Shares Outstanding) / Annual Revenue</p>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Calculate P/S Ratio</h2>
					<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
						<div class="space-y-4">
							<div>
								<label class="text-slate-300">Annual Revenue ($M)</label>
								<input
									type="number"
									bind:value={annualRevenue}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Stock Price ($)</label>
								<input
									type="number"
									bind:value={stockPrice}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Shares Outstanding (M)</label>
								<input
									type="number"
									bind:value={sharesOutstanding}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Gross Margin (%)</label>
								<input
									type="number"
									bind:value={grossMargin}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Growth Rate (%)</label>
								<input
									type="number"
									bind:value={growthRate}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
						</div>

						<div class="flex flex-col justify-center rounded-lg bg-slate-700 p-6">
							<div class="space-y-6">
								<div>
									<div class="text-slate-300">Market Cap</div>
									<div class="text-2xl font-bold text-green-400">
										${marketCap}M
									</div>
								</div>
								<div class="border-t border-slate-600 pt-4">
									<div class="text-slate-300">P/S Ratio</div>
									<div class="text-3xl font-bold text-green-400">
										{priceToSales.toFixed(1)}x
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Industry Patterns</h2>
					<div class="space-y-4">
						{#each Object.values(industryRanges) as industry}
							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-3 text-xl text-green-400">{industry.type}</h3>
								<div class="mb-3 grid grid-cols-3 gap-4">
									<div>
										<span class="text-slate-400">P/S Range:</span>
										<span class="ml-2 text-slate-300">{industry.range}</span>
									</div>
									<div>
										<span class="text-slate-400">Margins:</span>
										<span class="ml-2 text-slate-300">{industry.margins}</span>
									</div>
									<div>
										<span class="text-slate-400">Growth:</span>
										<span class="ml-2 text-slate-300">{industry.growth}</span>
									</div>
								</div>
								<div>
									<span class="text-slate-400">Key Success Factors:</span>
									<ul class="ml-6 mt-2 list-disc">
										{#each industry.keyFactors as factor}
											<li class="text-slate-300">{factor}</li>
										{/each}
									</ul>
								</div>
							</div>
						{/each}
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Using P/S Effectively</h2>
					<div class="space-y-4">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Higher P/S Justified When:</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Gross margins are high (>70%)</li>
								<li class="text-slate-300">Revenue growth is strong (>30%)</li>
								<li class="text-slate-300">Net revenue retention >120%</li>
								<li class="text-slate-300">Clear path to profitability exists</li>
							</ul>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Lower P/S Expected When:</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Low gross margins (less than 40%)</li>
								<li class="text-slate-300">Slower growth (less than 15%)</li>
								<li class="text-slate-300">High customer churn</li>
								<li class="text-slate-300">Heavy competition</li>
							</ul>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Rule of 40</h2>
					<p class="mb-4 text-slate-300">
						For software companies, the "Rule of 40" helps justify P/S ratios. If revenue growth
						rate + profit margin ≥ 40%, higher multiples are often warranted. This balances growth
						and profitability.
					</p>
					<div class="rounded-lg bg-slate-700 p-4">
						<p class="text-slate-300">Your Score: {(growthRate + grossMargin * 0.3).toFixed(1)}%</p>
						<p class="text-sm text-slate-400">
							(Growth Rate + Estimated Profit Margin based on typical conversion of gross margin)
						</p>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
