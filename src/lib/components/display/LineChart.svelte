<script lang="ts">
	import { scaleLinear, scaleTime, type ScaleTime, type ScaleLinear } from 'd3-scale';
	import { line, type Line } from 'd3-shape';
	import { extent } from 'd3-array';

	interface DataPoint {
		[key: string]: any;
		date: string | Date;
	}

	type Props = {
		data: DataPoint[];
		xKey: string;
		yKey?: string;
		yKeys?: string[];
		title?: string;
		width?: number;
		height?: number;
	};

	let {
		data,
		xKey,
		yKey,
		yKeys,
		title = '',
		width: widthProp,
		height: heightProp
	}: Props = $props();

	let chartDiv: HTMLDivElement | null = $state(null);
	let measuredWidth = $state(0);
	let measuredHeight = $state(0);

	const widthValue = $derived(widthProp ?? measuredWidth);
	const heightValue = $derived(heightProp ?? measuredHeight);

	$effect(() => {
		if (!chartDiv) return;
		if (widthProp !== undefined && heightProp !== undefined) return;
		measuredWidth = chartDiv.clientWidth;
		measuredHeight = chartDiv.clientHeight;
	});

	const margin = { top: 20, right: 20, bottom: 30, left: 40 };

	let xScale: ScaleTime<number, number> = $state(scaleTime());
	let yScale: ScaleLinear<number, number> = $state(scaleLinear());
	let lineGenerator: Line<DataPoint> = $state(line<DataPoint>());

	$effect(() => {
		if (!data?.length || !widthValue || !heightValue) return;

		const dateExtent = extent(data, (d: DataPoint) => new Date(d[xKey])) as [Date, Date];
		xScale = xScale.domain(dateExtent).range([margin.left, widthValue - margin.right]);

		const localYKeys = yKeys;
		const allValues: number[] = localYKeys
			? data.flatMap((d: DataPoint) => localYKeys.map((key: string) => d[key]))
			: data.map((d: DataPoint) => d[yKey as string]);

		const valueExtent = extent(allValues) as [number, number];
		yScale = yScale.domain(valueExtent).range([heightValue - margin.bottom, margin.top]);

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
	{#if widthValue > 0 && heightValue > 0 && data?.length}
		<svg width={widthValue} height={heightValue} class="h-full w-full">
			{#if title}
				<text
					x={widthValue / 2}
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

			<g transform={`translate(0,${heightValue - margin.bottom})`}>
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
