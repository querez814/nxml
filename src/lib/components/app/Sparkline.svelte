<script lang="ts">
	import { scaleLinear } from 'd3-scale';
	import { line } from 'd3-shape';
	import { extent } from 'd3-array';

	let {
		data,
		width = 80,
		height = 24,
		class: className = ''
	}: {
		data: { date: string; value: number }[];
		width?: number;
		height?: number;
		class?: string;
	} = $props();

	const pad = 2;

	const pathD = $derived.by(() => {
		if (!data.length) return '';
		const xs = data.map((_, i) => i);
		const ys = data.map((d) => d.value);
		const xExt = extent(xs) as [number, number];
		const yExt = extent(ys) as [number, number];
		if (yExt[0] === yExt[1]) {
			yExt[0] -= 1;
			yExt[1] += 1;
		}
		const xScale = scaleLinear().domain(xExt).range([pad, width - pad]);
		const yScale = scaleLinear().domain(yExt).range([height - pad, pad]);
		const gen = line<{ x: number; y: number }>()
			.x((d) => d.x)
			.y((d) => d.y);
		const pts = data.map((d, i) => ({ x: xScale(i), y: yScale(d.value) }));
		return gen(pts) ?? '';
	});
</script>

<svg
	class="text-emerald-400/90 {className}"
	{width}
	{height}
	viewBox="0 0 {width} {height}"
	aria-hidden="true"
>
	{#if pathD}
		<path d={pathD} fill="none" class="stroke-current" stroke-width="1.25" vector-effect="non-scaling-stroke" />
	{/if}
</svg>
