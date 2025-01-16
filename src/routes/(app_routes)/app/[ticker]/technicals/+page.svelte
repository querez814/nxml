<script lang="ts">
	import type { PageData } from './$types';
	import Technicals from '$lib/components/display/Technicals.svelte';
	import { TechnicalsTypeGuard } from '$lib/types/technicals/technicalclasses';
	import type { DailyAnalysis, MasterResponse } from '$lib/types/technicals/technicalinterfaces';

	// Props
	let { data } = $props<{ data: PageData }>();

	// State with runes
	let technicals = new TechnicalsTypeGuard();
	let processedData = $state<MasterResponse>(data.technicalData);
	let availableDates = $state<string[]>(technicals.getAvailableDates(data.technicalData));
	let selectedDate = $state<string>(availableDates[availableDates.length - 1]);
	let dailyAnalysis = $state<DailyAnalysis | null>(null);

	$effect(() => {
		if (processedData && selectedDate) {
			dailyAnalysis = technicals.getDailyAnalysis(processedData, selectedDate);
		}
	});

	// Event handler
	function handleDateChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		selectedDate = target.value;
	}
</script>

<div class="space-y-4">
	<div class="flex items-center space-x-4">
		<label for="date-select" class="font-mono text-sm">Select Date:</label>
		<select
			id="date-select"
			class="rounded bg-black/20 p-2 font-mono text-sm"
			value={selectedDate}
			onchange={handleDateChange}
		>
			{#each availableDates as date}
				<option value={date}>{date}</option>
			{/each}
		</select>
	</div>

	{#if processedData && dailyAnalysis}
		<Technicals {processedData} {dailyAnalysis} />
	{:else}
		<div class="flex h-96 items-center justify-center">
			<span class="font-mono text-lg">Loading technical data...</span>
		</div>
	{/if}
</div>
