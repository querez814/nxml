<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import { Chart } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { GripVertical, TrendingUp, TrendingDown } from 'lucide-svelte';
	import type { ApexOptions } from 'apexcharts';
	interface ChartDataPoint {
		date: string;
		macd?: number;
		macd_signal?: number;
		macd_hist?: number;
		aroonosc?: number;
		mom?: number;
		buy_signal?: number | null; // ✅ MACD Buy Signal
		sell_signal?: number | null; // ✅ MACD Sell Signal
		aroon_buy?: number | null; // ✅ Aroon Buy Signal
		aroon_sell?: number | null; // ✅ Aroon Sell Signal
		mom_buy?: number | null; // ✅ Momentum Buy Signal
		mom_sell?: number | null; // ✅ Momentum Sell Signal
	}

	let { ticker }: { ticker: string } = $props();
	let rawData = $state<ChartDataPoint[]>([]);
	let displayData = $state<ChartDataPoint[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);
	let chartOptions = $state<ApexOptions | null>(null);
	let selectedInterval = $state('daily');
	let selectedIndicator = $state('macd');
	let currentValue = $state<number | null>(null);
	let currentSecondaryValue = $state<number | null>(null);

	let currentHistogram = $state<number | null>(null);

	// UI State
	let position = $state({ x: 20, y: 20 });
	let size = $state({ width: 800, height: 500 });
	let isDragging = $state(false);
	let isResizing = $state(false);
	let startPosition = { x: 0, y: 0 };
	let container: HTMLElement;
	let lastCursor = { x: 0, y: 0 };

	const intervals = [
		{ value: '1min', label: '1 Minute' },
		{ value: '5min', label: '5 Minutes' },
		{ value: '15min', label: '15 Minutes' },
		{ value: '30min', label: '30 Minutes' },
		{ value: '60min', label: '1 Hour' },
		{ value: 'daily', label: 'Daily' },
		{ value: 'weekly', label: 'Weekly' },
		{ value: 'monthly', label: 'Monthly' }
	];

	const indicators = [
		{ value: 'macd', label: 'MACD' },
		{ value: 'ao', label: 'Aroon Oscillator' },
		{ value: 'mom', label: 'Momentum' }
	];

	const defaultChartOptions: ApexOptions = {
		chart: {
			type: 'line',
			height: '100%',
			width: '100%',
			toolbar: { show: false },
			animations: { enabled: false },
			background: '#1a1a1a',
			zoom: { enabled: false }
		},
		grid: {
			borderColor: '#2D3748',
			xaxis: { lines: { show: false } },
			yaxis: { lines: { show: true } }
		},
		xaxis: {
			type: 'datetime',
			labels: {
				style: { colors: '#A0AEC0' },
				datetimeFormatter: {
					year: 'yyyy',
					month: "MMM 'yy",
					day: 'dd MMM',
					hour: 'HH:mm'
				}
			}
		},
		yaxis: {
			labels: {
				style: { colors: '#A0AEC0' },
				formatter: (value: number) => value.toFixed(2)
			},
			forceNiceScale: true
		},
		tooltip: {
			theme: 'dark',
			x: {
				format: 'dd MMM yyyy HH:mm'
			},
			y: {
				formatter: (value) => value.toFixed(2)
			}
		},
		stroke: {
			width: 2,
			curve: 'smooth'
		},
		markers: {
			size: 0
		}
	};

	function parseNumericValue(value: any): number {
		const parsed = Number(value);
		return isNaN(parsed) ? 0 : parsed;
	}

	function filterDataByDate(data: ChartDataPoint[]): ChartDataPoint[] {
		const filterDate = getFilterDate();
		return data
			.filter((item) => new Date(item.date) >= filterDate)
			.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
	}

	function processData(rawData: ChartDataPoint[]): ChartDataPoint[] {
		return rawData.map((item, index, array) => {
			const macd = parseNumericValue(item.macd);
			const macd_signal = parseNumericValue(item.macd_signal);
			const macd_hist = parseNumericValue(item.macd_hist);
			const aroonosc = parseNumericValue(item.aroonosc);
			const mom = parseNumericValue(item.mom);

			let buy_signal = null;
			let sell_signal = null;
			let aroon_buy = null;
			let aroon_sell = null;
			let mom_buy = null;
			let mom_sell = null;

			if (index > 0) {
				const prev = array[index - 1];

				// MACD Buy/Sell Signals
				const prev_macd = parseNumericValue(prev.macd);
				const prev_signal = parseNumericValue(prev.macd_signal);
				if (prev_macd < prev_signal && macd > macd_signal) buy_signal = macd;
				if (prev_macd > prev_signal && macd < macd_signal) sell_signal = macd;

				// Aroon Buy/Sell Signals
				const prev_aroon = parseNumericValue(prev.aroonosc);
				if (prev_aroon < 50 && aroonosc >= 50) aroon_buy = aroonosc;
				if (prev_aroon > -50 && aroonosc <= -50) aroon_sell = aroonosc;

				// Momentum Buy/Sell Signals
				const prev_mom = parseNumericValue(prev.mom);
				if (prev_mom < 0 && mom > 0) mom_buy = mom;
				if (prev_mom > 0 && mom < 0) mom_sell = mom;
			}

			return {
				...item,
				macd,
				macd_signal,
				macd_hist,
				aroonosc,
				mom,
				buy_signal: buy_signal !== null ? buy_signal : undefined,
				sell_signal: sell_signal !== null ? sell_signal : undefined,
				aroon_buy: aroon_buy !== null ? aroon_buy : undefined,
				aroon_sell: aroon_sell !== null ? aroon_sell : undefined,
				mom_buy: mom_buy !== null ? mom_buy : undefined,
				mom_sell: mom_sell !== null ? mom_sell : undefined
			};
		});
	}
	function updateChartOptions() {
		if (!displayData.length) return;

		const series = [];
		const colors = [];

		switch (selectedIndicator) {
			case 'macd':
				series.push(
					{
						name: 'MACD',
						type: 'line',
						data: displayData.map((d) => ({ x: new Date(d.date).getTime(), y: d.macd }))
					},
					{
						name: 'Signal',
						type: 'line',
						data: displayData.map((d) => ({ x: new Date(d.date).getTime(), y: d.macd_signal }))
					},
					{
						name: 'Histogram',
						type: 'bar',
						data: displayData.map((d) => ({ x: new Date(d.date).getTime(), y: d.macd_hist }))
					},
					{
						name: 'MACD Buy',
						type: 'scatter',
						data: displayData
							.filter((d) => d.buy_signal !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.buy_signal })),
						marker: { size: 8, shape: 'circle', colors: ['#00FF00'] } // 🟢 Green Buy Marker
					},
					{
						name: 'MACD Sell',
						type: 'scatter',
						data: displayData
							.filter((d) => d.sell_signal !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.sell_signal })),
						marker: { size: 8, shape: 'triangle', colors: ['#FF0000'] } // 🔴 Red Sell Marker
					}
				);
				colors.push('#4299E1', '#48BB78', '#A0AEC0', '#00FF00', '#FF0000');
				break;

			case 'ao':
				series.push(
					{
						name: 'Aroon Oscillator',
						type: 'line',
						data: displayData.map((d) => ({ x: new Date(d.date).getTime(), y: d.aroonosc }))
					},
					{
						name: 'Aroon Buy',
						type: 'scatter',
						data: displayData
							.filter((d) => d.aroon_buy !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.aroon_buy })),
						marker: { size: 8, shape: 'circle', colors: ['#00FF00'] }
					},
					{
						name: 'Aroon Sell',
						type: 'scatter',
						data: displayData
							.filter((d) => d.aroon_sell !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.aroon_sell })),
						marker: { size: 8, shape: 'triangle', colors: ['#FF0000'] }
					}
				);
				colors.push('#FBBF24', '#00FF00', '#FF0000');
				break;

			case 'mom':
				series.push(
					{
						name: 'Momentum',
						type: 'line',
						data: displayData.map((d) => ({ x: new Date(d.date).getTime(), y: d.mom }))
					},
					{
						name: 'Momentum Buy',
						type: 'scatter',
						data: displayData
							.filter((d) => d.mom_buy !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.mom_buy })),
						marker: { size: 8, shape: 'circle', colors: ['#00FF00'] }
					},
					{
						name: 'Momentum Sell',
						type: 'scatter',
						data: displayData
							.filter((d) => d.mom_sell !== undefined)
							.map((d) => ({ x: new Date(d.date).getTime(), y: d.mom_sell })),
						marker: { size: 8, shape: 'triangle', colors: ['#FF0000'] }
					}
				);
				colors.push('#34D399', '#00FF00', '#FF0000');
				break;
		}

		chartOptions = {
			...defaultChartOptions,
			series,
			colors,
			stroke: {
				...defaultChartOptions.stroke,
				width: selectedIndicator === 'macd' ? [2, 2, 1, 0, 0] : [2]
			}
		};
	}

	function getFilterDate(): Date {
		const today = new Date();
		const filterDate = new Date();

		switch (selectedInterval) {
			case '1min':
			case '5min':
				filterDate.setDate(today.getDate() - 1);
				break;
			case '15min':
			case '30min':
			case '60min':
				filterDate.setDate(today.getDate() - 7);
				break;
			case 'daily':
				filterDate.setMonth(today.getMonth() - 6);
				break;
			case 'weekly':
				filterDate.setFullYear(today.getFullYear() - 1);
				break;
			case 'monthly':
				filterDate.setFullYear(today.getFullYear() - 2);
				break;
		}
		return filterDate;
	}

	function updateCurrentValues() {
		if (!displayData.length) return;

		const latest = displayData[displayData.length - 1];
		switch (selectedIndicator) {
			case 'macd':
				currentValue = latest.macd ?? null;
				currentSecondaryValue = latest.macd_signal ?? null ?? null;
				currentHistogram = latest.macd_hist ?? null;
				break;
			case 'ao':
				currentValue = latest.aroonosc ?? null;
				currentSecondaryValue = null;
				currentHistogram = null;
				break;
			case 'mom':
				currentValue = latest.mom ?? null;
				currentSecondaryValue = null;
				currentHistogram = null;
				break;
		}
	}

	async function fetchData() {
		loading = true;
		error = null;
		rawData = [];
		displayData = [];

		try {
			const response = await fetch(
				`${api_url}/technicals/${selectedIndicator}/${selectedInterval}/${ticker}`
			);

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const jsonData = await response.json();
			if (!Array.isArray(jsonData)) {
				throw new Error('Invalid data format received from server');
			}

			// Process the raw data
			rawData = processData(jsonData);
			// Filter and sort for display
			displayData = filterDataByDate(rawData);

			// Update current values and chart
			if (displayData.length > 0) {
				updateCurrentValues();
				updateChartOptions();
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to fetch data';
			console.error('Fetch error:', error);
		} finally {
			loading = false;
		}
	}

	// Drag and resize handlers...
	function handleDragStart(event: PointerEvent) {
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

			size = {
				width: Math.max(400, Math.min(window.innerWidth - position.x - 20, size.width + delta.x)),
				height: Math.max(300, Math.min(window.innerHeight - position.y - 20, size.height + delta.y))
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
		event.stopPropagation();
	}

	function handleResizeEnd() {
		isResizing = false;
	}

	$effect(() => {
		if (ticker && selectedInterval && selectedIndicator) {
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
				<h3 class="text-lg font-semibold text-foreground">
					{selectedIndicator.toUpperCase()} - {ticker}
				</h3>
			</div>

			<div class="flex items-center space-x-4">
				{#if currentValue !== null}
					<div class="flex items-center space-x-2">
						<span class="text-sm font-medium text-muted-foreground">
							{selectedIndicator === 'macd'
								? 'MACD:'
								: selectedIndicator === 'ao'
									? 'Aroon:'
									: 'Momentum:'}
						</span>
						<span
							class="text-lg font-bold"
							class:text-green-500={currentValue > 0}
							class:text-red-500={currentValue < 0}
						>
							{currentValue.toFixed(2)}
						</span>

						{#if currentSecondaryValue !== null}
							<span class="text-sm font-medium text-muted-foreground">Signal:</span>
							<span class="text-lg font-bold text-foreground">
								{currentSecondaryValue.toFixed(2)}
							</span>
						{/if}

						{#if selectedIndicator === 'macd' && currentHistogram !== null}
							<span class="text-sm">
								{#if currentHistogram > 0}
									<TrendingUp class="h-5 w-5 text-green-500" />
								{:else}
									<TrendingDown class="h-5 w-5 text-red-500" />
								{/if}
							</span>
						{/if}

						{#if selectedIndicator === 'macd' && currentValue !== null}
							<!-- We handle possible null for currentSecondaryValue by using optional chaining or coalescing. -->
							<span
								class="text-sm font-medium"
								class:text-green-500={(currentValue ?? 0) > (currentSecondaryValue ?? 0)}
								class:text-red-500={(currentValue ?? 0) < (currentSecondaryValue ?? 0)}
							>
								{(currentValue ?? 0) > (currentSecondaryValue ?? 0) ? 'BUY' : 'SELL'}
							</span>
						{/if}

						{#if selectedIndicator === 'ao' && currentValue !== null}
							<span
								class="text-sm font-medium"
								class:text-green-500={currentValue > 50}
								class:text-red-500={currentValue < -50}
							>
								{currentValue > 50 ? 'BUY' : 'SELL'}
							</span>
						{/if}

						{#if selectedIndicator === 'mom' && currentValue !== null}
							<span
								class="text-sm font-medium"
								class:text-green-500={currentValue > 0}
								class:text-red-500={currentValue < 0}
							>
								{currentValue > 0 ? 'BUY' : 'SELL'}
							</span>
						{/if}
					</div>
				{/if}

				<div class="flex space-x-2">
					<select
						value={selectedIndicator}
						onchange={(e) => (selectedIndicator = e.currentTarget.value)}
						class="h-8 rounded-md border border-border bg-background px-3 py-1 text-sm text-foreground hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
					>
						{#each indicators as indicator}
							<option value={indicator.value}>
								{indicator.label}
							</option>
						{/each}
					</select>

					<select
						value={selectedInterval}
						onchange={(e) => (selectedInterval = e.currentTarget.value)}
						class="h-8 rounded-md border border-border bg-background px-3 py-1 text-sm text-foreground hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
					>
						{#each intervals as interval}
							<option value={interval.value}>
								{interval.label}
							</option>
						{/each}
					</select>
				</div>
			</div>
		</div>

		<Card.Content class="h-[calc(100%-3rem)]">
			{#if loading}
				<div class="flex h-full items-center justify-center">
					<div class="text-muted-foreground">
						<div class="loading"></div>
						<span class="ml-2">Loading...</span>
					</div>
				</div>
			{:else if error}
				<div class="flex h-full items-center justify-center">
					<p class="text-destructive">{error}</p>
				</div>
			{:else if displayData.length === 0}
				<div class="flex h-full items-center justify-center">
					<p class="text-muted-foreground">No data available</p>
				</div>
			{:else if chartOptions}
				<div class="h-full w-full">
					<Chart options={chartOptions} />
				</div>
			{/if}
		</Card.Content>

		<div
			class="resize-handle absolute bottom-0 right-0 h-6 w-6 cursor-se-resize border-l border-t border-border bg-muted hover:bg-muted/80"
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

	:global(*) {
		user-select: none;
	}

	:global(.apexcharts-canvas) {
		transform: translateZ(0);
		backface-visibility: hidden;
		perspective: 1000;
		-webkit-font-smoothing: antialiased;
	}

	:global(::-webkit-scrollbar) {
		width: 8px;
		height: 8px;
	}

	:global(::-webkit-scrollbar-track) {
		background: hsl(var(--background));
		border-radius: 4px;
	}

	:global(::-webkit-scrollbar-thumb) {
		background: hsl(var(--muted-foreground));
		border-radius: 4px;
	}

	:global(::-webkit-scrollbar-thumb:hover) {
		background: hsl(var(--foreground));
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.loading {
		display: inline-block;
		width: 2rem;
		height: 2rem;
		border: 3px solid hsl(var(--muted-foreground));
		border-top-color: transparent;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.fixed {
		transition: transform 0.1s ease-out;
	}

	select {
		transition:
			background-color 0.2s ease,
			border-color 0.2s ease;
	}

	:global(.apexcharts-tooltip) {
		background: hsl(var(--background)) !important;
		border: 1px solid hsl(var(--border)) !important;
		box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
	}

	:global(.apexcharts-tooltip-title) {
		background: hsl(var(--muted)) !important;
		border-bottom: 1px solid hsl(var(--border)) !important;
	}

	:global(.apexcharts-tooltip-series-group) {
		padding: 8px !important;
	}

	:global(.apexcharts-tooltip-y-group) {
		padding: 4px 0 !important;
	}
</style>
