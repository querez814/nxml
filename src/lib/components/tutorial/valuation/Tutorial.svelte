<script lang="ts">
	import { DollarSign, AlertCircle, TrendingUp } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Alert from '$lib/components/ui/alert';
	import * as Tabs from '$lib/components/ui/tabs';

	interface CompanyExample {
		name: string;
		notes: string;
		typicalMultiple?: string;
		historicalRange?: string;
		keyFactors?: string[];
	}

	interface IndustryBenchmark {
		range: string;
		examples: CompanyExample[];
		interpretation: string;
		applicationTips: string;
		cyclical?: {
			range: string;
			notes: string;
		};
		keyMetrics?: string[];
	}

	let revenue = $state(100);
	let marketCap = $state(500);
	let debt = $state(50);
	let cash = $state(30);

	let ev = $derived(marketCap + debt - cash);
	let evToSales = $derived(ev / revenue);

	let activeTab = $state('semiconductors');

	const industryBenchmarks: Record<string, IndustryBenchmark> = {
		semiconductors: {
			range: '2-6x',
			cyclical: {
				range: '1-3x',
				notes: 'Highly cyclical with significant multiple expansion/contraction through cycles'
			},
			examples: [
				{
					name: 'Micron (MU)',
					notes: 'Pure-play memory manufacturer - highly cyclical',
					typicalMultiple: '1.5-3x',
					historicalRange: '0.8-4.2x',
					keyFactors: ['DRAM pricing cycles', 'Bit growth', 'Node transitions']
				},
				{
					name: 'AMKOR (AMKR)',
					notes: 'Semiconductor packaging and test services',
					typicalMultiple: '0.5-1x',
					historicalRange: '0.3-1.5x',
					keyFactors: ['Capital intensity', 'Advanced packaging mix', 'Utilization rates']
				},
				{
					name: 'AMD (AMD)',
					notes: 'High-performance computing and graphics',
					typicalMultiple: '6-8x',
					historicalRange: '1-12x',
					keyFactors: ['Market share gains', 'Data center growth', 'Product cycles']
				}
			],
			interpretation:
				'Focus on cycle-adjusted metrics and industry position. Key is understanding where we are in both company-specific and industry-wide cycles.',
			applicationTips:
				'Compare to historical averages, peer group positioning, and current cycle indicators.',
			keyMetrics: [
				'Book-to-bill ratio',
				'Inventory levels',
				'Capacity utilization',
				'Pricing trends'
			]
		},
		industrials: {
			range: '1.5-3x',
			cyclical: {
				range: '1-2x',
				notes: 'Moderate cyclicality tied to capital spending and economic cycles'
			},
			examples: [
				{
					name: 'Rockwell (ROK)',
					notes: 'Industrial automation leader',
					typicalMultiple: '3-4x',
					historicalRange: '1.5-5x',
					keyFactors: ['Software mix', 'Recurring revenue', 'Manufacturing automation trends']
				},
				{
					name: 'Cummins (CMI)',
					notes: 'Engine and power systems manufacturer',
					typicalMultiple: '1.2-1.8x',
					historicalRange: '0.8-2.5x',
					keyFactors: ['Truck cycle position', 'Emission regulations', 'Market share']
				},
				{
					name: 'Parker Hannifin (PH)',
					notes: 'Motion and control technologies',
					typicalMultiple: '1.8-2.5x',
					historicalRange: '1-3x',
					keyFactors: ['Aerospace exposure', 'Aftermarket mix', 'Operating margins']
				}
			],
			interpretation:
				'Consider capital spending cycles, end market exposure, and secular growth drivers.',
			applicationTips: 'Monitor order rates, backlog trends, and key end market indicators.',
			keyMetrics: ['Book-to-bill', 'Backlog coverage', 'PMI readings', 'Capital spending forecasts']
		},
		software: {
			range: '6-20x',
			examples: [
				{
					name: 'Microsoft (MSFT)',
					notes: 'Enterprise software and cloud leader',
					typicalMultiple: '10-12x',
					historicalRange: '3-15x',
					keyFactors: ['Cloud growth', 'Operating leverage', 'Enterprise spending']
				},
				{
					name: 'ServiceNow (NOW)',
					notes: 'Enterprise workflow automation',
					typicalMultiple: '15-20x',
					historicalRange: '12-25x',
					keyFactors: ['Subscription growth', 'Net retention', 'Operating margins']
				},
				{
					name: 'Oracle (ORCL)',
					notes: 'Enterprise software and cloud',
					typicalMultiple: '5-7x',
					historicalRange: '3-8x',
					keyFactors: ['Cloud transition', 'Database market share', 'Maintenance revenue']
				}
			],
			interpretation:
				'Growth and profitability profile key drivers of multiple. Focus on ARR growth, retention, and margin expansion potential.',
			applicationTips:
				'Analyze growth sustainability, competitive position, and path to profitability.',
			keyMetrics: ['ARR growth', 'Net retention rate', 'Gross margins', 'Rule of 40']
		},
		manufacturing: {
			range: '1-2x',
			cyclical: {
				range: '0.5-1.5x',
				notes: 'Significant cyclical exposure and capital intensity'
			},
			examples: [
				{
					name: 'Deere (DE)',
					notes: 'Agricultural and construction equipment',
					typicalMultiple: '1.8-2.2x',
					historicalRange: '0.8-2.5x',
					keyFactors: ['Ag cycles', 'Technology adoption', 'Services revenue']
				},
				{
					name: 'Stanley Black & Decker (SWK)',
					notes: 'Tools and storage products',
					typicalMultiple: '1.2-1.6x',
					historicalRange: '0.8-2x',
					keyFactors: ['Housing market', 'Channel inventory', 'Professional mix']
				}
			],
			interpretation:
				'Capital intensity and cyclical exposure drive lower multiples. Focus on cycle position and competitive advantages.',
			applicationTips: 'Evaluate cycle position, market share trends, and margin sustainability.',
			keyMetrics: [
				'Capacity utilization',
				'Order trends',
				'Channel inventory',
				'Raw material costs'
			]
		}
	};

	function getMultipleAnalysis(ratio: number, industry?: string): string {
		const baseAnalysis = industry
			? `Current multiple of ${ratio.toFixed(1)}x relative to ${industry} range of ${industryBenchmarks[industry]?.range}`
			: `Multiple of ${ratio.toFixed(1)}x indicates `;

		if (ratio > 15)
			return `${baseAnalysis} premium valuation - verify growth sustainability and margin profile`;
		if (ratio > 8)
			return `${baseAnalysis} above average - compare to peer group and growth profile`;
		if (ratio > 3) return `${baseAnalysis} moderate range - typical for stable businesses`;
		return `${baseAnalysis} below average - investigate cyclical factors or potential challenges`;
	}
</script>

<Card.Root class="w-full max-w-4xl">
	<Card.Header>
		<Card.Title>EV/Sales Analysis Framework</Card.Title>
		<Card.Description>
			Understanding valuation multiples across different business models and cycles
		</Card.Description>
	</Card.Header>

	<Card.Content class="space-y-6">
		<!-- Theory Section -->
		<div class="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
			<h3 class="mb-4 text-lg font-semibold">Key Principles</h3>
			<div class="space-y-2">
				<p>EV/Sales multiples vary significantly across sectors based on:</p>
				<div class="grid gap-4 md:grid-cols-3">
					<div class="rounded-lg bg-white p-3 dark:bg-slate-700">
						<h4 class="font-medium">Growth Profile</h4>
						<p class="text-sm">Revenue growth rate and sustainability drive expansion potential</p>
					</div>
					<div class="rounded-lg bg-white p-3 dark:bg-slate-700">
						<h4 class="font-medium">Margin Structure</h4>
						<p class="text-sm">Higher margins typically justify higher multiples</p>
					</div>
					<div class="rounded-lg bg-white p-3 dark:bg-slate-700">
						<h4 class="font-medium">Business Quality</h4>
						<p class="text-sm">Consider moat, capital intensity, and revenue visibility</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Calculator Section -->
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
			<div class="space-y-4">
				<!-- Inputs -->
				<div class="space-y-2">
					<label for="revenue" class="block text-sm font-medium"> Annual Revenue ($M) </label>
					<input
						id="revenue"
						type="number"
						bind:value={revenue}
						class="w-full rounded border p-2"
						min="0"
					/>
				</div>

				<div class="space-y-2">
					<label for="marketCap" class="block text-sm font-medium"> Market Cap ($M) </label>
					<input
						id="marketCap"
						type="number"
						bind:value={marketCap}
						class="w-full rounded border p-2"
						min="0"
					/>
				</div>

				<div class="space-y-2">
					<label for="debt" class="block text-sm font-medium"> Total Debt ($M) </label>
					<input
						id="debt"
						type="number"
						bind:value={debt}
						class="w-full rounded border p-2"
						min="0"
					/>
				</div>

				<div class="space-y-2">
					<label for="cash" class="block text-sm font-medium"> Cash ($M) </label>
					<input
						id="cash"
						type="number"
						bind:value={cash}
						class="w-full rounded border p-2"
						min="0"
					/>
				</div>
			</div>

			<!-- Results Panel -->
			<div class="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
				<div class="mb-4">
					<h3 class="text-lg font-semibold">Analysis</h3>
					<div class="mt-2 space-y-2">
						<div class="text-sm">Enterprise Value</div>
						<div class="text-2xl font-bold">${ev}M</div>
						<div class="text-sm">EV/Sales Ratio</div>
						<div class="text-2xl font-bold">{evToSales.toFixed(1)}x</div>
					</div>
				</div>

				<Alert.Root>
					<Alert.Description>
						{getMultipleAnalysis(evToSales, activeTab)}
					</Alert.Description>
				</Alert.Root>
			</div>
		</div>

		<!-- Industry Reference -->
		<Tabs.Root value={activeTab}>
			<Tabs.List>
				{#each Object.keys(industryBenchmarks) as industry}
					<Tabs.Trigger value={industry} on:click={() => (activeTab = industry)}>
						{industry}
					</Tabs.Trigger>
				{/each}
			</Tabs.List>

			{#each Object.entries(industryBenchmarks) as [industry, data]}
				<Tabs.Content value={industry}>
					<div class="space-y-4">
						<div class="mb-4">
							<h3 class="text-lg font-semibold capitalize">{industry}</h3>
							<p class="text-sm">{data.interpretation}</p>
						</div>

						<!-- Industry Ranges -->
						<div class="rounded-lg bg-white p-4 dark:bg-slate-700">
							<div class="mb-4">
								<h4 class="font-medium">Valuation Ranges</h4>
								<p class="text-sm">Typical Range: {data.range}</p>
								{#if data.cyclical}
									<p class="mt-1 text-sm">
										Cyclical Range: {data.cyclical.range}
										<br />
										{data.cyclical.notes}
									</p>
								{/if}
							</div>

							{#if data.keyMetrics}
								<div class="mt-2">
									<h4 class="font-medium">Key Metrics to Monitor</h4>
									<div class="mt-1 text-sm">
										{data.keyMetrics.join(' • ')}
									</div>
								</div>
							{/if}
						</div>

						<!-- Company Examples -->
						<div class="grid gap-4 md:grid-cols-2">
							{#each data.examples as example}
								<div class="rounded-lg bg-white p-4 dark:bg-slate-700">
									<div class="mb-2">
										<span class="font-medium">{example.name}</span>
										{#if example.typicalMultiple}
											<span class="ml-2 text-sm">
												Typical: {example.typicalMultiple}
											</span>
										{/if}
									</div>
									<p class="mb-2 text-sm">{example.notes}</p>
									{#if example.historicalRange}
										<div class="text-sm">
											Historical Range: {example.historicalRange}
										</div>
									{/if}
									{#if example.keyFactors}
										<div class="mt-2 text-sm">
											<span class="font-medium">Key Factors:</span>
											<div class="mt-1">
												{example.keyFactors.join(' • ')}
											</div>
										</div>
									{/if}
								</div>
							{/each}
						</div>
					</div>
				</Tabs.Content>
			{/each}
		</Tabs.Root>
	</Card.Content>
</Card.Root>
