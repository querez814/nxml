<script lang="ts">
	// Define our types first for better type safety
	type Section = {
		id: string;
		title: string;
		content: string;
	};

	type ExpandedState = {
		[key: string]: boolean;
	};

	// Create our state using proper Runes syntax
	let activeSection = $state('overview');
	let expandedSections = $state<ExpandedState>({});

	// Sections data with proper typing
	const sections: Section[] = [
		{
			id: 'overview',
			title: 'Momentum Score Calculation',
			content: `The final momentum score is a weighted combination of multiple technical indicators:
            • MACD (30%): Measures trend direction and strength
            • Aroon Oscillator (25%): Identifies trend changes
            • Momentum (25%): Shows price velocity
            • Stochastic (10%): Indicates overbought/oversold conditions
            • Trend Consistency (10%): Overall trend reliability`
		},
		{
			id: 'components',
			title: 'Component Calculations',
			content: `Each component score is normalized to a -100 to +100 scale:
            1. Calculate recent (10 days) vs historical (10-20 days) averages
            2. Measure volatility using standard deviation
            3. Normalize the difference: ((recent - historical) / volatility) * 50
            4. Clamp final values between -100 and +100`
		},
		{
			id: 'trends',
			title: 'Trend Analysis',
			content: `Market conditions are determined by:
            1. Calculate trend consistency (75%+ = Strong, 50-75% = Moderate)
            2. Count component trend directions (up vs down)
            3. Combine for final classification:
               • STRONG_UPTREND: High consistency + majority up
               • MODERATE_UPTREND: Medium consistency + majority up
               • CONSOLIDATION: Low consistency
               • MODERATE_DOWNTREND: Medium consistency + majority down
               • STRONG_DOWNTREND: High consistency + majority down`
		}
	];

	// Properly typed function for toggling sections
	function toggleSection(id: string): void {
		expandedSections[id] = !expandedSections[id];
	}

	// Derived state using Runes
	const isExpanded = $derived((id: string) => expandedSections[id] ?? false);
</script>

<div class="mx-auto max-w-3xl rounded-lg bg-gray-900 p-6 text-gray-100 shadow-xl">
	<h2 class="mb-6 text-3xl font-bold text-green-500">Market Momentum Analysis</h2>

	{#each sections as section}
		<div class="mb-4">
			<button
				class="w-full rounded-lg bg-gray-800 p-4 text-left transition-colors hover:bg-gray-700"
				onclick={() => toggleSection(section.id)}
			>
				<div class="flex items-center justify-between">
					<h3 class="text-xl font-semibold text-green-400">{section.title}</h3>
					<span class="text-green-500">
						{isExpanded(section.id) ? '−' : '+'}
					</span>
				</div>
			</button>

			{#if isExpanded(section.id)}
				<div class="mt-2 rounded-lg bg-gray-800 p-4 leading-relaxed text-gray-300">
					<p class="whitespace-pre-line">{section.content}</p>

					{#if section.id === 'overview'}
						<div class="mt-4 grid grid-cols-2 gap-4">
							<div class="rounded bg-gray-700 p-3">
								<div class="text-sm text-green-400">Example Score</div>
								<div class="text-2xl font-bold">37.7</div>
								<div class="text-xs text-gray-400">SPY Momentum</div>
							</div>
							<div class="rounded bg-gray-700 p-3">
								<div class="text-sm text-green-400">Market Condition</div>
								<div class="text-xl font-bold">STRONG UPTREND</div>
								<div class="text-xs text-gray-400">83.9% Consistency</div>
							</div>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	:global(body) {
		background-color: #0a0a0a;
	}
</style>
