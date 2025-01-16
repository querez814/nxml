<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Chart, Svg, Axis, Bar } from 'layerchart';
	import type { MasterResponse, DailyAnalysis } from '$lib/types/technicals/technicalinterfaces';
	import { TechnicalsTypeGuard } from '$lib/types/technicals/technicalclasses';

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

<div class="w-full max-w-4xl space-y-6 p-4">
	<Card.Root class="border-0 bg-black/40 font-mono backdrop-blur-xl">
		<Card.Header class="font-mono text-2xl">
			Current Technical Setup for {processedData?.data.ticker}
		</Card.Header>
		<Card.Content>
			<div class="h-[300px] rounded border p-4">
				<Chart data={rsiData} x="date" y="value" />
			</div>
		</Card.Content>
	</Card.Root>
</div>
