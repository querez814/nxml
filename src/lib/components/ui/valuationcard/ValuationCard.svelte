<script lang="ts">
	import * as Card from '../card';
	import { formatRatio } from '../../../../api/valuation/valuationdata';
	import type { ValuationLayout } from '../../../../api/valuation/valuationdata';

	let {
		symbol,
		layout,
		AnalystTargetPrice = null,
		AnalystRatingStrongBuy = null,
		AnalystRatingBuy = null,
		AnalystRatingHold = null,
		AnalystRatingSell = null,
		AnalystRatingStrongSell = null
	}: {
		symbol: string;
		layout: ValuationLayout | null;
		AnalystTargetPrice?: number | null;
		AnalystRatingStrongBuy?: number | null;
		AnalystRatingBuy?: number | null;
		AnalystRatingHold?: number | null;
		AnalystRatingSell?: number | null;
		AnalystRatingStrongSell?: number | null;
	} = $props();

	const ratios = $derived.by(() => {
		if (!layout) return [] as { key: string; label: string; value: string }[];
		return layout.order
			.map((key) => ({
				key,
				label: layout.labels[key] ?? key,
				value: formatRatio(key, layout.values[key] ?? null)
			}))
			.filter((r) => r.value !== '-');
	});
</script>

<Card.Root
	class="background-background
    mx-auto
    mb-4
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
			<Card.Title class="text-center font-mono text-5xl tracking-tight text-white">
				{symbol}
			</Card.Title>
			{#if layout?.sector}
				<p class="text-center font-mono text-xs text-white/80">{layout.sector}</p>
			{/if}
		</Card.Header>
	</div>

	<div class="p-6 text-gray-800">
		{#if AnalystTargetPrice !== null && AnalystTargetPrice !== undefined}
			<Card.Content class="mb-2">
				<h3 class="mb-2 text-2xl font-semibold uppercase tracking-wider text-green-700">
					Analyst Price Target
				</h3>
				<p class="text-2xl font-bold text-slate-300">{AnalystTargetPrice}</p>
			</Card.Content>
		{/if}

		{#if AnalystRatingStrongBuy !== null && AnalystRatingStrongBuy !== undefined}
			<Card.Content>
				<h3 class="mb-1 text-2xl font-semibold uppercase tracking-wider text-green-700">
					Analyst Rating
				</h3>
				<ul class="list-inside list-disc space-y-1 text-xl text-slate-300">
					<li><strong class="text-xl text-green-700">Strong Buy:</strong> {AnalystRatingStrongBuy}</li>
					<li><strong class="text-xl text-green-700">Buy:</strong> {AnalystRatingBuy}</li>
					<li><strong class="text-xl text-green-700">Hold:</strong> {AnalystRatingHold}</li>
					<li><strong class="text-xl text-green-700">Sell:</strong> {AnalystRatingSell}</li>
					<li><strong class="text-xl text-green-700">Strong Sell:</strong> {AnalystRatingStrongSell}</li>
				</ul>
			</Card.Content>
		{/if}

		<Card.Content>
			<h3 class="mb-2 text-2xl font-semibold uppercase tracking-wider text-green-700">
				Current Valuation
			</h3>
			{#if ratios.length === 0}
				<p class="text-slate-300">No valuation ratios available.</p>
			{:else}
				<ul class="list-inside list-disc space-y-1 text-xl text-slate-300">
					{#each ratios as ratio (ratio.key)}
						<li>
							<strong class="text-xl text-green-700">{ratio.label}:</strong>
							{ratio.value}
						</li>
					{/each}
				</ul>
			{/if}
		</Card.Content>
	</div>
</Card.Root>
