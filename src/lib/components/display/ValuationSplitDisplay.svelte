<script lang="ts">
	import DataTable from './DataTable.svelte';
	import type { ValuationStaticRow } from '$lib/utils/statementTableData';

	let {
		rawData,
		quarterDates,
		ratioMetrics,
		staticRows,
		byPeriodTitle = 'Valuation — by period (trailing / as-reported)',
		staticTitle = 'Forward & spot metrics',
		staticBlurb = 'Shown once: same value was repeated in every period column (e.g. forward multiples, or fields the backend cannot tie to a TTM for each date).',
		compact = false
	}: {
		rawData: Record<string, unknown>[];
		quarterDates: string[];
		ratioMetrics: string[];
		staticRows: ValuationStaticRow[];
		byPeriodTitle?: string;
		staticTitle?: string;
		staticBlurb?: string;
		compact?: boolean;
	} = $props();
</script>

<div class={compact ? 'space-y-4' : 'space-y-10'}>
	{#if rawData.length}
		<DataTable {rawData} quarters={quarterDates} title={byPeriodTitle} {ratioMetrics} />
	{/if}

	{#if staticRows.length}
		<div
			class="rounded-xl border border-slate-800 bg-slate-900/40 p-4 shadow-xl ring-1 ring-slate-800/80"
		>
			<h3 class="font-mono text-sm font-semibold tracking-wide text-amber-400/90">{staticTitle}</h3>
			<p class="mt-1 text-xs leading-relaxed text-slate-500">{staticBlurb}</p>
			<div class="mt-3 overflow-x-auto rounded-lg border border-slate-800/60">
				<table class="w-full min-w-[280px] border-separate border-spacing-0 text-sm">
					<thead>
						<tr class="bg-slate-800/60">
							<th
								class="px-3 py-2 text-left text-xs font-medium uppercase tracking-wide text-slate-400"
								>Metric</th
							>
							<th
								class="px-3 py-2 text-right text-xs font-medium uppercase tracking-wide text-slate-400"
								>Value</th
							>
						</tr>
					</thead>
					<tbody>
						{#each staticRows as row, i (row.label + i)}
							<tr class="border-t border-slate-800/50 hover:bg-slate-800/20">
								<td class="px-3 py-2.5 font-medium text-slate-200">{row.label}</td>
								<td class="px-3 py-2.5 text-right font-mono text-emerald-400">{row.value}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}

	{#if !rawData.length && !staticRows.length}
		<p class="text-sm text-slate-500">No valuation rows to display.</p>
	{/if}
</div>
