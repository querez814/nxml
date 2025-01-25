<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">Understanding Cash Flow</h1>

			<div class="grid grid-cols-1 gap-6 lg:grid-cols-4">
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Operating Activities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">OPERATING CASH FLOW</div>
								<div class="font-mono text-sm text-gray-300">Core business cash generation</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Revenue collection minus operating costs</li>
									<li>Primary measure of cash sustainability</li>
									<li>Key for operational health</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CASH PAYMENTS</div>
								<div class="font-mono text-sm text-gray-300">Operating cash outflows</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Supplier and vendor payments</li>
									<li>Employee compensation</li>
									<li>Day-to-day expenses</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">WORKING CAPITAL</div>
								<div class="font-mono text-sm text-gray-300">
									Short-term operational assets/liabilities
								</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Inventory management</li>
									<li>Customer payment timing</li>
									<li>Supplier payment terms</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Investment Activities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">CAPITAL EXPENDITURE</div>
								<div class="font-mono text-sm text-gray-300">Long-term investments</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Property and equipment purchases</li>
									<li>Infrastructure development</li>
									<li>Growth investments</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">ACQUISITIONS & DISPOSALS</div>
								<div class="font-mono text-sm text-gray-300">Business investment changes</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Business purchases/sales</li>
									<li>Asset acquisitions/disposals</li>
									<li>Investment portfolio changes</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">INVESTMENT RETURNS</div>
								<div class="font-mono text-sm text-gray-300">Income from investments</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Interest received</li>
									<li>Investment proceeds</li>
									<li>Asset sale gains/losses</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Margin Analysis</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">NET PROFIT MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Net Income / Revenue</div>
								<div class="mt-1 font-mono text-xs text-gray-400">Interpretation:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>High:20% (exceptional)</li>
									<li>Good: 10-20%</li>
									<li>Average: 5-10%</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">OCF MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Operating Cash / Revenue</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Strong: 10%</li>
									<li>Healthy: 5-10%</li>
									<li>Weak: 5%</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">FCF MARGIN</div>
								<div class="font-mono text-sm text-gray-300">Free Cash Flow / Revenue</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Strong: 7%</li>
									<li>Healthy: 4-7%</li>
									<li>Weak: 4%</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Efficiency Metrics</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">ROCE</div>
								<div class="font-mono text-sm text-gray-300">Return on Capital Employed</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Excellent: 15%</li>
									<li>Good: 8-15%</li>
									<li>Poor: 8%</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CASH ADEQUACY</div>
								<div class="font-mono text-sm text-gray-300">OCF Coverage Ratio</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Strong: 1.5</li>
									<li>Adequate: 1.0-1.5</li>
									<li>Weak: 1.0</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CAPEX RATIO</div>
								<div class="font-mono text-sm text-gray-300">OCF / Capital Expenditures</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Strong: 3.0</li>
									<li>Adequate: 1.5-3.0</li>
									<li>Weak: 1.5</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
