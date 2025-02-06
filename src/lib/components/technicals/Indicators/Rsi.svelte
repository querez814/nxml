<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import { Chart } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import { GripVertical, ArrowUpCircle, ArrowDownCircle } from 'lucide-svelte';
	import type { ApexOptions } from 'apexcharts';

	let { ticker }: { ticker: string } = $props();
	let data = $state<Array<{ date: string; rsi: number }>>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);
	let chartInstance = $state<any>(null);
	let selectedInterval = $state('daily');
	let currentRSI = $state<number | null>(null);

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

	// Drag and resize state
	let position = $state({ x: 20, y: 20 });
	let size = $state({ width: 800, height: 500 });
	let isDragging = $state(false);
	let isResizing = $state(false);
	let startPosition = { x: 0, y: 0 };
	let container: HTMLElement;
	let lastCursor = { x: 0, y: 0 };

	const options: ApexOptions = {
		series: [
			{
				name: 'RSI',
				data: []
			}
		],
		chart: {
			type: 'line',
			height: '100%',
			width: '100%',
			toolbar: {
				show: false
			},
			animations: {
				enabled: false
			},
			background: '#1a1a1a',
			redrawOnWindowResize: true,
			redrawOnParentResize: true,
			zoom: {
				enabled: false
			},
			events: {
				updated: function (chartContext: any) {
					const series = chartContext.series[0];
					if (series?.data?.length > 0) {
						currentRSI = series.data[series.data.length - 1].y;
					}
				}
			}
		},
		stroke: {
			curve: 'smooth',
			width: 2
		},
		colors: ['#4299E1'],
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
			},
			padding: {
				right: 10
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
					day: 'dd MMM',
					hour: 'HH:mm'
				},
				trim: true
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			tooltip: {
				enabled: false
			}
		},
		yaxis: {
			min: 0,
			max: 100,
			tickAmount: 4,
			labels: {
				style: {
					colors: '#A0AEC0'
				},
				formatter: (value: number) => value.toFixed(0)
			},
			tooltip: {
				enabled: false
			}
		},
		annotations: {
			yaxis: [
				{
					y: 70,
					borderColor: '#F56565',
					label: {
						text: 'Overbought',
						style: {
							color: '#fff',
							background: '#F56565'
						}
					}
				},
				{
					y: 30,
					borderColor: '#48BB78',
					label: {
						text: 'Oversold',
						style: {
							color: '#fff',
							background: '#48BB78'
						}
					}
				}
			]
		},
		tooltip: {
			x: {
				format: 'dd MMM yyyy HH:mm'
			},
			y: {
				formatter: (value: number) => `RSI: ${value.toFixed(2)}`
			},
			theme: 'dark',
			shared: false,
			intersect: true,
			followCursor: true
		},
		states: {
			hover: {
				filter: {
					type: 'none'
				}
			},
			active: {
				filter: {
					type: 'none'
				}
			}
		}
	};

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

	async function fetchData() {
		loading = true;
		error = null;

		try {
			const response = await fetch(`${api_url}/technicals/rsi/${selectedInterval}/${ticker}`);
			const jsonData = await response.json();

			if (!Array.isArray(jsonData)) {
				throw new Error('Invalid data format received from server');
			}

			// Filter data based on interval
			const today = new Date();
			let filterDate = new Date();

			switch (selectedInterval) {
				case '1min':
				case '5min':
					filterDate = new Date(today.getTime() - 24 * 60 * 60 * 1000); // 24 hours
					break;
				case '15min':
				case '30min':
				case '60min':
					filterDate = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000); // 7 days
					break;
				case 'daily':
					filterDate = new Date(today.setMonth(today.getMonth() - 6)); // 6 months
					break;
				case 'weekly':
					filterDate = new Date(today.setMonth(today.getMonth() - 12)); // 1 year
					break;
				case 'monthly':
					filterDate = new Date(today.setMonth(today.getMonth() - 24)); // 2 years
					break;
			}

			const recentData = jsonData.filter(
				(item: { date: string }) => new Date(item.date) >= filterDate
			);
			data = recentData;

			if (recentData.length > 0) {
				currentRSI = recentData[recentData.length - 1].rsi;
			}

			options.series = [
				{
					name: 'RSI',
					data: recentData.map((item: { date: string; rsi: number }) => ({
						x: new Date(item.date).getTime(),
						y: item.rsi,
						marker: {
							size: item.rsi <= 30 || item.rsi >= 70 ? 6 : 4,
							fillColor: item.rsi <= 30 ? '#48BB78' : item.rsi >= 70 ? '#F56565' : '#4299E1',
							strokeColor: '#1a1a1a',
							strokeWidth: 2
						}
					}))
				}
			];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to fetch market data';
			console.error('Fetch error:', error, err);
		} finally {
			loading = false;
		}
	}

	$effect(() => {
		if (selectedInterval) {
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
				<h3 class="text-lg font-semibold text-foreground">RSI (14) - {ticker}</h3>
			</div>

			<div class="flex items-center space-x-4">
				{#if currentRSI !== null}
					<div class="flex items-center space-x-2">
						<span class="text-sm font-medium text-muted-foreground">RSI:</span>
						<span
							class="text-lg font-bold"
							class:text-red-500={currentRSI >= 70}
							class:text-green-500={currentRSI <= 30}
							class:text-blue-500={currentRSI > 30 && currentRSI < 70}
						>
							{currentRSI.toFixed(2)}
						</span>

						{#if currentRSI >= 70}
							<div class="flex items-center text-red-500">
								<ArrowDownCircle class="h-5 w-5" />
								<span class="ml-1 text-sm font-medium">Sell</span>
							</div>
						{:else if currentRSI <= 30}
							<div class="flex items-center text-green-500">
								<ArrowUpCircle class="h-5 w-5" />
								<span class="ml-1 text-sm font-medium">Buy</span>
							</div>
						{/if}
					</div>
				{/if}

				<div class="relative w-32">
					<select
						value={selectedInterval}
						onchange={(e) => (selectedInterval = e.currentTarget.value)}
						class="h-8 w-full rounded-md border border-border bg-background px-3 py-1 text-sm text-foreground hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
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
				<p class="text-muted-foreground">Loading...</p>
			{:else if error}
				<p class="text-destructive">{error}</p>
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
			/>
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
