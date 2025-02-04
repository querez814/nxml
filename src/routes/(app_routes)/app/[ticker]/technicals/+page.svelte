<script lang="ts">
	import type { PageData } from '../$types';
	import Rsi from '$lib/components/technicals/Oscillator/Rsi.svelte';
	import Stochastic from '$lib/components/technicals/Oscillator/Stochastic.svelte';
	import Momentum from '$lib/components/technicals/Momentum/Momentum.svelte';
	import DailyPrice from '$lib/components/technicals/General/DailyPrice.svelte';

	let { data }: { data: PageData } = $props();
	console.log('Page Data', data);
	let ticker = data.ticker;
	console.log('ticker', ticker);
</script>

<Rsi {ticker} />
<Stochastic {ticker} />
<DailyPrice {ticker} />
<Momentum {ticker} />
