<script lang="ts">
	import ValuationCard from '$lib/components/ui/valuationcard/ValuationCard.svelte';
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();
	let new_data = data.data[0];
</script>

<div class="valuation">
	<ValuationCard
		symbol={new_data.symbol}
		AnalystTargetPrice={new_data.AnalystTargetPrice}
		AnalystRatingStrongBuy={new_data.AnalystRatingStrongBuy}
		AnalystRatingBuy={new_data.AnalystRatingBuy}
		AnalystRatingHold={new_data.AnalystRatingHold}
		AnalystRatingSell={new_data.AnalystRatingSell}
		AnalystRatingStrongSell={new_data.AnalystRatingStrongSell}
		evtosales={new_data.evtosales}
		evtoebitda={new_data.evtoebitda}
		revenue_per_share_ttm={new_data.revenue_per_share_ttm}
		price_to_sales_ratio_ttm={new_data.price_to_sales_ratio_ttm}
		TrailingPE={new_data.TrailingPE}
		ForwardPE={new_data.ForwardPE}
	/>
</div>
