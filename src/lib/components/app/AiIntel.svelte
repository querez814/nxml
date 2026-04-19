<script lang="ts">
	import * as Accordion from '$lib/components/ui/accordion';
	import NewsRecapPanel from '$lib/components/news/NewsRecapPanel.svelte';
	import type { NewsRecapPayload } from '$lib/api/newsRecap';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';
	import { fetchFinancingRisk, fetchRevenueSegments } from '$lib/api/analysisClient';

	let {
		ticker,
		newsRecap,
		newsLoading,
		newsError
	}: {
		ticker: string;
		newsRecap: NewsRecapPayload | null;
		newsLoading: boolean;
		newsError: string | null;
	} = $props();

	let finLoading = $state(false);
	let finError = $state<string | null>(null);
	let finResult = $state<Awaited<ReturnType<typeof fetchFinancingRisk>> | null>(null);

	let segLoading = $state(false);
	let segError = $state<string | null>(null);
	let segResult = $state<Awaited<ReturnType<typeof fetchRevenueSegments>> | null>(null);

	const finHtml = $derived.by(() => {
		if (!finResult) return '';
		const text = [finResult.financing_risk_summary, finResult.financing_risk_narrative].filter(Boolean).join('\n\n');
		if (!text) return '';
		return DOMPurify.sanitize(marked.parse(text) as string, { USE_PROFILES: { html: true } });
	});

	async function runFinancingRisk() {
		if (!ticker) return;
		finLoading = true;
		finError = null;
		try {
			finResult = await fetchFinancingRisk(ticker);
		} catch (e) {
			finError = e instanceof Error ? e.message : 'Request failed';
			finResult = null;
		} finally {
			finLoading = false;
		}
	}

	let accordionOpen = $state<string[]>(['news']);

	async function runSegments() {
		if (!ticker) return;
		segLoading = true;
		segError = null;
		try {
			segResult = await fetchRevenueSegments(ticker);
		} catch (e) {
			segError = e instanceof Error ? e.message : 'Request failed';
			segResult = null;
		} finally {
			segLoading = false;
		}
	}
</script>

<div class="rounded-lg border border-gray-800 bg-[#111215]">
	<Accordion.Root class="w-full" type="multiple" bind:value={accordionOpen}>
		<Accordion.Item value="news" class="border-b border-gray-800 px-4">
			<Accordion.Trigger class="flex w-full items-center justify-between py-3 font-mono text-sm text-gray-200 hover:no-underline">
				<span>Weekly news recap</span>
				<span class="text-[10px] text-gray-500">auto-loaded</span>
			</Accordion.Trigger>
			<Accordion.Content class="pb-4">
				{#if newsLoading}
					<p class="text-sm text-gray-400">Loading news recap…</p>
				{:else}
					<NewsRecapPanel recap={newsRecap} heading={`${ticker} — news recap (past week)`} />
				{/if}
				{#if newsError}
					<p class="mt-2 text-xs text-amber-400/90">{newsError}</p>
				{/if}
			</Accordion.Content>
		</Accordion.Item>

		<Accordion.Item value="financing" class="border-b border-gray-800 px-4">
			<Accordion.Trigger class="flex w-full items-center justify-between py-3 font-mono text-sm text-gray-200 hover:no-underline">
				<span>Financing risk</span>
				<span class="text-[10px] text-amber-400/90">30–90s · Run</span>
			</Accordion.Trigger>
			<Accordion.Content class="space-y-3 pb-4">
				<button
					type="button"
					class="rounded border border-amber-400/40 px-3 py-2 font-mono text-xs text-amber-400 hover:bg-amber-400/10 disabled:opacity-50"
					onclick={runFinancingRisk}
					disabled={finLoading || !ticker}
				>
					{finLoading ? 'Fetching 10-Q & analyzing…' : 'Run financing risk analysis'}
				</button>
				{#if finLoading}
					<p class="text-sm text-gray-400">
						Fetching latest 10-Q from SEC, extracting financing sections, and generating analysis. This may take
						30–90 seconds.
					</p>
				{:else if finError}
					<p class="text-sm text-red-400">{finError}</p>
				{:else if finResult && finHtml}
					<div class="max-h-[min(50vh,420px)] overflow-x-auto overflow-y-auto rounded border border-gray-800/60">
						<div
							class="prose prose-invert prose-sm min-w-0 max-w-none p-3 text-gray-300 [&_table]:block [&_table]:w-max [&_table]:min-w-full [&_table]:border-collapse [&_table]:border [&_table]:border-gray-700 [&_td]:border [&_td]:border-gray-700 [&_td]:px-2 [&_td]:py-1 [&_th]:border [&_th]:border-gray-700 [&_th]:px-2 [&_th]:py-1 [&_h3]:mt-4 [&_ul]:list-disc [&_ul]:pl-5"
						>
							<!-- eslint-disable-next-line svelte/no-at-html-tags -->
							{@html finHtml}
						</div>
					</div>
				{/if}
			</Accordion.Content>
		</Accordion.Item>

		<Accordion.Item value="segments" class="px-4">
			<Accordion.Trigger class="flex w-full items-center justify-between py-3 font-mono text-sm text-gray-200 hover:no-underline">
				<span>Revenue segments</span>
				<span class="text-[10px] text-amber-400/90">30–120s · Run</span>
			</Accordion.Trigger>
			<Accordion.Content class="space-y-3 pb-4">
				<button
					type="button"
					class="rounded border border-amber-400/40 px-3 py-2 font-mono text-xs text-amber-400 hover:bg-amber-400/10 disabled:opacity-50"
					onclick={runSegments}
					disabled={segLoading || !ticker}
				>
					{segLoading ? 'Analyzing segment disclosures…' : 'Run revenue segment analysis'}
				</button>
				{#if segLoading}
					<p class="text-sm text-gray-400">Fetching segment tables and running analysis — may take 30–120 seconds.</p>
				{:else if segError}
					<p class="text-sm text-red-400">{segError}</p>
				{:else if segResult}
					{#if segResult.has_segment_disclosure && segResult.segments?.length}
						<p class="text-sm text-gray-400">
							Found {segResult.segments.length} segment line(s). Open the income statement drawer → Revenue
							segments tab for the full matrix.
						</p>
					{:else}
						<p class="text-sm text-gray-400">
							{segResult.no_segment_reason ?? 'No segment disclosure extracted for this ticker.'}
						</p>
					{/if}
				{/if}
			</Accordion.Content>
		</Accordion.Item>
	</Accordion.Root>
</div>
