<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, LineChart } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

	let stockPrice = $state(50);
	let currentEps = $state(2);
	let expectedGrowth = $state(15);
	let marginExpansion = $state(0);
	let sharesOutstanding = $state(20);
	let estimateConfidence = $state('high');

	let forwardEps = $derived(currentEps * (1 + expectedGrowth / 100) * (1 + marginExpansion / 100));
	let forwardPE = $derived(stockPrice / forwardEps);

	let pgRatio = $derived(forwardPE / expectedGrowth);

	const growthPatterns = {
		secular: {
			type: 'Secular Growth',
			peRange: '25-35x',
			growth: '20%+',
			confidence: 'High',
			characteristics: [
				'Large addressable market',
				'Clear competitive advantages',
				'Proven unit economics',
				'Strong management execution'
			]
		},
		cyclicalGrowth: {
			type: 'Cyclical Growth',
			peRange: '12-18x',
			growth: '10-15%',
			confidence: 'Medium',
			characteristics: [
				'Economic sensitivity',
				'Margin cyclicality',
				'Market share gains',
				'Industry consolidation'
			]
		},
		mature: {
			type: 'Mature Growth',
			peRange: '15-20x',
			growth: '8-12%',
			confidence: 'High',
			characteristics: [
				'Market leadership',
				'Pricing power',
				'Operating leverage',
				'Capital return focus'
			]
		},
		turnaround: {
			type: 'Turnaround/Recovery',
			peRange: 'Variable',
			growth: '15-25%',
			confidence: 'Low',
			characteristics: [
				'Margin recovery potential',
				'Cost restructuring',
				'Market repair',
				'Balance sheet repair'
			]
		}
	};
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				Forward Price-to-Earnings (P/E)
			</Card.Title>

			<Card.Description class="space-y-8">
				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Forward P/E Fundamentals</h2>
					<p class="mb-4 text-lg text-slate-300">
						Forward P/E looks at expected future earnings rather than historical results. While more
						relevant for valuation theory, its reliability depends heavily on the quality of
						earnings estimates and visibility into future growth.
					</p>
					<div class="mt-4 rounded-lg bg-slate-700 p-4">
						<p class="mb-2 font-semibold text-green-400">Key Components:</p>
						<p class="text-slate-300">Forward P/E = Current Price / Expected EPS</p>
						<p class="text-slate-300">
							Expected EPS = Current EPS × (1 + Growth) × (1 + Margin Changes)
						</p>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Estimate Builder</h2>
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
								<label class="text-slate-300">Current EPS ($)</label>
								<input
									type="number"
									bind:value={currentEps}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
							</div>
							<div>
								<label class="text-slate-300">Expected Growth Rate (%)</label>
								<input
									type="number"
									bind:value={expectedGrowth}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
								<p class="mt-1 text-sm text-slate-400">Year-over-year earnings growth</p>
							</div>
							<div>
								<label class="text-slate-300">Margin Expansion (%)</label>
								<input
									type="number"
									bind:value={marginExpansion}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								/>
								<p class="mt-1 text-sm text-slate-400">Expected profit margin improvement</p>
							</div>
							<div>
								<label class="text-slate-300">Estimate Confidence</label>
								<select
									bind:value={estimateConfidence}
									class="mt-1 w-full rounded bg-slate-700 p-2 text-white"
								>
									<option value="high">High - Clear Visibility</option>
									<option value="medium">Medium - Some Uncertainty</option>
									<option value="low">Low - Limited Visibility</option>
								</select>
							</div>
						</div>

						<div class="flex flex-col justify-center rounded-lg bg-slate-700 p-6">
							<div class="space-y-6">
								<div>
									<div class="text-slate-300">Forward EPS</div>
									<div class="text-2xl font-bold text-green-400">
										${forwardEps.toFixed(2)}
									</div>
								</div>
								<div class="border-t border-slate-600 pt-4">
									<div class="text-slate-300">Forward P/E</div>
									<div class="text-3xl font-bold text-green-400">
										{forwardPE.toFixed(1)}x
									</div>
								</div>
								<div class="border-t border-slate-600 pt-4">
									<div class="text-slate-300">PEG Ratio</div>
									<div class="text-2xl font-bold text-green-400">
										{pgRatio.toFixed(2)}x
									</div>
									<p class="text-sm text-slate-400">Forward P/E ÷ Growth Rate</p>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Growth Types and Valuation</h2>
					<div class="space-y-4">
						{#each Object.values(growthPatterns) as pattern}
							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-3 text-xl text-green-400">{pattern.type}</h3>
								<div class="mb-3 grid grid-cols-3 gap-4">
									<div>
										<span class="text-slate-400">Typical P/E:</span>
										<span class="ml-2 text-slate-300">{pattern.peRange}</span>
									</div>
									<div>
										<span class="text-slate-400">Growth:</span>
										<span class="ml-2 text-slate-300">{pattern.growth}</span>
									</div>
									<div>
										<span class="text-slate-400">Visibility:</span>
										<span class="ml-2 text-slate-300">{pattern.confidence}</span>
									</div>
								</div>
								<div>
									<span class="text-slate-400">Key Drivers:</span>
									<ul class="ml-6 mt-2 list-disc">
										{#each pattern.characteristics as char}
											<li class="text-slate-300">{char}</li>
										{/each}
									</ul>
								</div>
							</div>
						{/each}
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">Estimate Quality Framework</h2>
					<div class="space-y-4">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">High Confidence Estimates</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Strong recurring revenue base</li>
								<li class="text-slate-300">Contracted backlog visibility</li>
								<li class="text-slate-300">Stable competitive environment</li>
								<li class="text-slate-300">Proven operational execution</li>
							</ul>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Lower Confidence Estimates</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Lumpy/project-based revenue</li>
								<li class="text-slate-300">High economic sensitivity</li>
								<li class="text-slate-300">Competitive disruption risk</li>
								<li class="text-slate-300">Limited operating history</li>
							</ul>
						</div>
					</div>
				</section>

				<section class="rounded-lg bg-slate-800 p-6">
					<h2 class="mb-4 text-xl text-green-400">PEG Ratio Context</h2>
					<p class="mb-4 text-slate-300">
						The PEG ratio helps assess if a forward P/E is justified by expected growth. A PEG of
						1.0 traditionally suggests fair value, but acceptable ranges vary by sector and quality:
					</p>
					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Premium PEG (>1.5)</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">High-quality earnings</li>
								<li class="text-slate-300">Market leadership</li>
								<li class="text-slate-300">Strong balance sheet</li>
							</ul>
						</div>
						<div class="rounded-lg bg-slate-700 p-4">
							<h3 class="mb-2 text-green-400">Discount PEG (less than 1.0)</h3>
							<ul class="ml-6 list-disc">
								<li class="text-slate-300">Cyclical earnings</li>
								<li class="text-slate-300">Competitive pressure</li>
								<li class="text-slate-300">Growth uncertainty</li>
							</ul>
						</div>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
