<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	let revenue = $state(100);
	let cogs = $state(50);
	let grossProfit = $derived(revenue - cogs);
</script>

<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">
				Understanding The Income Statement
			</h1>

			<div class="mb-12 font-mono text-sm text-gray-300">
				The income statement reveals a company's financial performance by showing revenues, costs,
				and profitability over a specific period (quarterly or annually). Each line item tells part
				of the company's financial story, and that story drives the movement of the assets price
			</div>

			<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Revenue & Direct Costs</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">TOTAL REVENUE</div>
								<div class="font-mono text-sm text-gray-300">
									All income from sales of products/services before any costs
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Includes:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Product sales revenue</li>
									<li>Service revenue</li>
									<li>Subscription income</li>
									<li>Licensing fees</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">COST OF REVENUE (COGS)</div>
								<div class="font-mono text-sm text-gray-300">
									Direct costs associated with delivering products/services
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Examples:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Raw materials</li>
									<li>Direct labor costs</li>
									<li>Manufacturing overhead</li>
									<li>Cloud hosting costs</li>
									<li>Product shipping</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">GROSS PROFIT</div>
								<div class="font-mono text-sm text-gray-300">
									Revenue - Cost of Revenue = Core profitability
								</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Indicates how efficiently a company converts revenue into profit before other
									expenses
								</div>
							</div>
						</div>
					</div>
				</Card.Root>

				<!-- Operating Expenses -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Operating Expenses & Income</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">SG&A EXPENSES</div>
								<div class="font-mono text-sm text-gray-300">
									Selling, General & Administrative costs
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Includes:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Marketing & advertising</li>
									<li>Office expenses</li>
									<li>Executive salaries</li>
									<li>Legal & accounting</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">R&D EXPENSES</div>
								<div class="font-mono text-sm text-gray-300">
									Research & Development investments
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Examples:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Product development</li>
									<li>Research costs</li>
									<li>Engineering salaries</li>
									<li>Testing & prototypes</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">OPERATING INCOME</div>
								<div class="font-mono text-sm text-gray-300">Gross Profit - Operating Expenses</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Shows profitability from core business operations
								</div>
							</div>
						</div>
					</div>
				</Card.Root>

				<!-- EBITDA & Other Income -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">EBITDA & Other Metrics</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">EBITDA</div>
								<div class="font-mono text-sm text-gray-300">
									Earnings Before Interest, Taxes, Depreciation & Amortization
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Importance:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Measures operational performance</li>
									<li>Excludes financing decisions</li>
									<li>Comparable across companies</li>
									<li>Key metric for valuations</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">OTHER INCOME/EXPENSES</div>
								<div class="font-mono text-sm text-gray-300">Non-operational financial items</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Examples:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Interest expenses</li>
									<li>Investment income</li>
									<li>Foreign exchange gains/losses</li>
									<li>One-time charges</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<!-- Bottom Line Metrics -->
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Net Income & Per Share</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">NET INCOME</div>
								<div class="font-mono text-sm text-gray-300">
									The final profit/loss after all expenses
								</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Key Points:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Bottom line earnings</li>
									<li>After tax profits</li>
									<li>Available for dividends</li>
									<li>Reinvestment potential</li>
								</ul>
							</div>
							<div>
								<div class="font-mono text-xs text-gray-500">EARNINGS PER SHARE (EPS)</div>
								<div class="font-mono text-sm text-gray-300">Net Income ÷ Outstanding Shares</div>
								<div class="mt-1 font-mono text-xs text-gray-500">Types:</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Basic EPS (simple division)</li>
									<li>Diluted EPS (includes options)</li>
									<li>Adjusted EPS (non-GAAP)</li>
									<li>TTM EPS (trailing 12 months)</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
