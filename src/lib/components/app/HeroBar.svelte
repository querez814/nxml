<script lang="ts">
	import type { ValuationLayout } from '../../../api/valuation/valuationdata';

	let {
		ticker,
		layout,
		latestPrice,
		dayChangePct
	}: {
		ticker: string;
		layout: ValuationLayout | null;
		latestPrice: number | null;
		dayChangePct: number | null;
	} = $props();

	const target = $derived(layout?.latest?.analyst_target_price ?? null);
	const hi = $derived(layout?.latest?.week52_high ?? null);
	const lo = $derived(layout?.latest?.week52_low ?? null);
	const cap = $derived(layout?.latest?.latest_market_cap ?? layout?.latest?.market_cap ?? null);
	const ev = $derived(layout?.latest?.latest_enterprise_value ?? layout?.latest?.enterprise_value ?? null);

	const pctIn52 = $derived.by(() => {
		if (latestPrice == null || hi == null || lo == null || hi <= lo) return null;
		return ((latestPrice - lo) / (hi - lo)) * 100;
	});

	function fmtCap(n: number | null): string {
		if (n == null || !Number.isFinite(n)) return '—';
		if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
		if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`;
		if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`;
		return `$${n.toFixed(0)}`;
	}

	const ratings = $derived.by(() => {
		const l = layout?.latest;
		if (!l) return null;
		const parts = [
			{ k: 'Strong buy', v: l.analyst_rating_strong_buy },
			{ k: 'Buy', v: l.analyst_rating_buy },
			{ k: 'Hold', v: l.analyst_rating_hold },
			{ k: 'Sell', v: l.analyst_rating_sell },
			{ k: 'Strong sell', v: l.analyst_rating_strong_sell }
		].filter((p) => p.v != null && p.v > 0) as { k: string; v: number }[];
		const sum = parts.reduce((a, p) => a + p.v, 0);
		if (!sum) return null;
		return parts.map((p) => ({ ...p, pct: (p.v / sum) * 100 }));
	});
</script>

<div
	class="flex flex-col gap-4 rounded-lg border border-gray-800 bg-[#111215] px-4 py-4 font-mono text-sm text-gray-200 md:flex-row md:flex-wrap md:items-center md:justify-between"
>
	<div class="flex flex-wrap items-baseline gap-3">
		<span class="text-2xl font-bold text-emerald-400">{ticker}</span>
		{#if layout?.sector}
			<span class="text-xs text-gray-500">{layout.sector}{layout.industry ? ` · ${layout.industry}` : ''}</span>
		{/if}
	</div>

	<div class="flex flex-wrap items-center gap-6">
		<div>
			<p class="text-[10px] uppercase text-gray-500">Price</p>
			<p class="text-lg text-white">
				{latestPrice != null ? `$${latestPrice.toFixed(2)}` : '—'}
				{#if dayChangePct != null}
					<span class={dayChangePct >= 0 ? 'text-emerald-400' : 'text-red-400'}>
						{dayChangePct >= 0 ? '+' : ''}{dayChangePct.toFixed(2)}%
					</span>
				{/if}
			</p>
		</div>
		<div>
			<p class="text-[10px] uppercase text-gray-500">Mkt cap</p>
			<p class="text-white">{fmtCap(cap)}</p>
		</div>
		<div>
			<p class="text-[10px] uppercase text-gray-500">EV</p>
			<p class="text-white">{fmtCap(ev)}</p>
		</div>
	</div>

	<div class="min-w-[200px] flex-1 md:max-w-md">
		<p class="mb-1 text-[10px] uppercase text-gray-500">52-week range</p>
		{#if hi != null && lo != null && latestPrice != null}
			<div class="flex items-center gap-2 text-[10px] text-gray-500">
				<span>${lo.toFixed(2)}</span>
				<div class="relative h-2 flex-1 rounded-full bg-gray-800">
					<div class="absolute inset-y-0 left-0 rounded-full bg-emerald-500/40" style:width="100%"></div>
					{#if pctIn52 != null}
						<div
							class="absolute top-1/2 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-emerald-400 bg-gray-950"
							style:left="{Math.min(100, Math.max(0, pctIn52))}%"
						></div>
					{/if}
				</div>
				<span>${hi.toFixed(2)}</span>
			</div>
		{:else}
			<p class="text-xs text-gray-500">—</p>
		{/if}
	</div>

	<div class="min-w-[220px]">
		<p class="mb-1 text-[10px] uppercase text-gray-500">Analyst target</p>
		<div class="flex items-baseline gap-2">
			<span class="text-lg text-emerald-400">
				{target != null ? `$${target.toFixed(2)}` : '—'}
			</span>
			{#if target != null && latestPrice != null && latestPrice > 0}
				<span class={target >= latestPrice ? 'text-emerald-400' : 'text-amber-400'}>
					{(((target - latestPrice) / latestPrice) * 100).toFixed(1)}% vs spot
				</span>
			{/if}
		</div>
		{#if ratings?.length}
			<div class="mt-2 flex h-2 overflow-hidden rounded-full bg-gray-800">
				{#each ratings as r (r.k)}
					<div
						class="h-full bg-emerald-500/70 first:rounded-l last:rounded-r"
						style:width="{r.pct}%"
						title="{r.k}: {r.v}"
					></div>
				{/each}
			</div>
			<div class="mt-1 flex flex-wrap gap-x-2 text-[9px] text-gray-500">
				{#each ratings as r (r.k)}
					<span>{r.k} {r.v}</span>
				{/each}
			</div>
		{/if}
	</div>
</div>
