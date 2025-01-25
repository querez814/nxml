<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

```svelte
<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">
				Understanding Cash Flow Analysis
			</h1>

			<div class="mb-6 font-mono text-sm text-gray-300">
				Cash flow metrics reveal a company's ability to generate cash, fund operations, and invest
				in growth. Below are the key metrics and their interpretations.
			</div>

			<div class="grid grid-cols-1 gap-6 md:grid-cols-3">
				<!-- Operating Margins -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Operating Margins</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">NET PROFIT MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Net Income / Revenue</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Industry Benchmarks:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Tech: >15% excellent</li>
									<li>Retail: >5% strong</li>
									<li>Your 23.6%: Very healthy</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">OCF MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Operating Cash Flow / Revenue</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Interpretation:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>>10%: Strong cash generation</li>
									<li>5-10%: Healthy operations</li>
									<li>Your 9.2%: Solid performance</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">FCF MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Free Cash Flow / Revenue</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Analysis:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>>7%: Strong cash retention</li>
									<li>Your 7.3%: Above target</li>
									<li>Shows efficient operations</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<!-- Efficiency Metrics -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Return & Efficiency</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">ROCE</div>
								<div class="font-mono text-sm text-gray-300">EBIT / Capital Employed</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Target Ranges:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>>15%: Excellent efficiency</li>
									<li>8-15%: Good performance</li>
									<li>Your 5.84: Moderate returns</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CASH FLOW ADEQUACY</div>
								<div class="font-mono text-sm text-gray-300">OCF / (Debt + Capex + Dividends)</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Assessment:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>>1.0: Strong coverage</li>
									<li>Your -1.09: Cash flow strain</li>
									<li>Watch debt coverage</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CAPEX RATIO</div>
								<div class="font-mono text-sm text-gray-300">OCF / Capital Expenditures</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Interpretation:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>>2.0: Strong investment ability</li>
									<li>Your 4.76: Excellent coverage</li>
									<li>Room for more investment</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<!-- Trends & Analysis -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Trend Analysis</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">MARGIN TRENDS</div>
								<div class="font-mono text-sm text-gray-300">Period-over-Period Changes</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Key Observations:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Net margin improving: 23.6% → 122.8%</li>
									<li>OCF margin stable: ~9%</li>
									<li>FCF margin consistent: ~7%</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">EFFICIENCY PATTERNS</div>
								<div class="font-mono text-sm text-gray-300">Operational Effectiveness</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Analysis:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>ROCE improving: 0.87 → 5.84</li>
									<li>Capex ratio increasing</li>
									<li>Cash adequacy needs attention</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">RECOMMENDATIONS</div>
								<div class="font-mono text-sm text-gray-300">Action Items</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Monitor cash adequacy</li>
									<li>Consider debt management</li>
									<li>Maintain strong margins</li>
									<li>Optimize capital allocation</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
```
