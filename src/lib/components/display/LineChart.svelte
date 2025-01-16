<script lang="ts">
	import { scaleLinear, scaleTime, type ScaleTime, type ScaleLinear } from 'd3-scale';
	import { line, type Line } from 'd3-shape';
	import { extent } from 'd3-array';

	interface DataPoint {
		[key: string]: any;
		date: string | Date;
	}

	// Props
	let {
		data,
		xKey,
		yKey,
		yKeys = undefined,
		title = '',
		width: initialWidth = undefined,
		height: initialHeight = undefined
	} = $props<{
		data: DataPoint[];
		xKey: string;
		yKey?: string;
		yKeys?: string[];
		title?: string;
		width?: number;
		height?: number;
	}>();

	let chartDiv: HTMLDivElement | null = null;

	let dimensions = $state({
		width: initialWidth || 0,
		height: initialHeight || 0
	});

	$effect(() => {
		if (chartDiv) {
			dimensions = {
				width: initialWidth || chartDiv.clientWidth,
				height: initialHeight || chartDiv.clientHeight
			};
		}
	});

	const margin = { top: 20, right: 20, bottom: 30, left: 40 };

	let xScale = $state<ScaleTime<number, number>>(scaleTime());
	let yScale = $state<ScaleLinear<number, number>>(scaleLinear());
	let lineGenerator = $state<Line<DataPoint>>(line<DataPoint>());

	$effect(() => {
		if (!data.length || !dimensions.width || !dimensions.height) return;

		const dateExtent = extent(data, (d: any) => new Date(d[xKey])) as [Date, Date];
		xScale = xScale.domain(dateExtent).range([margin.left, dimensions.width - margin.right]);

		const allValues: number[] = yKeys
			? data.flatMap((d: any) => yKeys.map((key: any) => d[key]))
			: data.map((d: any) => d[yKey as string]);

		const valueExtent = extent(allValues) as [number, number];
		yScale = yScale.domain(valueExtent).range([dimensions.height - margin.bottom, margin.top]);

		lineGenerator = lineGenerator
			.x((d) => xScale(new Date(d[xKey])))
			.y((d) => yScale(d[yKey as string]));
	});

	function formatDate(date: Date): string {
		return date.toLocaleDateString();
	}

	function getPathData(lineData: DataPoint[]): string {
		return lineGenerator(lineData) || '';
	}
</script>

<div class="h-full w-full" bind:this={chartDiv}>
	{#if dimensions.width > 0 && dimensions.height > 0 && data.length}
		<svg width={dimensions.width} height={dimensions.height} class="h-full w-full">
			{#if title}
				<text
					x={dimensions.width / 2}
					y={margin.top / 2}
					text-anchor="middle"
					class="fill-current text-sm font-medium"
				>
					{title}
				</text>
			{/if}

			{#if yKeys}
				{#each yKeys as key (key)}
					<path
						d={getPathData(data)}
						class="fill-none stroke-current"
						style="stroke: var(--color-{key})"
					/>
				{/each}
			{:else}
				<path d={getPathData(data)} class="fill-none stroke-current" />
			{/if}

			<g transform={`translate(0,${dimensions.height - margin.bottom})`}>
				{#each xScale.ticks(5) as tick (tick.getTime())}
					<g transform={`translate(${xScale(tick)},0)`}>
						<line y2="6" stroke="currentColor" />
						<text y="9" dy="0.71em" text-anchor="middle" class="fill-current text-xs">
							{formatDate(tick)}
						</text>
					</g>
				{/each}
			</g>

			<g transform={`translate(${margin.left},0)`}>
				{#each yScale.ticks(5) as tick (tick)}
					<g transform={`translate(0,${yScale(tick)})`}>
						<line x2="-6" stroke="currentColor" />
						<text x="-9" dy="0.32em" text-anchor="end" class="fill-current text-xs">
							{tick.toFixed(2)}
						</text>
					</g>
				{/each}
			</g>
		</svg>
	{/if}
</div>

<style>
	:global(.stroke-current) {
		stroke-width: 1.5;
	}
</style>
