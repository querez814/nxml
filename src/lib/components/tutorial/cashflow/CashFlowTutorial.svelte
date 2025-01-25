<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

```svelte
<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">Understanding Cash Flow</h1>

			<div class="grid grid-cols-1 gap-6 lg:grid-cols-4">
				<!-- First three columns same as before -->

				<!-- New Ratios Column -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Key Ratios & Analysis</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">OPERATING CASH FLOW RATIO</div>
								<div class="font-mono text-sm text-gray-300">
									Operating Cash Flow / Current Liabilities
								</div>
								<div class="font-mono text-xs text-gray-400">
									Measures ability to cover short-term debts with operating cash
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Interpretation:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Above 1.0: Strong cash generation</li>
									<li>Below 1.0: Potential liquidity issues</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CASH FLOW COVERAGE RATIO</div>
								<div class="font-mono text-sm text-gray-300">
									Operating Cash Flow / (Long-term Debt + Interest + Lease Payments)
								</div>
								<div class="font-mono text-xs text-gray-400">
									Shows ability to meet long-term obligations
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Target Ranges:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>1.5: Healthy coverage</li>
									<li>1.0: Debt service risk</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">FREE CASH FLOW YIELD</div>
								<div class="font-mono text-sm text-gray-300">
									Free Cash Flow / Market Capitalization
								</div>
								<div class="font-mono text-xs text-gray-400">
									Cash generating efficiency relative to size
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Benchmarks:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>8%: Potentially undervalued</li>
									<li>4%: May be overvalued</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CAPEX TO OPERATING CASH</div>
								<div class="font-mono text-sm text-gray-300">
									Capital Expenditures / Operating Cash Flow
								</div>
								<div class="font-mono text-xs text-gray-400">
									Investment intensity of operations
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Analysis:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>High ratio: Growth investment</li>
									<li>Low ratio: Mature business</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
