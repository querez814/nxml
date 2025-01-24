<script lang="ts">
	import type { PageData } from './$types';
	import DataTable from '$lib/components/display/DataTable.svelte';
	import BalanceSheetTutorial from '$lib/components/tutorial/balancesheet/BalanceSheetTutorial.svelte';
	let { data }: { data: PageData } = $props();
	const quarters = data.quarters || [];
	let showTutorial = $state(false);
	function formatMetricName(name: string): string {
		return name
			.replace(/([A-Z])/g, ' $1')
			.split('_')
			.join(' ')
			.trim()
			.replace(/\b\w/g, (c) => c.toUpperCase());
	}

	const quarterDates = quarters.map((q) => q.fiscalDateEnding);

	const rawData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter(
						(key) =>
							!['_id', 'symbol', 'reportedCurrency', '__v', 'fiscalDateEnding'].includes(key) &&
							!key.endsWith('_YoY') &&
							!key.endsWith('_QoQ')
					)
					.map((metric) => ({
						metric: formatMetricName(metric),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];

	const yoyData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter((key) => key.endsWith('_YoY'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_YoY', '')),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];

	const qoqData =
		quarters.length > 0
			? Object.keys(quarters[0])
					.filter((key) => key.endsWith('_QoQ'))
					.map((metric) => ({
						metric: formatMetricName(metric.replace('_QoQ', '')),
						...quarters.reduce(
							(acc, quarter) => ({
								...acc,
								[quarter.fiscalDateEnding]: quarter[metric]
							}),
							{}
						)
					}))
			: [];
</script>

<div class="mb-4 flex justify-end">
	{#if !showTutorial}
		<button
			class="rounded border border-green-400/20 px-3 py-1 font-mono text-xs text-green-400 hover:text-green-300"
			onclick={() => (showTutorial = true)}
		>
			📊 Learn about the Balance Sheet Statement
		</button>
	{/if}
</div>
{#if showTutorial}
	<div class="mb-6">
		<div class="relative">
			<BalanceSheetTutorial />
			<button
				class="absolute right-4 top-4 font-mono text-xs text-gray-400 hover:text-gray-300"
				onclick={() => (showTutorial = false)}
			>
				✕ Close
			</button>
		</div>
	</div>
{/if}
<DataTable
	{rawData}
	{yoyData}
	{qoqData}
	quarters={quarterDates}
	title="Balance Sheet - Quarterly"
/>
