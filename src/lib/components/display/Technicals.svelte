<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import type { MasterResponse, DailyAnalysis } from '$lib/types/technicals/technicalinterfaces';
	import { TechnicalsTypeGuard } from '$lib/types/technicals/technicalclasses';
	import LineChart from './LineChart.svelte'; // Make sure to create LineChart.svelte in the same directory

	// Props definition
	let { processedData, dailyAnalysis } = $props<{
		processedData: MasterResponse;
		dailyAnalysis: DailyAnalysis;
	}>();

	const technicals = new TechnicalsTypeGuard();
	const xKey = 'date';
	const yKey = 'value';

	const rsiData = $derived(
		dailyAnalysis
			? [
					{
						date: new Date(processedData?.data.last_updated || ''),
						value: dailyAnalysis.indicators.rsi.value
					}
				]
			: []
	);

	const macdData = $derived(
		dailyAnalysis
			? [
					{
						date: new Date(processedData?.data.last_updated || ''),
						value: dailyAnalysis.indicators.macd.values.macd,
						signal: dailyAnalysis.indicators.macd.values.signal,
						histogram: dailyAnalysis.indicators.macd.values.histogram
					}
				]
			: []
	);

	const aroonData = $derived(
		dailyAnalysis
			? [
					{
						date: new Date(processedData?.data.last_updated || ''),
						up: dailyAnalysis.indicators.aroon.values.aroon_up,
						down: dailyAnalysis.indicators.aroon.values.aroon_down
					}
				]
			: []
	);
</script>

I'll help integrate our new LineChart component into the existing Technicals.svelte file. Here's the
modified version: ```svelte
<div
	class="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black px-4 py-6 font-mono text-gray-100"
>
	<div class="w-full max-w-4xl space-y-6 p-4">
		<Card.Root class="border-0 bg-black/40 font-mono backdrop-blur-xl">
			<Card.Header class="pb-2">
				<div class="flex items-baseline justify-between">
					<Card.Title class="text-lg tracking-tight text-green-400">
						Technical Analysis for {processedData.data.ticker}
					</Card.Title>
				</div>
			</Card.Header>
			<Card.Content>
				<div class="space-y-6">
					<!-- RSI Chart -->
					<div class="h-64 rounded-lg bg-black/20 p-4">
						<div class="mb-2 text-xs uppercase tracking-widest text-gray-500">RSI</div>
						<LineChart data={rsiData} xKey="date" yKey="value" title="RSI" />
					</div>

					<!-- MACD Chart -->
					<div class="h-64 rounded-lg bg-black/20 p-4">
						<div class="mb-2 text-xs uppercase tracking-widest text-gray-500">MACD</div>
						<LineChart data={macdData} xKey="date" yKeys={['value', 'signal']} title="MACD" />
					</div>

					<!-- Aroon Chart -->
					<div class="h-64 rounded-lg bg-black/20 p-4">
						<div class="mb-2 text-xs uppercase tracking-widest text-gray-500">Aroon</div>
						<LineChart data={aroonData} xKey="date" yKeys={['up', 'down']} title="Aroon" />
					</div>

					<!-- Technical indicators summary -->
					<div class="grid grid-cols-2 gap-4 md:grid-cols-4">
						<div class="overflow-hidden rounded-lg bg-black/20 p-4">
							<div class="text-xs uppercase tracking-widest text-gray-500">RSI</div>
							<div class="text-2xl font-bold text-green-400">
								{dailyAnalysis.indicators.rsi.value.toFixed(2)}
							</div>
						</div>
						<div class="overflow-hidden rounded-lg bg-black/20 p-4">
							<div class="text-xs uppercase tracking-widest text-gray-500">MACD</div>
							<div class="text-2xl font-bold text-green-400">
								{dailyAnalysis.indicators.macd.values.macd.toFixed(2)}
							</div>
						</div>
						<div class="overflow-hidden rounded-lg bg-black/20 p-4">
							<div class="text-xs uppercase tracking-widest text-gray-500">Signal</div>
							<div class="text-2xl font-bold text-green-400">
								{dailyAnalysis.indicators.macd.values.signal.toFixed(2)}
							</div>
						</div>
						<div class="overflow-hidden rounded-lg bg-black/20 p-4">
							<div class="text-xs uppercase tracking-widest text-gray-500">Histogram</div>
							<div class="text-2xl font-bold text-green-400">
								{dailyAnalysis.indicators.macd.values.histogram.toFixed(2)}
							</div>
						</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>
	</div>
</div>
