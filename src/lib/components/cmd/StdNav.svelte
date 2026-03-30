<script lang="ts">
	import { ChevronDown, LineChart, PieChart, DollarSign, BarChart2, ShieldAlert } from 'lucide-svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let { ticker = '' } = $props<{ ticker?: string }>();

	let isOpen = $state(false);
	let tickerInput = $state('');
	let showTickerInput = $state(false);
	let inputRef: HTMLInputElement;

	const sections = [
		{
			name: 'Balance Sheet',
			path: 'balancesheet',
			icon: PieChart,
			subsections: ['Annual', 'Quarterly']
		},
		{
			name: 'Cash Flow',
			path: 'cashflow',
			icon: DollarSign,
			subsections: ['Annual', 'Quarterly']
		},
		{
			name: 'Income Statement',
			path: 'incomestatement',
			icon: BarChart2,
			subsections: ['Annual', 'Quarterly']
		},
		{
			name: 'Valuation',
			path: 'valuation',
			icon: LineChart,
			subsections: ['Quarterly']
		},
		{
			name: 'Financing Risk',
			path: 'financing-risk',
			icon: ShieldAlert,
			subsections: ['Analysis']
		}
	];

	function handleTickerSubmit() {
		if (tickerInput.trim()) {
			const newTicker = tickerInput.toUpperCase();
			goto(`/app/${newTicker}`);
			showTickerInput = false;
			tickerInput = '';
		}
	}

	function toggleNav() {
		isOpen = !isOpen;
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if ((isOpen || showTickerInput) && target && !target.closest('.nav-container')) {
			isOpen = false;
			showTickerInput = false;
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleTickerSubmit();
		} else if (event.key === 'Escape') {
			showTickerInput = false;
			tickerInput = '';
		}
	}

	function showTickerSelector() {
		showTickerInput = true;
		requestAnimationFrame(() => {
			inputRef?.focus();
		});
	}
</script>

<svelte:window onclick={handleClickOutside} />

<nav class="nav-container relative flex items-center gap-2">
	{#if !showTickerInput}
		<button
			onclick={showTickerSelector}
			class="flex items-center gap-2 rounded-md bg-background/80 px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
			aria-label="Select ticker symbol"
		>
			<span class="font-mono">{ticker || 'Select Ticker'}</span>
			<ChevronDown class="h-4 w-4" />
		</button>
	{:else}
		<div class="relative">
			<input
				type="text"
				bind:this={inputRef}
				bind:value={tickerInput}
				placeholder="Enter ticker..."
				onkeydown={handleKeydown}
				class="w-32 rounded-md bg-background/80 px-3 py-1.5 font-mono text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
				aria-label="Enter ticker symbol"
			/>
		</div>
	{/if}

	{#if ticker}
		<button
			onclick={toggleNav}
			class="flex items-center gap-2 rounded-md px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
			aria-expanded={isOpen}
			aria-haspopup="true"
		>
			Navigate
			<ChevronDown class="h-4 w-4 transform transition-transform {isOpen ? 'rotate-180' : ''}" />
		</button>

		{#if isOpen}
			<div
				class="absolute right-0 top-full z-[60] mt-1 w-48 rounded-md border border-border bg-popover shadow-lg"
				role="menu"
			>
				{#each sections as section}
					<div class="py-1">
						<div class="flex items-center gap-2 px-3 py-1 text-sm font-medium">
							<svelte:component this={section.icon} class="h-4 w-4" />
							{section.name}
						</div>
						<div class="pl-2">
							{#each section.subsections as subsection}
								<a
									href="/app/{ticker}/{section.path}/{subsection.toLowerCase()}"
									class="block px-3 py-1 text-xs text-muted-foreground hover:bg-accent/50 hover:text-accent-foreground"
									role="menuitem"
								>
									{subsection}
								</a>
							{/each}
						</div>
					</div>
				{/each}
			</div>
		{/if}
	{/if}
</nav>

<style>
	:global(.nav-container) {
		position: relative;
		z-index: 60;
	}
</style>
