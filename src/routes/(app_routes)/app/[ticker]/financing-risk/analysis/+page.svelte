<script lang="ts">
	import { page } from '$app/stores';
	import { marked } from 'marked';
	import DOMPurify from 'isomorphic-dompurify';

	const apiUrl = import.meta.env.VITE_API_URL;

	type DisplayMode = 'original' | 'summary';

	let analysisLoading = $state(false);
	let analysisError = $state<string | null>(null);
	let financingRiskJson = $state<Record<string, unknown> | null>(null);
	let financingRiskRaw = $state<string | null>(null);
	let financingRiskNarrative = $state<string | null>(null);
	let financingRiskSummary = $state<string | null>(null);
	let filingDate = $state<string | null>(null);
	let displayMode = $state<DisplayMode>('original');

	const ticker = $derived($page.params.ticker?.toUpperCase() ?? '');

	// Original = raw SEC filing text; Summary = AI analysis (key points + full narrative)
	const displayContent = $derived(
		displayMode === 'original'
			? (financingRiskRaw ?? '')
			: [financingRiskSummary, financingRiskNarrative].filter(Boolean).join('\n\n---\n\n')
	);

	const displayHtml = $derived(
		displayContent
			? DOMPurify.sanitize(marked.parse(displayContent) as string, { USE_PROFILES: { html: true } })
			: ''
	);

	const hasAnalysis = $derived(
		!!financingRiskRaw || !!financingRiskNarrative || !!financingRiskSummary || !!financingRiskJson
	);

	async function runFinancingRiskAnalysis() {
		if (!ticker) return;
		analysisLoading = true;
		analysisError = null;
		financingRiskJson = null;
		financingRiskRaw = null;
		financingRiskNarrative = null;
		financingRiskSummary = null;
		filingDate = null;
		try {
			const res = await fetch(`${apiUrl}/analysis/financing-risk/${ticker}`, {
				method: 'POST'
			});
			const json = await res.json();
			if (!res.ok) {
				throw new Error(json.detail ?? `Request failed: ${res.status}`);
			}
			financingRiskJson = json.financing_risk_json ?? null;
			financingRiskRaw = json.financing_risk_raw ?? null;
			financingRiskNarrative = json.financing_risk_narrative ?? null;
			financingRiskSummary = json.financing_risk_summary ?? null;
			filingDate = json.filing_date ?? null;
		} catch (e) {
			analysisError = e instanceof Error ? e.message : 'Failed to fetch financing risk analysis';
		} finally {
			analysisLoading = false;
		}
	}
</script>

<div class="space-y-6">
	<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
		<div>
			<h1 class="font-mono text-xl text-green-500">Financing Risk Analysis</h1>
			<p class="mt-1 text-sm text-gray-400">
				AI analysis of liquidity, debt, covenants, and refinancing risk from the latest Form 10-Q.
			</p>
		</div>
		<button
			class="w-fit rounded border border-amber-400/30 px-4 py-2 font-mono text-sm text-amber-400 hover:bg-amber-400/10 hover:text-amber-300 disabled:opacity-50"
			onclick={runFinancingRiskAnalysis}
			disabled={analysisLoading || !ticker}
		>
			{analysisLoading ? '⏳ Fetching 10-Q & analyzing...' : '🤖 Run Financing Risk Analysis'}
		</button>
	</div>

	{#if analysisLoading}
		<div class="rounded-lg border border-gray-700/50 bg-gray-900/40 p-6">
			<p class="text-sm text-gray-400">
				Fetching latest 10-Q from SEC, extracting financing sections, and generating analysis. This may take 30–90 seconds.
			</p>
		</div>
	{:else if analysisError}
		<div class="rounded-lg border border-red-900/50 bg-red-950/20 p-4">
			<p class="text-sm text-red-400">{analysisError}</p>
			<p class="mt-2 text-xs text-gray-500">
				Ensure SEC_API_KEY is set in the backend .env (sec-api.io) and OPENROUTER_API_KEY_GEMINI is configured.
			</p>
		</div>
	{:else if hasAnalysis}
		<div class="rounded-lg border border-gray-700/50 bg-gray-900/40 p-6">
			<div class="mb-4 flex flex-wrap items-center justify-between gap-2">
				<div class="flex items-center gap-2">
					{#if filingDate}
						<span class="font-mono text-xs text-gray-500">Based on 10-Q filed {filingDate}</span>
					{/if}
				</div>
				<div class="flex gap-1 rounded border border-gray-700/50 p-0.5">
					<button
						class="rounded px-3 py-1 font-mono text-xs transition-colors {displayMode === 'original'
							? 'bg-amber-500/20 text-amber-400'
							: 'text-gray-400 hover:text-gray-300'}"
						onclick={() => (displayMode = 'original')}
					>
						Original
					</button>
					<button
						class="rounded px-3 py-1 font-mono text-xs transition-colors {displayMode === 'summary'
							? 'bg-amber-500/20 text-amber-400'
							: 'text-gray-400 hover:text-gray-300'}"
						onclick={() => (displayMode = 'summary')}
					>
						Summary
					</button>
				</div>
			</div>
			<div
				class="prose prose-invert prose-sm max-w-none text-gray-300 [&_h2]:mt-4 [&_h2]:text-amber-400 [&_h3]:mt-3 [&_h3]:text-amber-300/90 [&_h4]:mt-2 [&_h4]:text-amber-200/80 [&_ul]:list-disc [&_ul]:pl-5 [&_pre]:overflow-x-auto [&_pre]:rounded [&_pre]:bg-gray-800/50 [&_pre]:p-3"
			>
				{@html displayHtml}
			</div>
		</div>
	{:else}
		<div class="rounded-lg border border-dashed border-gray-700/50 bg-gray-900/20 p-8 text-center">
			<p class="text-sm text-gray-500">
				Click <span class="font-mono text-amber-400">Run Financing Risk Analysis</span> to analyze
				{ticker || 'this ticker'}'s latest 10-Q.
			</p>
		</div>
	{/if}
</div>
