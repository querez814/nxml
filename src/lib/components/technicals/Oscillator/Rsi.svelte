<script lang="ts">
	const api_url = import.meta.env.VITE_API_URL;
	import { Chart } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import type { ApexOptions } from 'apexcharts';
	import { GripVertical } from 'lucide-svelte';

	let { ticker }: { ticker: string } = $props();
	let data = $state([]);
	let error = $state<string | null>(null);
	let loading = $state(true);
	let chartInstance = $state<any>(null);

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
					day: 'dd MMM'
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
				format: 'dd MMM yyyy'
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

			// Check if we have room to grow
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
				const response = await fetch(`${api_url}/technicals/rsi/${ticker}`);
				const jsonData = await response.json();

				const today = new Date();
				const sixMonthsAgo = new Date(today.setMonth(today.getMonth() - 6));

				const recentData = jsonData.filter(
					(item: { date: string }) => new Date(item.date) >= sixMonthsAgo
				);
				data = recentData;

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
		<div
			class="drag-handle flex cursor-move items-center border-b border-border bg-muted px-4 py-2"
		>
			<GripVertical class="mr-2 h-4 w-4 text-muted-foreground" />
			<h3 class="flex-1 text-lg font-semibold text-foreground">RSI (14) - {ticker}</h3>
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
