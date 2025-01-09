<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, Calculator } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Alert from '$lib/components/ui/alert';

	interface CompanyExample {
		name: string;
		ticker: string;
		multiple: string;
		historicalRange: string;
		notes: string;
		keyFactors: string[];
	}

	interface IndustryPattern {
		type: string;
		range: string;
		interpretation: string;
		examples: CompanyExample[];
		characteristics: string[];
		adjustmentFactors: string[];
		whenToUse: string[];
	}

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
	let grossMargin = $derived((grossProfit / revenue) * 100);
	let ebitdaMargin = $derived((ebitda / revenue) * 100);

	const industryPatterns: Record<string, IndustryPattern> = {
		industrials: {
			type: 'Industrial Manufacturing',
			range: '8-12x',
			interpretation: 'Reflects capital intensity and cyclical exposure',
			examples: [
				{
					name: 'Deere & Company',
					ticker: 'DE',
					multiple: '12-14x',
					historicalRange: '8-16x',
					notes: 'Premium multiple due to technology integration and strong market position',
					keyFactors: ['Ag cycle position', 'Precision ag adoption', 'Aftermarket revenue']
				},
				{
					name: 'Caterpillar',
					ticker: 'CAT',
					multiple: '10-12x',
					historicalRange: '6-14x',
					notes: 'Cyclical exposure balanced by global presence',
					keyFactors: ['Mining cycle', 'Infrastructure spending', 'Service revenue mix']
				}
			],
			characteristics: [
				'High capital requirements',
				'Cyclical end markets',
				'Service revenue opportunities'
			],
			adjustmentFactors: [
				'Working capital intensity',
				'Maintenance vs growth capex',
				'Lease adjustments'
			],
			whenToUse: [
				'Comparing companies with different capital structures',
				'Analyzing through-cycle earnings power',
				'Evaluating operational efficiency'
			]
		},
		technology: {
			type: 'Enterprise Technology',
			range: '12-18x',
			interpretation: 'Higher multiples reflect growth and margin profile',
			examples: [
				{
					name: 'Microsoft',
					ticker: 'MSFT',
					multiple: '18-20x',
					historicalRange: '8-22x',
					notes: 'Premium reflects cloud growth and software margins',
					keyFactors: ['Cloud growth rate', 'Operating leverage', 'Enterprise IT spend']
				},
				{
					name: 'IBM',
					ticker: 'IBM',
					multiple: '8-10x',
					historicalRange: '6-12x',
					notes: 'Lower multiple reflects legacy exposure',
					keyFactors: ['Cloud transition', 'Consulting mix', 'Mainframe cycle']
				}
			],
			characteristics: ['High margins', 'Recurring revenue', 'Platform economics'],
			adjustmentFactors: ['Stock-based compensation', 'R&D capitalization', 'Deferred revenue'],
			whenToUse: [
				'Comparing mature tech companies',
				'Analyzing business model transitions',
				'Evaluating margin sustainability'
			]
		},
		healthcare: {
			type: 'Healthcare Services',
			range: '10-14x',
			interpretation: 'Steady multiples reflect defensive characteristics',
			examples: [
				{
					name: 'UnitedHealth',
					ticker: 'UNH',
					multiple: '12-14x',
					historicalRange: '8-16x',
					notes: 'Premium for scale and Optum growth',
					keyFactors: ['Medical cost trends', 'Value-based care', 'Technology integration']
				},
				{
					name: 'HCA Healthcare',
					ticker: 'HCA',
					multiple: '8-10x',
					historicalRange: '6-12x',
					notes: 'Asset intensity affects multiple',
					keyFactors: ['Payer mix', 'Volume trends', 'Capital requirements']
				}
			],
			characteristics: ['Stable demand', 'Regulatory oversight', 'Scale advantages'],
			adjustmentFactors: [
				'Lease obligations',
				'Joint venture accounting',
				'Risk-sharing arrangements'
			],
			whenToUse: [
				'Comparing different healthcare business models',
				'Analyzing operational efficiency',
				'Evaluating scale benefits'
			]
		},
		consumer: {
			type: 'Consumer Staples',
			range: '11-15x',
			interpretation: 'Reflects defensive characteristics and brand value',
			examples: [
				{
					name: 'Procter & Gamble',
					ticker: 'PG',
					multiple: '14-16x',
					historicalRange: '10-18x',
					notes: 'Premium for brand strength and stability',
					keyFactors: ['Pricing power', 'Innovation pipeline', 'Geographic mix']
				},
				{
					name: 'Kraft Heinz',
					ticker: 'KHC',
					multiple: '8-10x',
					historicalRange: '6-14x',
					notes: 'Lower multiple reflects growth challenges',
					keyFactors: ['Private label competition', 'Input costs', 'Brand investment']
				}
			],
			characteristics: ['Brand value', 'Distribution strength', 'Category leadership'],
			adjustmentFactors: [
				'Marketing spending',
				'Trade promotion accounting',
				'Restructuring costs'
			],
			whenToUse: [
				'Evaluating brand value',
				'Comparing operational efficiency',
				'Analyzing margin sustainability'
			]
		}
	};

	function getMultipleAnalysis(ratio: number): string {
		if (ratio > 20)
			return 'Premium valuation - verify growth sustainability and competitive advantages';
		if (ratio > 15)
			return 'Above average multiple - compare to peer group and assess margin sustainability';
		if (ratio > 10) return 'Moderate valuation - typical for stable businesses with good margins';
		return 'Below average multiple - investigate competitive position and cycle impact';
	}

	let selectedTab = $state('overview');
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="mb-6 text-center text-3xl font-bold text-green-400">
				EV/EBITDA Analysis Framework
			</Card.Title>
		</Card.Header>

		<Card.Content class="space-y-8">
			<Tabs.Root value={selectedTab} onValueChange={(value) => (selectedTab = value)}>
				<Tabs.List class="grid grid-cols-4">
					<Tabs.Trigger value="overview">Overview</Tabs.Trigger>
					<Tabs.Trigger value="calculator">Calculator</Tabs.Trigger>
					<Tabs.Trigger value="industries">Industries</Tabs.Trigger>
					<Tabs.Trigger value="application">Application</Tabs.Trigger>
				</Tabs.List>

				<!-- Overview Tab -->
				<Tabs.Content value="overview">
					<div class="space-y-6">
						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Understanding EV/EBITDA</h2>
							<p class="mb-4 text-lg text-slate-300">
								The "operating multiple" compares total enterprise value to operating earnings
								power. Key benefits include:
							</p>
							<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Capital Structure Neutral</h3>
									<p class="text-slate-300">
										Enterprise Value normalizes for different debt levels
									</p>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Operating Focus</h3>
									<p class="text-slate-300">EBITDA highlights core earnings power</p>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Comparable Analysis</h3>
									<p class="text-slate-300">Removes accounting and tax differences</p>
								</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Key Considerations</h2>
							<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">When to Use</h3>
									<ul class="ml-6 list-disc text-slate-300">
										<li>Capital intensive businesses</li>
										<li>Mature companies with positive EBITDA</li>
										<li>Cross-industry comparisons</li>
										<li>Companies with different tax rates</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Limitations</h3>
									<ul class="ml-6 list-disc text-slate-300">
										<li>Ignores working capital needs</li>
										<li>Doesn't reflect capex requirements</li>
										<li>May overstate true earnings power</li>
										<li>Less relevant for growth companies</li>
									</ul>
								</div>
							</div>
						</section>
					</div>
				</Tabs.Content>

				<!-- Calculator Tab -->
				<Tabs.Content value="calculator">
					<div class="space-y-6">
						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">EBITDA Construction</h2>
							<!-- Revenue and COGS -->
							<div class="mb-4 grid grid-cols-2 gap-4">
								<div>
									<label for="revenue" class="block text-sm text-slate-300">Revenue ($M)</label>
									<input
										id="revenue"
										type="number"
										bind:value={revenue}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label for="cogs" class="block text-sm text-slate-300">Cost of Goods ($M)</label>
									<input
										id="cogs"
										type="number"
										bind:value={costOfGoods}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
							</div>

							<div class="mb-4 rounded-lg bg-slate-700 p-3">
								<div class="flex justify-between">
									<span class="text-slate-300">Gross Profit:</span>
									<span class="font-bold text-green-400">${grossProfit}M</span>
								</div>
								<div class="text-sm text-slate-400">
									Margin: {grossMargin.toFixed(1)}%
								</div>
							</div>

							<!-- Operating Expenses and Add-backs -->
							<div class="grid grid-cols-3 gap-4">
								<div>
									<label for="opex" class="block text-sm text-slate-300"
										>Operating Expenses ($M)</label
									>
									<input
										id="opex"
										type="number"
										bind:value={operatingExpenses}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label for="depr" class="block text-sm text-slate-300">Depreciation ($M)</label>
									<input
										id="depr"
										type="number"
										bind:value={depreciation}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label for="amort" class="block text-sm text-slate-300">Amortization ($M)</label>
									<input
										id="amort"
										type="number"
										bind:value={amortization}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
							</div>

							<div class="mt-4 rounded-lg bg-slate-700 p-3">
								<div class="flex justify-between">
									<span class="text-slate-300">EBITDA:</span>
									<span class="font-bold text-green-400">${ebitda}M</span>
								</div>
								<div class="text-sm text-slate-400">
									Margin: {ebitdaMargin.toFixed(1)}%
								</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Enterprise Value Components</h2>
							<div class="grid grid-cols-3 gap-4">
								<div>
									<label for="mcap" class="block text-sm text-slate-300">Market Cap ($M)</label>
									<input
										id="mcap"
										type="number"
										bind:value={marketCap}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								[Previous code remains the same until the Enterprise Value Components section...]

								<div>
									<label for="debt" class="block text-sm text-slate-300">Total Debt ($M)</label>
									<input
										id="debt"
										type="number"
										bind:value={debt}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
								<div>
									<label for="cash" class="block text-sm text-slate-300">Cash ($M)</label>
									<input
										id="cash"
										type="number"
										bind:value={cash}
										class="mt-1 w-full rounded bg-slate-600 p-2 text-white"
									/>
								</div>
							</div>

							<div class="mt-4 rounded-lg bg-slate-700 p-3">
								<div class="flex justify-between">
									<span class="text-slate-300">Enterprise Value:</span>
									<span class="font-bold text-green-400">${ev}M</span>
								</div>
								<div class="text-sm text-slate-400">Market Cap + Total Debt - Cash</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Multiple Analysis</h2>
							<div class="text-center">
								<div class="mb-2 text-3xl font-bold text-green-400">
									{evToEbitda.toFixed(1)}x
								</div>
								<p class="text-slate-300">EV/EBITDA Multiple</p>
							</div>

							<Alert.Root class="mt-4">
								<Alert.Description>
									{getMultipleAnalysis(evToEbitda)}
								</Alert.Description>
							</Alert.Root>
						</section>
					</div>
				</Tabs.Content>

				<!-- Industries Tab -->
				<Tabs.Content value="industries">
					<div class="space-y-4">
						{#each Object.entries(industryPatterns) as [key, industry]}
							<section class="rounded-lg bg-slate-800 p-6">
								<h2 class="mb-4 text-xl text-green-400">{industry.type}</h2>

								<div class="mb-4">
									<span class="text-slate-400">Typical Range:</span>
									<span class="ml-2 text-xl font-bold text-green-400">{industry.range}</span>
								</div>

								<div class="grid gap-4 md:grid-cols-2">
									{#each industry.examples as company}
										<div class="rounded-lg bg-slate-700 p-4">
											<div class="mb-2">
												<span class="font-bold text-green-400">{company.name}</span>
												<span class="ml-2 text-sm text-slate-400">({company.ticker})</span>
											</div>
											<div class="mb-2 text-sm">
												<span class="text-slate-400">Multiple:</span>
												<span class="ml-2 text-slate-300">{company.multiple}</span>
											</div>
											<div class="mb-2 text-sm">
												<span class="text-slate-400">Historical Range:</span>
												<span class="ml-2 text-slate-300">{company.historicalRange}</span>
											</div>
											<p class="mb-2 text-sm text-slate-300">{company.notes}</p>
											<div class="text-sm">
												<div class="text-slate-400">Key Drivers:</div>
												<ul class="ml-4 list-disc">
													{#each company.keyFactors as factor}
														<li class="text-slate-300">{factor}</li>
													{/each}
												</ul>
											</div>
										</div>
									{/each}
								</div>

								<div class="mt-4">
									<h3 class="mb-2 text-lg text-green-400">Analysis Framework</h3>
									<div class="grid gap-4 md:grid-cols-2">
										<div class="rounded-lg bg-slate-700 p-4">
											<h4 class="mb-2 font-medium text-green-400">Characteristics</h4>
											<ul class="ml-4 list-disc">
												{#each industry.characteristics as trait}
													<li class="text-slate-300">{trait}</li>
												{/each}
											</ul>
										</div>
										<div class="rounded-lg bg-slate-700 p-4">
											<h4 class="mb-2 font-medium text-green-400">Adjustment Factors</h4>
											<ul class="ml-4 list-disc">
												{#each industry.adjustmentFactors as factor}
													<li class="text-slate-300">{factor}</li>
												{/each}
											</ul>
										</div>
									</div>
								</div>
							</section>
						{/each}
					</div>
				</Tabs.Content>

				<!-- Application Tab -->
				<Tabs.Content value="application">
					<div class="space-y-6">
						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Analysis Framework</h2>
							<div class="grid gap-4 md:grid-cols-3">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Quality Assessment</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Margin sustainability</li>
										<li>Market position</li>
										<li>Revenue visibility</li>
										<li>Working capital efficiency</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Growth Analysis</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Organic vs acquired</li>
										<li>Market growth rate</li>
										<li>Share gain potential</li>
										<li>Reinvestment needs</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Risk Factors</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Cyclical exposure</li>
										<li>Competitive threats</li>
										<li>Regulatory changes</li>
										<li>Capital structure</li>
									</ul>
								</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Key Adjustment Considerations</h2>
							<div class="space-y-4">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Operating Adjustments</h3>
									<ul class="ml-6 list-disc text-slate-300">
										<li>Normalize for one-time items</li>
										<li>Adjust for restructuring costs</li>
										<li>Consider stock compensation impact</li>
										<li>Standardize accounting policies</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Capital Structure Impact</h3>
									<ul class="ml-6 list-disc text-slate-300">
										<li>Evaluate lease obligations</li>
										<li>Consider pension liabilities</li>
										<li>Assess working capital financing</li>
										<li>Analyze off-balance sheet items</li>
									</ul>
								</div>
							</div>
						</section>
					</div>
				</Tabs.Content>
			</Tabs.Root>
		</Card.Content>
	</Card.Root>
</div>
