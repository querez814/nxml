<script lang="ts">
	import Sparkline from './Sparkline.svelte';
	import type { HealthResult } from '$lib/utils/healthRules';
	import type { PulseKpi } from '$lib/utils/tickerPulse';
	import { ChevronRight } from 'lucide-svelte';

	let {
		title,
		kpis,
		sparklineData,
		health,
		onOpen,
		showSparkline = true,
		footerExtra = ''
	}: {
		title: string;
		kpis: PulseKpi[];
		sparklineData?: { date: string; value: number }[];
		health: HealthResult;
		onOpen: () => void;
		showSparkline?: boolean;
		footerExtra?: string;
	} = $props();

	const chipClass = $derived(
		health.level === 'healthy'
			? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
			: health.level === 'watch'
				? 'border-amber-500/40 bg-amber-500/10 text-amber-200'
				: 'border-red-500/40 bg-red-500/10 text-red-300'
	);

	const chipLabel = $derived(
		health.level === 'healthy' ? 'Healthy' : health.level === 'watch' ? 'Watch' : 'Concern'
	);
</script>

<button
	type="button"
	class="group flex w-full flex-col rounded-lg border border-gray-800 bg-[#111215] p-4 text-left transition hover:border-gray-700 hover:bg-[#15171c]"
	title="Opens the statement panel. Drag the grip on the left (or the top bar on mobile) to resize; use ⤢ for full width."
	onclick={onOpen}
>
	<div class="mb-3 flex items-start justify-between gap-2">
		<h3 class="font-mono text-xs font-semibold uppercase tracking-wide text-gray-400">{title}</h3>
		<ChevronRight class="h-4 w-4 shrink-0 text-gray-600 transition group-hover:text-emerald-400" />
	</div>

	<div class="grid flex-1 gap-4 sm:grid-cols-2">
		{#each kpis as k (k.label)}
			<div class="min-w-0">
				<p class="text-[10px] font-medium uppercase tracking-wide text-gray-500">{k.label}</p>
				<p class="mt-0.5 truncate font-mono text-lg text-white">{k.value}</p>
				<p class="mt-0.5 font-mono text-[10px] text-gray-500">{k.qoq}</p>
				<p class="font-mono text-[10px] text-gray-500">{k.yoy}</p>
			</div>
		{/each}
	</div>

	<div class="mt-4 flex items-end justify-between gap-2">
		<div class="flex flex-col gap-1">
			<span
				class="inline-flex w-fit cursor-help items-center rounded border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wide {chipClass}"
				title={health.tooltip}
			>
				{chipLabel}
			</span>
			{#if footerExtra}
				<p class="font-mono text-[10px] text-gray-500">{footerExtra}</p>
			{/if}
		</div>
		{#if showSparkline && sparklineData?.length}
			<Sparkline data={sparklineData} />
		{/if}
	</div>
</button>
