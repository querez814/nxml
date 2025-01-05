<script lang="ts">
	import * as Card from '$lib/components/ui/card';
</script>

<div class="max-w-md space-y-6">
	<div>
		<h2 class="text-xl font-bold text-slate-100">Understanding the Balance Sheet</h2>
		<p class="mt-2 text-sm text-slate-300">
			A financial snapshot showing what a company owns (assets), owes (liabilities), and the
			shareholders' stake (equity).
		</p>
	</div>

	<div class="rounded-lg bg-slate-800/50 p-4">
		<h3 class="mb-3 font-semibold text-slate-100">Assets</h3>
		<div class="space-y-4">
			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Total Current Assets</span>
				<p class="mt-1 text-sm text-slate-300">
					Assets that can be converted to cash within one year.
				</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Cash and Equivalents</span>
				<p class="mt-1 text-sm text-slate-300">
					Immediately available cash and highly liquid investments.
				</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Inventory</span>
				<p class="mt-1 text-sm text-slate-300">
					Products ready for sale and materials for production.
				</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Property & Equipment</span>
				<p class="mt-1 text-sm text-slate-300">
					Long-term physical assets like buildings and machinery.
				</p>
			</div>
		</div>
	</div>

	<div class="rounded-lg bg-slate-800/50 p-4">
		<h3 class="mb-3 font-semibold text-slate-100">Liabilities</h3>
		<div class="space-y-4">
			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Current Liabilities</span>
				<p class="mt-1 text-sm text-slate-300">Debts and obligations due within one year.</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Total Liabilities</span>
				<p class="mt-1 text-sm text-slate-300">
					All debts and obligations, both short and long-term.
				</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Current Debt</span>
				<p class="mt-1 text-sm text-slate-300">Short-term borrowings due within one year.</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Deferred Revenue</span>
				<p class="mt-1 text-sm text-slate-300">Advance payments for future goods/services.</p>
			</div>
		</div>
	</div>

	<div class="rounded-lg bg-slate-800/50 p-4">
		<h3 class="mb-3 font-semibold text-slate-100">Key Metrics</h3>
		<div class="space-y-4">
			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Working Capital</span>
				<p class="mt-1 text-sm text-slate-300">
					Current assets minus current liabilities - shows operational liquidity.
				</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Shareholder Equity</span>
				<p class="mt-1 text-sm text-slate-300">Company's net worth (assets minus liabilities).</p>
			</div>

			<div class="rounded-md bg-slate-700/30 p-3">
				<span class="font-medium text-slate-100">Shares Outstanding</span>
				<p class="mt-1 text-sm text-slate-300">Total number of shares held by all shareholders.</p>
			</div>
		</div>
	</div>
</div>
