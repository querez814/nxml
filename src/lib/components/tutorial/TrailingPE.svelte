<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, BarChart2 } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

	let stockPrice = $state(50);
	let netIncome = $state(100);
	let sharesOutstanding = $state(20);
	let extraordinaryItems = $state(0);
	let cyclicalPeak = $state(false);

	let earningsPerShare = $derived((netIncome - extraordinaryItems) / sharesOutstanding);
	let trailingPE = $derived(stockPrice / earningsPerShare);

	const sectorRanges = {
		technology: {
			type: 'Technology',
			range: '20-30x',
			earningsGrowth: '15-25%',
			qualities: [
				'High R&D investment',
				'Strong operating leverage',
				'Recurring revenue mix',
				'Market expansion potential'
			]
		},
		consumer: {
			type: 'Consumer Staples',
			range: '15-20x',
			earningsGrowth: '5-10%',
			qualities: ['Stable earnings', 'Defensive characteristics', 'Brand strength', 'Pricing power']
		},
		industrial: {
			type: 'Industrial',
			range: '12-18x',
			earningsGrowth: '8-12%',
			qualities: [
				'Cyclical earnings',
				'Capital intensity',
				'Economic sensitivity',
				'Scale advantages'
			]
		},
		financial: {
			type: 'Financial',
			range: '10-15x',
			earningsGrowth: '7-12%',
			qualities: [
				'Interest rate sensitivity',
				'Credit cycle exposure',
				'Regulatory capital needs',
				'Fee income stability'
			]
		}
	};
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				Trailing Price-to-Earnings (P/E)
			</Card.Title>

			<Card.Description class="space-y-8">
				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Understanding Trailing P/E</h2>
					<p class="mb-4 text-lg text-slate-300">
						The trailing P/E ratio measures how much investors are paying for each dollar of
						historical earnings. It uses the last twelve months (LTM) of actual reported earnings,
						making it more concrete than forward estimates but potentially less relevant for
						fast-changing companies.
					</p>
					<div class="mt-4 rounded-lg bg-slate-700 p-4">
						<p class="mb-2 font-semibold text-green-400">Basic Formula:</p>
						<p class="text-slate-300">P/E = Stock Price / Earnings Per Share (LTM)</p>
						<p class="text-slate-300">
							EPS = (Net Income - Extraordinary Items) / Shares Outstanding
						</p>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Calculate Trailing P/E</h2>
					<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
						<div class="space-y-4">
							<div>
								<label class="text-slate-300">Stock Price ($)</label>
								<input
									type="number"
									bind:value={stockPrice}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Net Income (LTM, $M)</label>
								<input
									type="number"
									bind:value={netIncome}
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
								<label class="text-slate-300">Extraordinary Items ($M)</label>
								<input
									type="number"
									bind:value={extraordinaryItems}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
								<p class="mt-1 text-sm text-slate-400">One-time gains/losses to exclude</p>
							</div>
							<div class="flex items-center space-x-2">
								<input type="checkbox" bind:checked={cyclicalPeak} class="rounded bg-slate-700" />
								<label class="text-slate-300">Cyclical Peak Earnings?</label>
							</div>
						</div>

						<div class="flex flex-col justify-center rounded-lg bg-slate-700 p-6">
							<div class="space-y-6">
								<div>
									<div class="text-slate-300">Earnings Per Share</div>
									<div class="text-2xl font-bold text-green-400">
										${earningsPerShare.toFixed(2)}
									</div>
								</div>
								<div class="border-t border-slate-600 pt-4">
									<div class="text-slate-300">Trailing P/E</div>
									<div class="text-3xl font-bold text-green-400">
										{trailingPE.toFixed(1)}x
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Sector Patterns</h2>
					<div class="space-y-4">
						{#each Object.values(sectorRanges) as sector}
							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-3 text-xl text-green-400">{sector.type}</h3>
								<div class="mb-3 grid grid-cols-2 gap-4">
									<div>
										<span class="text-slate-400">Typical P/E:</span>
										<span class="ml-2 text-slate-300">{sector.range}</span>
									</div>
									<div>
										<span class="text-slate-400">Earnings Growth:</span>
										<span class="ml-2 text-slate-300">{sector.earningsGrowth}</span>
									</div>
								</div>
								<div>
									<span class="text-slate-400">Key Qualities:</span>
									<ul class="ml-6 mt-2 list-disc">
										{#each sector.qualities as quality}
											<li class="text-slate-300">{quality}</li>
										{/each}
									</ul>
								</div>
							</div>
						{/each}
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Earnings Quality Considerations</h2>
					<div class="space-y-4">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">High Quality Earnings</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Consistent and predictable</li>
								<li class="text-slate-300">Strong cash conversion</li>
								<li class="text-slate-300">Limited one-time items</li>
								<li class="text-slate-300">Conservative accounting</li>
							</ul>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Lower Quality Earnings</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">High volatility</li>
								<li class="text-slate-300">Poor cash conversion</li>
								<li class="text-slate-300">Frequent special items</li>
								<li class="text-slate-300">Aggressive recognition</li>
							</ul>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Business Cycle Impact</h2>
					<div class="space-y-4">
						<p class="text-slate-300">
							Trailing P/E can be misleading during extreme points in the business cycle. At cycle
							peaks, earnings are inflated making P/E look artificially low. At troughs, depressed
							earnings make P/E look artificially high.
						</p>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Cyclical Adjustments</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Use multi-year average earnings</li>
								<li class="text-slate-300">Consider position in cycle</li>
								<li class="text-slate-300">Compare to historical ranges</li>
								<li class="text-slate-300">Factor in normalized margins</li>
							</ul>
						</div>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
