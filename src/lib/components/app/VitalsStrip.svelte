<script lang="ts">
	import type { VitalLine } from '$lib/utils/tickerPulse';

	let { lines }: { lines: VitalLine[] } = $props();
</script>

<div
	class="grid grid-cols-1 gap-3 rounded-lg border border-gray-800/80 bg-[#0d0f12] px-3 py-3 font-mono text-xs text-gray-200 sm:grid-cols-2 lg:grid-cols-4"
>
	{#each lines as line (line.label)}
		<div class="min-w-0 border-b border-gray-800/50 pb-2 last:border-b-0 sm:border-b-0 sm:pb-0">
			<p class="text-[10px] uppercase tracking-wide text-gray-500">{line.label}</p>
			<p class="mt-0.5 truncate text-base text-white">{line.value}</p>
			<p class="mt-0.5 text-[10px] text-gray-500">{line.qoq}</p>
			<p class="text-[10px] text-gray-500">{line.yoy}</p>
		</div>
	{/each}
</div>
