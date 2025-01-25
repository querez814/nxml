<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">Understanding Cash Flow</h1>

			<div class="mb-6 font-mono text-sm text-gray-300">
				The cash flow statement tracks money moving in and out of a company through operations,
				investments, and financing activities.
			</div>

			<div class="grid grid-cols-1 gap-6 lg:grid-cols-4">
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Operating Activities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">OPERATING CASH FLOW</div>
								<div class="font-mono text-sm text-gray-300">
									Cash from core business operations
								</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Customer payments received</li>
									<li>Supplier payments made</li>
									<li>Employee wages paid</li>
									<li>Operating expenses paid</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">WORKING CAPITAL</div>
								<div class="font-mono text-sm text-gray-300">Short-term operational changes</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Inventory fluctuations</li>
									<li>Accounts receivable changes</li>
									<li>Accounts payable changes</li>
									<li>Other current asset/liability changes</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">NON-CASH ITEMS</div>
								<div class="font-mono text-sm text-gray-300">
									Adjustments for accounting entries
								</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Depreciation & Amortization</li>
									<li>Stock-based compensation</li>
									<li>Asset write-downs</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Investing Activities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">CAPITAL EXPENDITURES</div>
								<div class="font-mono text-sm text-gray-300">Long-term asset investments</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Property & building purchases</li>
									<li>Equipment & machinery</li>
									<li>Technology infrastructure</li>
									<li>Major upgrades/maintenance</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">INVESTMENTS</div>
								<div class="font-mono text-sm text-gray-300">
									Financial investments & acquisitions
								</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Securities purchases/sales</li>
									<li>Business acquisitions/disposals</li>
									<li>Investment proceeds</li>
									<li>Joint ventures</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">IMPACT ANALYSIS</div>
								<div class="font-mono text-sm text-gray-300">Investment strategy indicators</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Growth vs maintenance capex</li>
									<li>Investment intensity</li>
									<li>Return on invested capital</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Financing Activities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">DEBT ACTIVITIES</div>
								<div class="font-mono text-sm text-gray-300">Borrowing and repayment</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>New debt issuance</li>
									<li>Debt repayment</li>
									<li>Interest payments</li>
									<li>Lease payments</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">EQUITY ACTIVITIES</div>
								<div class="font-mono text-sm text-gray-300">Shareholder transactions</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Stock issuance</li>
									<li>Share buybacks</li>
									<li>Dividend payments</li>
									<li>Capital raising</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">FINANCING STRATEGY</div>
								<div class="font-mono text-sm text-gray-300">Capital structure choices</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Leverage decisions</li>
									<li>Shareholder returns</li>
									<li>Capital allocation</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Key Ratios & Analysis</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">OPERATING CASH FLOW RATIO</div>
								<div class="font-mono text-sm text-gray-300">OCF / Current Liabilities</div>
								<div class="font-mono text-xs text-gray-400">Short-term debt coverage</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Interpretation:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>1.0: Strong cash generation</li>
									<li>1.0: Potential liquidity issues</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">CASH FLOW COVERAGE</div>
								<div class="font-mono text-sm text-gray-300">OCF / (LT Debt + Interest)</div>
								<div class="font-mono text-xs text-gray-400">Long-term obligation coverage</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>1.5: Healthy coverage</li>
									<li>1.0: Debt service risk</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">FREE CASH FLOW YIELD</div>
								<div class="font-mono text-sm text-gray-300">FCF / Market Cap</div>
								<div class="font-mono text-xs text-gray-400">Cash generation efficiency</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>8%: Potentially undervalued</li>
									<li>4%: Possibly overvalued</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">QUALITY INDICATORS</div>
								<div class="font-mono text-sm text-gray-300">Cash flow health checks</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>OCF vs Net Income trends</li>
									<li>FCF conversion rate</li>
									<li>Working capital efficiency</li>
									<li>Cash flow sustainability</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
