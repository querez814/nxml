<script lang="ts">
	import type { PageData } from './$types';
	import ApexCharts from 'apexcharts';
	import { onMount } from 'svelte';

	let { data }: { data: PageData } = $props();

	// DOM elements for charts
	let priceChartEl: HTMLElement;
	let macdChartEl: HTMLElement;
	let rsiChartEl: HTMLElement;

	// Chart instances
	let priceChart: ApexCharts;
	let macdChart: ApexCharts;
	let rsiChart: ApexCharts;

	// Price chart configuration
	const priceChartOptions = {
		chart: {
			type: 'candlestick',
			height: 400,
			toolbar: {
				show: true,
				tools: {
					download: true,
					selection: true,
					zoom: true,
					zoomin: true,
					zoomout: true,
					pan: true,
					reset: true
				}
			}
		},
		series: [
			{
				data: [
					{
						x: new Date(),
						y: [data.priceData.open, data.priceData.high, data.priceData.low, data.priceData.close]
					}
				]
			}
		],
		xaxis: {
			type: 'datetime',
			labels: {
				datetimeUTC: false
			}
		},
		yaxis: {
			tooltip: {
				enabled: true
			}
		}
	};

	// MACD chart configuration
	const macdChartOptions = {
		chart: {
			type: 'line',
			height: 200,
			toolbar: {
				show: false
			}
		},
		series: [
			{
				name: 'MACD',
				type: 'line',
				data: [data.macd.values.macd]
			},
			{
				name: 'Signal',
				type: 'line',
				data: [data.macd.values.signal]
			},
			{
				name: 'Histogram',
				type: 'bar',
				data: [data.macd.values.histogram]
			}
		],
		colors: ['#2E93fA', '#FF9800', '#66DA26'],
		yaxis: {
			labels: {
				formatter: (value: number) => value.toFixed(2)
			}
		}
	};

	// RSI chart configuration
	const rsiChartOptions = {
		chart: {
			type: 'line',
			height: 200,
			toolbar: {
				show: false
			}
		},
		series: [
			{
				name: 'RSI',
				data: [data.rsi.value]
			}
		],
		yaxis: {
			min: 0,
			max: 100,
			labels: {
				formatter: (value: number) => value.toFixed(1)
			}
		},
		annotations: {
			yaxis: [
				{
					y: 70,
					borderColor: '#FF4560',
					label: { text: 'Overbought' }
				},
				{
					y: 30,
					borderColor: '#00E396',
					label: { text: 'Oversold' }
				}
			]
		}
	};

	onMount(() => {
		// Initialize all charts
		priceChart = new ApexCharts(priceChartEl, priceChartOptions);
		macdChart = new ApexCharts(macdChartEl, macdChartOptions);
		rsiChart = new ApexCharts(rsiChartEl, rsiChartOptions);

		priceChart.render();
		macdChart.render();
		rsiChart.render();

		return () => {
			priceChart?.destroy();
			macdChart?.destroy();
			rsiChart?.destroy();
		};
	});
</script>

<div class="min-h-screen bg-gray-100 p-6">
	<!-- Main Dashboard Container -->
	<div class="mx-auto max-w-7xl space-y-6">
		<!-- Header Section -->
		<div class="rounded-lg bg-white p-6 shadow-sm">
			<h1 class="text-3xl font-bold text-gray-800">Technical Analysis Dashboard</h1>
			<div class="mt-4 grid grid-cols-3 gap-4">
				<div class="rounded-md bg-gray-50 p-4">
					<p class="text-sm text-gray-500">Overall Trend</p>
					<p
						class="text-lg font-semibold {data.summary.overall_trend === 'bullish'
							? 'text-green-600'
							: 'text-red-600'}"
					>
						{data.summary.overall_trend.toUpperCase()}
					</p>
				</div>
				<div class="rounded-md bg-gray-50 p-4">
					<p class="text-sm text-gray-500">Signal Strength</p>
					<p class="text-lg font-semibold">{data.summary.signal_strength}</p>
				</div>
				<div class="rounded-md bg-gray-50 p-4">
					<p class="text-sm text-gray-500">Recommended Action</p>
					<p class="text-lg font-semibold">{data.summary.recommended_action.toUpperCase()}</p>
				</div>
			</div>
		</div>

		<!-- Price Chart Section -->
		<div class="rounded-lg bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold">Price Action</h2>
			<div bind:this={priceChartEl} />
		</div>

		<!-- Technical Indicators Section -->
		<div class="grid grid-cols-2 gap-6">
			<!-- MACD Panel -->
			<div class="rounded-lg bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-semibold">MACD</h2>
				<div bind:this={macdChartEl} />
				<div class="mt-4 grid grid-cols-2 gap-4 text-sm">
					<div>
						<p class="text-gray-500">Trend</p>
						<p class="font-semibold">{data.macd.signals.trend}</p>
					</div>
					<div>
						<p class="text-gray-500">Momentum</p>
						<p class="font-semibold">{data.macd.signals.momentum}</p>
					</div>
				</div>
			</div>

			<!-- RSI Panel -->
			<div class="rounded-lg bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-semibold">RSI</h2>
				<div bind:this={rsiChartEl} />
				<div class="mt-4 grid grid-cols-2 gap-4 text-sm">
					<div>
						<p class="text-gray-500">Status</p>
						<p class="font-semibold">{data.rsi.status}</p>
					</div>
					<div>
						<p class="text-gray-500">Trend</p>
						<p class="font-semibold">{data.rsi.trend}</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Additional Indicators -->
		<div class="grid grid-cols-2 gap-6">
			<!-- Aroon Panel -->
			<div class="rounded-lg bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-semibold">Aroon</h2>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-sm text-gray-500">Up</p>
						<p class="text-lg font-semibold">{data.aroon.values.aroon_up.toFixed(2)}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">Down</p>
						<p class="text-lg font-semibold">{data.aroon.values.aroon_down.toFixed(2)}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">Trend</p>
						<p class="font-semibold">{data.aroon.signals.trend}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">Signal</p>
						<p class="font-semibold">{data.aroon.signals.signal}</p>
					</div>
				</div>
			</div>

			<!-- Stochastic Panel -->
			<div class="rounded-lg bg-white p-6 shadow-sm">
				<h2 class="mb-4 text-xl font-semibold">Stochastic</h2>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<p class="text-sm text-gray-500">K-Line</p>
						<p class="text-lg font-semibold">{data.stochastic.values.k_line.toFixed(2)}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">D-Line</p>
						<p class="text-lg font-semibold">{data.stochastic.values.d_line.toFixed(2)}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">Status</p>
						<p class="font-semibold">{data.stochastic.signals.status}</p>
					</div>
					<div>
						<p class="text-sm text-gray-500">Signal</p>
						<p class="font-semibold">{data.stochastic.signals.signal}</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
