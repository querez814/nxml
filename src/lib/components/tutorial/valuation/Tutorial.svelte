<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, Rocket } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';

	let revenue = $state(100);
	let marketCap = $state(500);
	let debt = $state(50);
	let cash = $state(30);

	let ev = $derived(marketCap + debt - cash);
	let evToSales = $derived(ev / revenue);

	const industryTypes = {
		highGrowthSoftware: {
			type: 'High-Growth Software',
			growth: '40-100%+',
			margins: '80-90%',
			evRange: '15-30x',
			characteristics: [
				'Rapid revenue growth',
				'High gross margins',
				'Strong recurring revenue',
				'High R&D investment'
			]
		},
		legacyTech: {
			type: 'Legacy Technology',
			growth: '6-12%',
			margins: '60-70%',
			evRange: '3-5x',
			characteristics: [
				'Stable revenue base',
				'Established market position',
				'Moderate growth',
				'Mix of products and services'
			]
		},
		semiconductor: {
			type: 'Semiconductor',
			growth: '15-25%',
			margins: '50-65%',
			evRange: '4-8x',
			characteristics: [
				'Cyclical business',
				'High capital requirements',
				'Complex supply chains',
				'R&D intensive'
			]
		},
		hardwareManufacturing: {
			type: 'Hardware Manufacturing',
			growth: '5-15%',
			margins: '30-45%',
			evRange: '1.5-3x',
			characteristics: [
				'Physical inventory',
				'Lower margins',
				'Capital intensive',
				'Supply chain dependent'
			]
		},
		retail: {
			type: 'Retail',
			growth: '4-8%',
			margins: '25-35%',
			evRange: '0.5-1.5x',
			characteristics: ['Thin margins', 'High inventory', 'Real estate costs', 'Competitive market']
		}
	};
</script>

<div class="w-full max-w-4xl space-y-6 bg-slate-900 p-4">
	<Card.Root class="background-background border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				Understanding EV/Sales Across Industries
			</Card.Title>

			<Card.Description class="space-y-8">
				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">The Basics of EV/Sales</h2>
						<p class="mb-4 text-lg text-slate-300">
							EV/Sales tells us how expensive a company is relative to its revenue. It's especially
							useful when comparing companies that aren't profitable yet, as it helps us understand
							how the market values their revenue.
						</p>
					</div>
				</section>

				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">Building Enterprise Value (EV)</h2>
						<div class="space-y-4">
							<div class="rounded-lg bg-slate-700 p-4">
								<p class="text-lg text-slate-300">
									Market Cap + Total Debt - Cash = Enterprise Value
								</p>
							</div>
							<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Market Cap</h3>
									<p class="text-slate-300">The public market value of all outstanding shares</p>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Total Debt</h3>
									<p class="text-slate-300">All debt obligations the company must repay</p>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Cash</h3>
									<p class="text-slate-300">
										Available liquid assets that offset the purchase price
									</p>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">Calculate EV/Sales</h2>
						<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
							<!-- Inputs -->
							<div class="space-y-4">
								<div class="space-y-2">
									<label class="text-slate-300">Annual Revenue ($M)</label>
									<input
										type="number"
										bind:value={revenue}
										class="w-full rounded bg-slate-700 p-2 text-white"
										min="0"
									/>
								</div>
								<div class="space-y-2">
									<label class="text-slate-300">Market Cap ($M)</label>
									<input
										type="number"
										bind:value={marketCap}
										class="w-full rounded bg-slate-700 p-2 text-white"
										min="0"
									/>
								</div>
								<div class="space-y-2">
									<label class="text-slate-300">Total Debt ($M)</label>
									<input
										type="number"
										bind:value={debt}
										class="w-full rounded bg-slate-700 p-2 text-white"
										min="0"
									/>
								</div>
								<div class="space-y-2">
									<label class="text-slate-300">Cash ($M)</label>
									<input
										type="number"
										bind:value={cash}
										class="w-full rounded bg-slate-700 p-2 text-white"
										min="0"
									/>
								</div>
							</div>

							<div class="flex flex-col justify-center rounded-lg bg-slate-700 p-6">
								<div class="space-y-6">
									<div>
										<div class="text-slate-300">Enterprise Value</div>
										<div class="text-2xl font-bold text-green-400">
											${ev}M
										</div>
									</div>
									<div class="border-t border-slate-600 pt-4">
										<div class="text-slate-300">EV/Sales Ratio</div>
										<div class="text-2xl font-bold text-green-400">
											{evToSales.toFixed(1)}x
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>

				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">Understanding Industry Patterns</h2>
						<p class="mb-6 text-slate-300">
							Different industries have typical EV/Sales ranges based on their growth rates,
							margins, and business characteristics. Here's how they compare:
						</p>
						<div class="space-y-6">
							{#each Object.values(industryTypes) as industry}
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-3 text-lg text-green-400">{industry.type}</h3>
									<div class="mb-3 grid grid-cols-1 gap-4 md:grid-cols-3">
										<div>
											<span class="text-slate-400">Growth Rate:</span>
											<span class="ml-2 text-slate-300">{industry.growth}</span>
										</div>
										<div>
											<span class="text-slate-400">Typical Margins:</span>
											<span class="ml-2 text-slate-300">{industry.margins}</span>
										</div>
										<div>
											<span class="text-slate-400">EV/Sales Range:</span>
											<span class="ml-2 text-slate-300">{industry.evRange}</span>
										</div>
									</div>
									<div class="text-sm text-slate-300">
										<span class="text-slate-400">Key Characteristics:</span>
										<ul class="ml-6 mt-2 list-disc">
											{#each industry.characteristics as trait}
												<li>{trait}</li>
											{/each}
										</ul>
									</div>
								</div>
							{/each}
						</div>
					</div>
				</section>

				<section class="space-y-4">
					<div class="rounded-lg bg-slate-800 p-6">
						<h2 class="mb-4 text-xl text-green-400">Core Principles to Remember</h2>
						<div class="space-y-4 text-slate-300">
							<p>The EV/Sales ratio is fundamentally driven by three key factors:</p>

							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-2 text-green-400">1. Growth Rate</h3>
								<p>
									Faster growing companies command higher multiples because investors are willing to
									pay more for rapidly expanding revenue streams.
								</p>
							</div>

							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-2 text-green-400">2. Profit Margins</h3>
								<p>
									Higher margin businesses deserve higher multiples because each dollar of revenue
									translates into more potential profit.
								</p>
							</div>

							<div class="rounded-lg bg-slate-700 p-4">
								<h3 class="mb-2 text-green-400">3. Business Model</h3>
								<p>
									Companies with recurring revenue, strong market positions, and capital-light
									models typically command premium valuations.
								</p>
							</div>
						</div>
					</div>
				</section>
			</Card.Description>
		</Card.Header>
	</Card.Root>
</div>
