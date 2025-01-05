<script lang="ts">
	import * as Card from '../card';

	let {
		symbol,
		AnalystTargetPrice,
		AnalystRatingStrongBuy,
		AnalystRatingBuy,
		AnalystRatingHold,
		AnalystRatingSell,
		AnalystRatingStrongSell,
		evtosales,
		evtoebitda,
		revenue_per_share_ttm,
		price_to_sales_ratio_ttm,
		TrailingPE,
		ForwardPE
	} = $props();
</script>

<Card.Root
	class="
    background-background 
    mx-auto 
    max-w-md 
    transform 
    overflow-hidden 
    rounded-xl 
    shadow-lg 
    ring-1
    ring-green-200 
    transition-all 
    duration-300 
    hover:scale-[1.02]
    hover:shadow-2xl
  "
>
	<div class="bg-gradient-to-r from-green-600 via-emerald-500 to-green-400 p-6">
		<Card.Header>
			<Card.Title class="text-2xl font-extrabold tracking-tight text-slate-300">
				{symbol} Summary
			</Card.Title>
			<Card.Description class="text-sm text-green-50/90">Some Important Data</Card.Description>
		</Card.Header>
	</div>

	<div class="p-6 text-gray-800">
		<Card.Content class="mb-0.5">
			<h3 class="mb-2 text-lg font-semibold uppercase tracking-wider text-green-700">
				Analyst Price Target
			</h3>
			<p class="text-2xl font-bold text-slate-300">{AnalystTargetPrice}</p>
		</Card.Content>

		<Card.Content>
			<h3 class="mb-0.5 text-lg font-semibold uppercase tracking-wider text-green-700">
				Analyst Rating
			</h3>
			<ul class="list-inside list-disc space-y-1 text-xl text-slate-300">
				<li>
					<strong class="text-xl text-green-700">Strong Buy:</strong>
					{AnalystRatingStrongBuy}
				</li>
				<li><strong class="text-xl text-green-700">Buy:</strong> {AnalystRatingBuy}</li>
				<li><strong class="text-xl text-green-700">Hold:</strong> {AnalystRatingHold}</li>
				<li><strong class="text-xl text-green-700">Sell:</strong> {AnalystRatingSell}</li>
				<li>
					<strong class="text-xl text-green-700">Strong Sell:</strong>
					{AnalystRatingStrongSell}
				</li>
			</ul>
		</Card.Content>

		<Card.Content>
			<h3 class="mb-0.5 text-lg font-semibold uppercase tracking-wider text-green-700">
				Current Valuation
			</h3>
			<ul class="list-inside list-disc space-y-1 text-slate-300">
				<li><strong class="text-xl text-green-700">EV to Sales:</strong> {evtosales}</li>
				<li><strong class="text-xl text-green-700">EV to EBITDA:</strong> {evtoebitda}</li>
				<li>
					<strong class="text-xl text-green-700">Revenue per Share (TTM):</strong>
					{revenue_per_share_ttm}
				</li>
				<li>
					<strong class="text-xl text-green-700">Price to Sales (TTM):</strong>
					{price_to_sales_ratio_ttm}
				</li>
				<li><strong class=" text-xl text-green-700">Trailing PE:</strong> {TrailingPE}</li>
				<li><strong class=" text-xl text-green-700">Forward PE:</strong> {ForwardPE}</li>
			</ul>
		</Card.Content>
	</div>
</Card.Root>
