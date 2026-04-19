<script lang="ts">
	import type { PageData } from './$types';
	import ValuationSplitDisplay from '$lib/components/display/ValuationSplitDisplay.svelte';
	import { buildValuationTable } from '$lib/utils/statementTableData';

	let { data }: { data: PageData } = $props();
	const quarters = $derived(data.quarters || []);

	const built = $derived(buildValuationTable(quarters as Record<string, unknown>[]));
</script>

<ValuationSplitDisplay
	rawData={built.rawData}
	quarterDates={built.quarterDates}
	ratioMetrics={built.ratioMetrics}
	staticRows={built.staticRows}
	byPeriodTitle="Valuation — by period (trailing / as-reported)"
/>
