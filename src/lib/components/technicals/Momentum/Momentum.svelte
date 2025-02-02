<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import * as Card from '$lib/components/ui/card';
	import { TrendingDown, TrendingUp, GripVertical, Info } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let { ticker }: { ticker: string } = $props();
	let data = $state<any>(null);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// Drag and resize state
	let position = $state({ x: 20, y: 20 });
	let size = $state({ width: 800, height: 500 });
	let isDragging = $state(false);
	let isResizing = $state(false);
	let startPosition = { x: 0, y: 0 };
	let container: HTMLElement;
	let lastCursor = { x: 0, y: 0 };

	// Helper function to determine score visuals
	function getScoreDisplay(score: number) {
		const isPositive = score >= 0;
		const absScore = Math.abs(score);
		const color = isPositive ? 'text-green-500' : 'text-red-500';
		const prefix = isPositive ? '+' : '-';
		return { color, displayValue: `${prefix}${absScore.toFixed(2)}` };
	}

	// Helper function for consistency color
	function getConsistencyColor(value: number): string {
		if (value >= 75) return 'text-green-500';
		if (value >= 50) return 'text-yellow-500';
		return 'text-red-500';
	}

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
		event.stopPropagation();
	}

	function handleResizeEnd() {
		isResizing = false;
	}

	onMount(() => {
		const fetchData = async () => {
			try {
				const response = await fetch(`${api_url}/technicals/momentum/${ticker}`);
				const jsonData = await response.json();
				data = jsonData;
			} catch (err) {
				error = err instanceof Error ? err.message : 'Failed to fetch trend data';
			} finally {
				loading = false;
			}
		};

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
		{#if loading}
			<div class="flex h-full items-center justify-center">
				<p class="text-muted-foreground">Loading trend analysis...</p>
			</div>
		{:else if error}
			<div class="flex h-full items-center justify-center">
				<p class="text-destructive">{error}</p>
			</div>
		{:else if data}
			<!-- Header -->
			<div
				class="drag-handle flex cursor-move items-center border-b border-border bg-muted px-4 py-2"
			>
				<GripVertical class="mr-2 h-4 w-4 text-muted-foreground" />
				<div class="flex flex-1 items-center justify-between">
					<h3 class="text-lg font-semibold text-foreground">
						{data.symbol} Market Trend Analysis
					</h3>
					<span class="text-sm text-muted-foreground">{data.period}</span>
				</div>
			</div>

			<div class="flex h-[calc(100%-3rem)] flex-col gap-4 overflow-y-auto p-4">
				<!-- Market Condition Banner -->
				<div class="flex items-center justify-between rounded-lg bg-muted/50 p-3">
					<span class="font-medium">Current Market Trend:</span>
					<span class={data.market_condition.includes('UP') ? 'text-green-500' : 'text-red-500'}>
						{data.market_condition.replace(/_/g, ' ')}
					</span>
				</div>

				<!-- Indicator Cards -->
				<div class="grid grid-cols-2 gap-4">
					<!-- MACD -->
					<div class="rounded-lg border border-border p-4">
						<div class="mb-2 flex items-center justify-between">
							<div class="flex items-center gap-2">
								<span class="font-medium">MACD Signal</span>
								<Info class="h-4 w-4 text-muted-foreground" />
							</div>
							<span class={getScoreDisplay(data.component_scores.macd).color}>
								{getScoreDisplay(data.component_scores.macd).displayValue}
							</span>
						</div>
						<div class="flex items-center justify-between text-sm">
							<div>
								<span class="text-muted-foreground">Signal Confidence:</span>
								<span class={getConsistencyColor(data.trend_analysis.macd_trend.consistency)}>
									{data.trend_analysis.macd_trend.consistency}%
								</span>
							</div>
							<div class="flex items-center gap-1">
								<span class="text-muted-foreground">Trend Strength:</span>
								<span
									class={data.trend_analysis.macd_trend.direction === 'up'
										? 'text-green-500'
										: 'text-red-500'}
								>
									{(data.trend_analysis.macd_trend.strength * 100).toFixed(1)}%
								</span>
							</div>
						</div>
					</div>

					<!-- Aroon -->
					<div class="rounded-lg border border-border p-4">
						<div class="mb-2 flex items-center justify-between">
							<div class="flex items-center gap-2">
								<span class="font-medium">Aroon Trend</span>
								<Info class="h-4 w-4 text-muted-foreground" />
							</div>
							<span class={getScoreDisplay(data.component_scores.aroon).color}>
								{getScoreDisplay(data.component_scores.aroon).displayValue}
							</span>
						</div>
						<div class="flex items-center justify-between text-sm">
							<div>
								<span class="text-muted-foreground">Signal Confidence:</span>
								<span class={getConsistencyColor(data.trend_analysis.aroon_trend.consistency)}>
									{data.trend_analysis.aroon_trend.consistency}%
								</span>
							</div>
							<div class="flex items-center gap-1">
								<span class="text-muted-foreground">Trend Strength:</span>
								<span
									class={data.trend_analysis.aroon_trend.direction === 'up'
										? 'text-green-500'
										: 'text-red-500'}
								>
									{(data.trend_analysis.aroon_trend.strength * 100).toFixed(1)}%
								</span>
							</div>
						</div>
					</div>

					<!-- Momentum -->
					<div class="rounded-lg border border-border p-4">
						<div class="mb-2 flex items-center justify-between">
							<div class="flex items-center gap-2">
								<span class="font-medium">Price Momentum</span>
								<Info class="h-4 w-4 text-muted-foreground" />
							</div>
							<span class={getScoreDisplay(data.component_scores.momentum).color}>
								{getScoreDisplay(data.component_scores.momentum).displayValue}
							</span>
						</div>
						<div class="flex items-center justify-between text-sm">
							<div>
								<span class="text-muted-foreground">Signal Confidence:</span>
								<span class={getConsistencyColor(data.trend_analysis.momentum_trend.consistency)}>
									{data.trend_analysis.momentum_trend.consistency}%
								</span>
							</div>
							<div class="flex items-center gap-1">
								<span class="text-muted-foreground">Trend Strength:</span>
								<span
									class={data.trend_analysis.momentum_trend.direction === 'up'
										? 'text-green-500'
										: 'text-red-500'}
								>
									{(data.trend_analysis.momentum_trend.strength * 100).toFixed(1)}%
								</span>
							</div>
						</div>
					</div>

					<!-- Stochastic -->
					<div class="rounded-lg border border-border p-4">
						<div class="mb-2 flex items-center justify-between">
							<div class="flex items-center gap-2">
								<span class="font-medium">Stochastic Signal</span>
								<Info class="h-4 w-4 text-muted-foreground" />
							</div>
							<span class={getScoreDisplay(data.component_scores.stochastic).color}>
								{getScoreDisplay(data.component_scores.stochastic).displayValue}
							</span>
						</div>
						<div class="flex items-center justify-between text-sm">
							<div>
								<span class="text-muted-foreground">Signal Confidence:</span>
								<span class={getConsistencyColor(data.trend_analysis.stochastic_trend.consistency)}>
									{data.trend_analysis.stochastic_trend.consistency}%
								</span>
							</div>
							<div class="flex items-center gap-1">
								<span class="text-muted-foreground">Trend Strength:</span>
								<span
									class={data.trend_analysis.stochastic_trend.direction === 'up'
										? 'text-green-500'
										: 'text-red-500'}
								>
									{(data.trend_analysis.stochastic_trend.strength * 100).toFixed(1)}%
								</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Overall Trend -->
				<div class="rounded-lg border border-border p-4">
					<div class="mb-2 flex items-center justify-between">
						<span class="font-medium">Overall Trend Analysis</span>
						<div class="flex items-center gap-2">
							<span class="text-sm text-muted-foreground">Trend Score:</span>
							<span class={getScoreDisplay(data.momentum_score).color}>
								{getScoreDisplay(data.momentum_score).displayValue}
							</span>
						</div>
					</div>
					<div class="space-y-2">
						<div class="flex items-center justify-between text-sm">
							<span class="text-muted-foreground">Signal Consistency:</span>
							<span class={getConsistencyColor(data.trend_analysis.consistency)}>
								{data.trend_analysis.consistency}%
							</span>
						</div>
						<div class="h-2 overflow-hidden rounded-full bg-muted">
							<div
								class="h-full bg-blue-500 transition-all"
								style="width: {data.trend_analysis.consistency}%"
							/>
						</div>
					</div>
				</div>
			</div>

			<!-- Resize Handle -->
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
		{/if}
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
</style>
