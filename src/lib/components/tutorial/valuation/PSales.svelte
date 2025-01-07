<script lang="ts">
	import { DollarSign, BookOpen, TrendingUp, CircleDollarSign } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Alert from '$lib/components/ui/alert';

	interface CompanyExample {
		name: string;
		ticker: string;
		multiple: string;
		historicalRange: string;
		notes: string;
		metrics: {
			growth: string;
			margins: string;
			nrr?: string;
		};
	}

	interface IndustryPattern {
		type: string;
		range: string;
		interpretation: string;
		examples: CompanyExample[];
		keyMetrics: string[];
		analysis: string[];
	}

	let annualRevenue = $state(100);
	let stockPrice = $state(20);
	let sharesOutstanding = $state(10);
	let growthRate = $state(40);
	let grossMargin = $state(75);
	let nrr = $state(120);

	let marketCap = $derived(stockPrice * sharesOutstanding);
	let priceToSales = $derived(marketCap / annualRevenue);
	let ruleOf40Score = $derived(growthRate + grossMargin * 0.3);

	const industryPatterns: Record<string, IndustryPattern> = {
		hyperGrowth: {
			type: 'Hyper-Growth Software',
			range: '20-40x+',
			interpretation: 'Premium multiples for exceptional growth and margins',
			examples: [
				{
					name: 'Snowflake',
					ticker: 'SNOW',
					multiple: '25-35x',
					historicalRange: '20-80x',
					notes: 'Premium for data cloud leadership and consumption model',
					metrics: {
						growth: '65-85%',
						margins: '75%',
						nrr: '170%'
					}
				},
				{
					name: 'MongoDB',
					ticker: 'MDB',
					multiple: '20-30x',
					historicalRange: '15-40x',
					notes: 'Strong Atlas cloud growth and developer adoption',
					metrics: {
						growth: '45-55%',
						margins: '73%',
						nrr: '130%'
					}
				}
			],
			keyMetrics: ['Revenue growth >40%', 'Gross margins >75%', 'NRR >130%', 'Rule of 40 >60'],
			analysis: ['Market leadership position', 'Platform potential', 'Enterprise penetration']
		},
		establishedSaaS: {
			type: 'Established SaaS',
			range: '8-15x',
			interpretation: 'Balanced growth and profitability',
			examples: [
				{
					name: 'ServiceNow',
					ticker: 'NOW',
					multiple: '12-15x',
					historicalRange: '8-20x',
					notes: 'Premium for workflow automation dominance',
					metrics: {
						growth: '25-30%',
						margins: '78%',
						nrr: '125%'
					}
				},
				{
					name: 'Salesforce',
					ticker: 'CRM',
					multiple: '6-8x',
					historicalRange: '5-12x',
					notes: 'Scale impact on multiple',
					metrics: {
						growth: '20-25%',
						margins: '73%',
						nrr: '120%'
					}
				}
			],
			keyMetrics: ['Revenue growth 20-30%', 'Gross margins >70%', 'NRR >120%', 'Rule of 40 >40'],
			analysis: ['Enterprise penetration', 'Platform expansion', 'Operating leverage']
		},
		consumerTech: {
			type: 'Consumer Technology',
			range: '3-8x',
			interpretation: 'Network effects and scale drive valuation',
			examples: [
				{
					name: 'DoorDash',
					ticker: 'DASH',
					multiple: '4-6x',
					historicalRange: '3-15x',
					notes: 'Network effects in food delivery',
					metrics: {
						growth: '30-40%',
						margins: '50%'
					}
				},
				{
					name: 'Airbnb',
					ticker: 'ABNB',
					multiple: '8-10x',
					historicalRange: '6-15x',
					notes: 'Premium for brand and platform model',
					metrics: {
						growth: '20-30%',
						margins: '65%'
					}
				}
			],
			keyMetrics: ['GMV growth', 'Take rate trends', 'Unit economics', 'Network effects'],
			analysis: ['Market leadership', 'Platform stickiness', 'Category expansion']
		},
		ecommerce: {
			type: 'E-commerce',
			range: '1-3x',
			interpretation: 'Lower margins but valuable customer relationships',
			examples: [
				{
					name: 'Shopify',
					ticker: 'SHOP',
					multiple: '8-12x',
					historicalRange: '6-40x',
					notes: 'Premium for platform model vs pure retail',
					metrics: {
						growth: '25-35%',
						margins: '55%'
					}
				},
				{
					name: 'Wayfair',
					ticker: 'W',
					multiple: '0.5-1x',
					historicalRange: '0.3-3x',
					notes: 'Pure-play furniture retail model',
					metrics: {
						growth: '10-20%',
						margins: '30%'
					}
				}
			],
			keyMetrics: ['GMV growth', 'Customer retention', 'CAC trends', 'AOV'],
			analysis: ['Platform vs retail model', 'Category dynamics', 'Fulfillment efficiency']
		}
	};

	let selectedTab = $state('overview');

	function getMultipleAnalysis(ps: number, growth: number, margin: number): string {
		const ruleOf40 = growth + margin * 0.3;
		if (ps > 20)
			return `Premium multiple of ${ps.toFixed(1)}x - verify growth sustainability and competitive moat`;
		if (ps > 10)
			return `Above-average multiple of ${ps.toFixed(1)}x - compare growth profile to peers`;
		if (ps > 5)
			return `Moderate multiple of ${ps.toFixed(1)}x - typical for established growth companies`;
		return `Below-average multiple of ${ps.toFixed(1)}x - investigate growth trajectory and competitive position`;
	}
</script>

<div class="w-full max-w-4xl p-4">
	<Card.Root class="border-slate-700 bg-slate-900 text-white">
		<Card.Header>
			<Card.Title class="text-2xl font-bold text-green-400">
				Price to Sales Analysis Framework
			</Card.Title>
		</Card.Header>

		<Card.Content class="space-y-6">
			<Tabs.Root value={selectedTab}>
				<Tabs.List class="grid grid-cols-4">
					<Tabs.Trigger value="overview">Overview</Tabs.Trigger>
					<Tabs.Trigger value="calculator">Calculator</Tabs.Trigger>
					<Tabs.Trigger value="industries">Industry Patterns</Tabs.Trigger>
					<Tabs.Trigger value="analysis">Analysis Framework</Tabs.Trigger>
				</Tabs.List>

				<!-- Overview Tab -->
				<Tabs.Content value="overview">
					<div class="space-y-6">
						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">The Growth Company Metric</h2>
							<div class="grid gap-4 md:grid-cols-2">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Core Use Cases</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>High-growth, pre-profit companies</li>
										<li>SaaS and platform businesses</li>
										<li>Emerging technology sectors</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Key Advantages</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Revenue quality focus</li>
										<li>Growth rate emphasis</li>
										<li>Business model insights</li>
									</ul>
								</div>
							</div>
						</section>
					</div>
				</Tabs.Content>

				<!-- Calculator Tab -->
				<Tabs.Content value="calculator">
					<div class="space-y-6">
						<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
							<!-- Inputs -->
							<div class="space-y-4">
								<div>
									<label class="text-sm text-slate-300">Annual Revenue ($M)</label>
									<input
										type="number"
										bind:value={annualRevenue}
										class="mt-1 w-full rounded bg-slate-700 p-2"
									/>
								</div>
								<div>
									<label class="text-sm text-slate-300">Stock Price ($)</label>
									<input
										type="number"
										bind:value={stockPrice}
										class="mt-1 w-full rounded bg-slate-700 p-2"
									/>
								</div>
								<div>
									<label class="text-sm text-slate-300">Shares Outstanding (M)</label>
									<input
										type="number"
										bind:value={sharesOutstanding}
										class="mt-1 w-full rounded bg-slate-700 p-2"
									/>
								</div>
								<div>
									<label class="text-sm text-slate-300">Growth Rate (%)</label>
									<input
										type="number"
										bind:value={growthRate}
										class="mt-1 w-full rounded bg-slate-700 p-2"
									/>
								</div>
								<div>
									<label class="text-sm text-slate-300">Gross Margin (%)</label>
									<input
										type="number"
										bind:value={grossMargin}
										class="mt-1 w-full rounded bg-slate-700 p-2"
									/>
								</div>
							</div>

							<!-- Results -->
							<div class="rounded-lg bg-slate-800 p-6">
								<div class="mb-4">
									<div class="text-sm text-slate-300">Market Cap</div>
									<div class="text-2xl font-bold text-green-400">${marketCap}M</div>
								</div>
								<div class="mb-4">
									<div class="text-sm text-slate-300">P/S Ratio</div>
									<div class="text-3xl font-bold text-green-400">{priceToSales.toFixed(1)}x</div>
								</div>
								<div class="mb-4">
									<div class="text-sm text-slate-300">Rule of 40 Score</div>
									<div class="text-2xl font-bold text-green-400">{ruleOf40Score.toFixed(1)}%</div>
								</div>
								<Alert.Root>
									<Alert.Description>
										{getMultipleAnalysis(priceToSales, growthRate, grossMargin)}
									</Alert.Description>
								</Alert.Root>
							</div>
						</div>
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
									<p class="mt-2 text-slate-300">{industry.interpretation}</p>
								</div>

								<div class="grid gap-4 md:grid-cols-2">
									{#each industry.examples as company}
										<div class="rounded-lg bg-slate-700 p-4">
											<div class="mb-2">
												<span class="font-bold text-green-400">{company.name}</span>
												<span class="ml-2 text-sm text-slate-400">({company.ticker})</span>
											</div>
											<div class="mb-2 text-sm">
												<div>
													<span class="text-slate-400">Multiple:</span>
													<span class="ml-2 text-slate-300">{company.multiple}</span>
												</div>
												<div>
													<span class="text-slate-400">Historical Range:</span>
													<span class="ml-2 text-slate-300">{company.historicalRange}</span>
												</div>
											</div>
											<div class="mb-2 text-sm">
												<div>
													<span class="text-slate-400">Growth:</span>
													<span class="ml-2 text-slate-300">{company.metrics.growth}</span>
												</div>
												<div>
													<span class="text-slate-400">Margins:</span>
													<span class="ml-2 text-slate-300">{company.metrics.margins}</span>
												</div>
												{#if company.metrics.nrr}
													<div>
														<span class="text-slate-400">NRR:</span>
														<span class="ml-2 text-slate-300">{company.metrics.nrr}</span>
													</div>
												{/if}
											</div>
											<p class="text-sm text-slate-300">{company.notes}</p>
										</div>
									{/each}
								</div>

								<div class="mt-4">
									<div class="grid gap-4 md:grid-cols-2">
										<div class="rounded-lg bg-slate-700 p-4">
											<h4 class="mb-2 font-medium text-green-400">Key Metrics</h4>
											<ul class="ml-4 list-disc">
												{#each industry.keyMetrics as metric}
													<li class="text-slate-300">{metric}</li>
												{/each}
											</ul>
										</div>

										<div class="rounded-lg bg-slate-700 p-4">
											<h4 class="mb-2 font-medium text-green-400">Analysis Framework</h4>
											<ul class="ml-4 list-disc">
												{#each industry.analysis as point}
													<li class="text-slate-300">{point}</li>
												{/each}
											</ul>
										</div>
									</div>
								</div>
							</section>
						{/each}
					</div>
				</Tabs.Content>

				<!-- Analysis Framework Tab -->
				<Tabs.Content value="analysis">
					<div class="space-y-6">
						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Revenue Quality Analysis</h2>
							<div class="grid gap-4 md:grid-cols-3">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Growth Profile</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Organic vs inorganic</li>
										<li>Market share trends</li>
										<li>TAM penetration</li>
										<li>Growth sustainability</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Business Model</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Revenue visibility</li>
										<li>Customer retention</li>
										<li>Platform potential</li>
										<li>Network effects</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Unit Economics</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Gross margins</li>
										<li>CAC efficiency</li>
										<li>LTV/CAC ratio</li>
										<li>Sales efficiency</li>
									</ul>
								</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Common Pitfalls</h2>
							<div class="grid gap-4 md:grid-cols-2">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Value Traps</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Declining market share</li>
										<li>Poor net revenue retention</li>
										<li>Competitive disruption risk</li>
										<li>Margin pressure</li>
									</ul>
								</div>
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Growth Traps</h3>
									<ul class="ml-4 list-disc text-slate-300">
										<li>Unsustainable growth rates</li>
										<li>High customer concentration</li>
										<li>Channel dependency</li>
										<li>Poor unit economics</li>
									</ul>
								</div>
							</div>
						</section>

						<section class="rounded-lg bg-slate-800 p-6">
							<h2 class="mb-4 text-xl text-green-400">Rule of 40 Framework</h2>
							<div class="space-y-4">
								<div class="rounded-lg bg-slate-700 p-4">
									<h3 class="mb-2 text-green-400">Score Interpretation</h3>
									<div class="grid gap-4 md:grid-cols-3">
										<div class="rounded bg-slate-800 p-3">
											<div class="font-medium text-green-400">60%</div>
											<p class="text-sm text-slate-300">Premium multiple justified</p>
										</div>
										<div class="rounded bg-slate-800 p-3">
											<div class="font-medium text-green-400">40-60%</div>
											<p class="text-sm text-slate-300">Solid performance</p>
										</div>
										<div class="rounded bg-slate-800 p-3">
											<div class="font-medium text-green-400">40%</div>
											<p class="text-sm text-slate-300">Needs improvement</p>
										</div>
									</div>
								</div>
							</div>
						</section>
					</div>
				</Tabs.Content>
			</Tabs.Root>
		</Card.Content>
	</Card.Root>
</div>
