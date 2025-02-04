<script lang="ts">
	// Using new Svelte 5 syntax (e.g. $props, $state, $effect)
	const api_url = import.meta.env.VITE_API_URL;
	import { Chart } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { GripVertical } from 'lucide-svelte';
	import type { ApexOptions } from 'apexcharts';

	let { ticker }: { ticker: string } = $props();
	let data = $state<Record<string, any>>({});
	let error = $state<string | null>(null);
	let loading = $state(true);
	let chartInstance = $state<any>(null);
	let selectedTimeframe = $state('daily');
	let selectedRange = $state('6m');
	let currentPrice = $state<number | null>(null);
	let dataPointCount = $state<number>(0);

	// Drag and resize state
	let position = $state({ x: 20, y: 20 });
	let size = $state({ width: 800, height: 500 });
	let isDragging = $state(false);
	let isResizing = $state(false);
	let startPosition = { x: 0, y: 0 };
	let container: HTMLElement;
	let lastCursor = { x: 0, y: 0 };

	const timeframes = [
		{ value: 'daily', label: 'Daily' },
		{ value: 'weekly', label: 'Weekly' },
		{ value: 'monthly', label: 'Monthly' }
	];

	const ranges = [
		{ value: '1m', label: '1M', days: 30 },
		{ value: '3m', label: '3M', days: 90 },
		{ value: '6m', label: '6M', days: 180 },
		{ value: '1y', label: '1Y', days: 365 },
		{ value: '2y', label: '2Y', days: 730 },
		{ value: '5y', label: '5Y', days: 1825 }
	];

	function handleDragStart(event: PointerEvent) {
		// Only start dragging if the pointer is on an element with the "drag-handle" class
		if (event.target instanceof HTMLElement && !event.target.closest('.drag-handle')) {
			return;
		}
		isDragging = true;
		const target = event.currentTarget as HTMLElement;
		target.setPointerCapture(event.pointerId);
		startPosition = {
			x: event.clientX - position.x,
			y: event.clientY - position.y
		};
	}

	function handleDragMove(event: PointerEvent) {
		if (isDragging) {
			position = {
				x: Math.max(0, event.clientX - startPosition.x),
				y: Math.max(0, event.clientY - startPosition.y)
			};
		}

		if (isResizing) {
			const cursor = { x: event.clientX, y: event.clientY };
			const delta = {
				x: cursor.x - lastCursor.x,
				y: cursor.y - lastCursor.y
			};

			const newSize = {
				width: Math.max(400, size.width + delta.x),
				height: Math.max(300, size.height + delta.y)
			};

			const maxWidth = window.innerWidth - position.x - 20;
			const maxHeight = window.innerHeight - position.y - 20;

			size = {
				width: Math.min(maxWidth, newSize.width),
				height: Math.min(maxHeight, newSize.height)
			};

			lastCursor = cursor;
		}
	}

	function handleDragEnd(event: PointerEvent) {
		isDragging = false;
		isResizing = false;
		if (event.currentTarget instanceof HTMLElement) {
			event.currentTarget.releasePointerCapture(event.pointerId);
		}
	}

	function handleResizeStart(event: PointerEvent) {
		isResizing = true;
		lastCursor = { x: event.clientX, y: event.clientY };
		// Prevent the resize handle from triggering a drag
		event.stopPropagation();
	}

	function handleResizeEnd() {
		isResizing = false;
	}

	function filterDataByRange(data: any[], range: string): any[] {
		const rangeDays = ranges.find((r) => r.value === range)?.days || 180;
		const cutoffDate = new Date();
		cutoffDate.setDate(cutoffDate.getDate() - rangeDays);
		return data.filter((item) => new Date(item.x) >= cutoffDate);
	}

	const options: ApexOptions = {
		series: [
			{
				name: 'Price',
				data: []
			}
		],
		chart: {
			type: 'candlestick',
			height: '100%',
			width: '100%',
			animations: {
				enabled: false
			},
			background: '#1a1a1a',
			toolbar: {
				show: true,
				tools: {
					download: false,
					selection: true,
					zoom: true,
					zoomin: true,
					zoomout: true,
					pan: true,
					reset: true
				}
			}
		},
		grid: {
			borderColor: '#2D3748',
			xaxis: {
				lines: {
					show: false
				}
			},
			yaxis: {
				lines: {
					show: true
				}
			}
		},
		plotOptions: {
			candlestick: {
				colors: {
					upward: '#48BB78',
					downward: '#F56565'
				},
				wick: {
					useFillColor: true
				}
			}
		},
		xaxis: {
			type: 'datetime',
			labels: {
				style: {
					colors: '#A0AEC0'
				},
				datetimeFormatter: {
					year: 'yyyy',
					month: "MMM 'yy",
					day: 'dd MMM'
				},
				hideOverlappingLabels: true
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			tickAmount: 8
		},
		yaxis: {
			labels: {
				style: {
					colors: '#A0AEC0'
				},
				formatter: (value: number) => value.toFixed(2)
			},
			tickAmount: 8,
			tooltip: {
				enabled: true
			}
		},
		tooltip: {
			custom: function ({ seriesIndex, dataPointIndex, w }) {
				const o = w.globals.seriesCandleO[0][dataPointIndex];
				const h = w.globals.seriesCandleH[0][dataPointIndex];
				const l = w.globals.seriesCandleL[0][dataPointIndex];
				const c = w.globals.seriesCandleC[0][dataPointIndex];
				const date = new Date(w.globals.seriesX[0][dataPointIndex]);

				return `
					<div class="px-2 py-1 bg-background/90 backdrop-blur-sm border border-border rounded-sm">
						<div class="text-xs">
							<div class="font-semibold mb-1">${date.toLocaleDateString()}</div>
							<div class="grid grid-cols-2 gap-x-3">
								<span class="text-muted-foreground">Open</span>
								<span class="text-right">${o.toFixed(2)}</span>
								<span class="text-muted-foreground">High</span>
								<span class="text-right">${h.toFixed(2)}</span>
								<span class="text-muted-foreground">Low</span>
								<span class="text-right">${l.toFixed(2)}</span>
								<span class="text-muted-foreground">Close</span>
								<span class="text-right">${c.toFixed(2)}</span>
							</div>
						</div>
					</div>
				`;
			}
		},
		states: {
			hover: {
				filter: {
					type: 'none'
				}
			},
			active: {
				allowMultipleDataPointsSelection: false,
				filter: {
					type: 'none'
				}
			}
		}
	};

	async function fetchData() {
		loading = true;
		error = null;

		try {
			const params = new URLSearchParams({
				ticker,
				timeframe: selectedTimeframe,
				outputsize: 'full'
			});

			const response = await fetch(`${api_url}/financials/pricescard?${params}`);
			const jsonData = await response.json();

			if ('error' in jsonData) {
				throw new Error(jsonData.error);
			}

			data = jsonData.data;

			const candleData = Object.entries(data)
				.map(([timestamp, values]) => ({
					x: new Date(timestamp).getTime(),
					y: [
						parseFloat(values['1. open']),
						parseFloat(values['2. high']),
						parseFloat(values['3. low']),
						parseFloat(values['4. close'])
					]
				}))
				.sort((a, b) => a.x - b.x);

			const filteredData = filterDataByRange(candleData, selectedRange);
			dataPointCount = filteredData.length;

			if (filteredData.length > 0) {
				currentPrice = filteredData[filteredData.length - 1].y[3];
			}

			options.series = [
				{
					name: 'Price',
					data: filteredData
				}
			];

			if (chartInstance) {
				chartInstance.updateOptions(options);
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to fetch market data';
			console.error('Fetch error:', error, err);
		} finally {
			loading = false;
		}
	}

	$effect(() => {
		if (selectedTimeframe) {
			fetchData();
		}
	});

	onMount(() => {
		fetchData();
	});
</script>

<div
	bind:this={container}
	class="fixed shadow-lg"
	class:resizing={isResizing}
	style="transform: translate({position.x}px, {position.y}px); width: {size.width}px; height: {size.height}px;"
	onpointerdown={handleDragStart}
	onpointermove={handleDragMove}
	onpointerup={handleDragEnd}
	onpointercancel={handleDragEnd}
>
	<Card.Root class="relative h-full w-full border-solid border-border bg-background font-mono">
		<div
			class="drag-handle flex cursor-move items-center justify-between border-b border-border bg-muted px-4 py-2"
		>
			<div class="flex items-center">
				<GripVertical class="mr-2 h-4 w-4 text-muted-foreground" />
				<h3 class="text-lg font-semibold text-foreground">Price Chart - {ticker}</h3>
				{#if currentPrice}
					<span class="ml-4 text-lg font-bold text-foreground">
						${currentPrice.toFixed(2)}
					</span>
				{/if}
			</div>
			<!-- Wrap interactive controls in a container that stops pointer events from triggering drag -->
			<div class="flex items-center space-x-2">
				<div class="flex overflow-hidden rounded-md border border-border">
					{#each ranges as range}
						<button
							type="button"
							class="px-3 py-1 text-sm font-medium transition-colors"
							class:bg-primary={selectedRange === range.value}
							class:text-primary-foreground={selectedRange === range.value}
							class:bg-background={selectedRange !== range.value}
							class:text-foreground={selectedRange !== range.value}
							class:hover:bg-muted={selectedRange !== range.value}
							onclick={() => {
								selectedRange = range.value;
								fetchData();
							}}
						>
							{range.label}
						</button>
					{/each}
				</div>

				<select
					value={selectedTimeframe}
					onchange={(e) => {
						selectedTimeframe = e.currentTarget.value;
						fetchData();
					}}
					class="h-8 w-28 rounded-md border border-border bg-background px-2 py-1 text-sm text-foreground hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
				>
					{#each timeframes as timeframe}
						<option value={timeframe.value}>
							{timeframe.label}
						</option>
					{/each}
				</select>

				{#if dataPointCount}
					<span class="text-sm text-muted-foreground">
						{dataPointCount} points
					</span>
				{/if}
			</div>
		</div>

		<Card.Content class="h-[calc(100%-3rem)]">
			{#if loading}
				<p class="flex h-full items-center justify-center text-muted-foreground">Loading...</p>
			{:else if error}
				<p class="flex h-full items-center justify-center text-destructive">{error}</p>
			{:else}
				<div class="h-full w-full">
					<Chart {options} bind:chart={chartInstance} />
				</div>
			{/if}
		</Card.Content>

		<div
			class="resize-handle absolute bottom-0 right-0 flex h-6 w-6 cursor-se-resize items-center justify-center border-l border-t border-border bg-muted hover:bg-muted/80"
			onpointerdown={handleResizeStart}
			onpointerup={handleResizeEnd}
			onpointercancel={handleResizeEnd}
		>
			<div
				class="h-3 w-3"
				style="background: repeating-linear-gradient(135deg, currentColor 0px, currentColor 1px, transparent 1px, transparent 4px);"
			></div>
		</div>
	</Card.Root>
</div>

<style>
	.resize-handle {
		opacity: 0.7;
		z-index: 10;
		touch-action: none;
	}

	.resize-handle:hover {
		opacity: 1;
	}

	.drag-handle {
		touch-action: none;
		-webkit-app-region: drag;
	}

	/* Prevent text selection while dragging */
	:global(*) {
		user-select: none;
	}

	/* Hardware acceleration */
	:global(.apexcharts-canvas) {
		transform: translateZ(0);
		backface-visibility: hidden;
		perspective: 1000;
		-webkit-font-smoothing: antialiased;
	}
</style>
