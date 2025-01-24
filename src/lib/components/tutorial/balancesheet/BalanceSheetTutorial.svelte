<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

<div class="min-h-screen bg-[#0a0b0d] p-4">
	<Card.Root class="border-none bg-[#111215]">
		<div class="p-6">
			<h1 class="mb-8 font-mono text-3xl font-bold text-green-400">
				Understanding the Balance Sheet
			</h1>

			<div class="grid grid-cols-1 gap-6 md:grid-cols-3">
				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Assets</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">CURRENT ASSETS</div>
								<div class="font-mono text-sm text-gray-300">
									Liquid assets convertible to cash within 1 year
								</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Includes: Cash, Receivables, Inventory, Marketable Securities
								</div>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">NON-CURRENT ASSETS</div>
								<div class="font-mono text-sm text-gray-300">Long-term investments and assets</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Includes: Property & Equipment, Intangibles, Goodwill
								</div>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">ASSET RATIOS</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Return on Assets (ROA)</li>
									<li>Asset Turnover</li>
									<li>Quick Ratio</li>
									<li>Current Ratio</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Liabilities</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">CURRENT LIABILITIES</div>
								<div class="font-mono text-sm text-gray-300">Debts due within one year</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Includes: Accounts Payable, Short-term Debt, Current Portion of Long-term Debt
								</div>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">LONG-TERM LIABILITIES</div>
								<div class="font-mono text-sm text-gray-300">Obligations beyond one year</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Includes: Long-term Debt, Lease Obligations, Pension Liabilities
								</div>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">KEY METRICS</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Debt-to-Equity</li>
									<li>Interest Coverage</li>
									<li>Working Capital</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>

				<Card.Root class="bg-[#1a1b1e]">
					<div class="p-4">
						<h3 class="mb-4 font-mono text-lg text-green-400">Shareholders' Equity</h3>
						<div class="space-y-4">
							<div>
								<div class="font-mono text-xs text-gray-500">COMPONENTS</div>
								<div class="font-mono text-sm text-gray-300">Net worth = Assets - Liabilities</div>
								<div class="mt-1 font-mono text-xs text-gray-400">
									Includes: Common Stock, Retained Earnings, Additional Paid-in Capital
								</div>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">EQUITY METRICS</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Return on Equity (ROE)</li>
									<li>Book Value per Share</li>
									<li>Equity Multiplier</li>
								</ul>
							</div>

							<div>
								<div class="font-mono text-xs text-gray-500">IMPORTANT NOTES</div>
								<ul class="ml-4 list-disc font-mono text-xs text-gray-400">
									<li>Treasury Stock reduces equity</li>
									<li>Dividends impact retained earnings</li>
									<li>Stock issuance affects shares outstanding</li>
								</ul>
							</div>
						</div>
					</div>
				</Card.Root>
			</div>
		</div>
	</Card.Root>
</div>
