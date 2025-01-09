<script lang="ts">
	import '../../../../app.css';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import CommandLine from '$lib/components/cmd/CommandLine.svelte';
	import StdNav from '$lib/components/cmd/StdNav.svelte';
	import * as Toggle from '$lib/components/ui/toggle';
	import { Terminal } from 'lucide-svelte';
	import { afterNavigate } from '$app/navigation';
	import { invalidate } from '$app/navigation';

	let showCommandLine = $state(true);
	let ticker = $derived($page.params.ticker?.toUpperCase() ?? '');
	let key = $state(0);

	afterNavigate(() => {
		key++;
	});

	async function handleTickerChange(newTicker: string) {
		if (newTicker !== ticker) {
			goto(`/app/${newTicker}`);
		} else {
			key++;
			await invalidate('app:data');
		}
	}

	function handlePressedChange(pressed: boolean) {
		showCommandLine = pressed;
	}
</script>

<div class="min-h-screen bg-gray-950">
	<div class="fixed left-0 right-0 top-0 z-20">
		<div class="flex h-14 items-center justify-between bg-gray-900/30 px-4 backdrop-blur-sm">
			<div class="flex items-center gap-4">
				<a href="/" class="font-mono text-xl text-green-500">InvestorTerminal</a>
				<Toggle.Root
					pressed={showCommandLine}
					onPressedChange={handlePressedChange}
					class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground data-[state=on]:bg-accent/50"
					aria-label="Toggle command line"
				>
					<Terminal class="h-4 w-4" />
				</Toggle.Root>
			</div>
			<div class="flex items-center gap-4">
				<StdNav {ticker} />
			</div>
		</div>

		{#if showCommandLine}
			<div
				class="border-t border-gray-800/50 bg-gray-900/20 px-4 py-2 backdrop-blur-sm transition-all duration-200 ease-in-out"
			>
				<CommandLine onTickerChange={handleTickerChange} />
			</div>
		{/if}
	</div>

	<main class="container mx-auto px-4" class:pt-28={showCommandLine} class:pt-16={!showCommandLine}>
		{#key key}
			<slot />
		{/key}
	</main>
</div>

<style>
	:global(body) {
		background-color: rgb(3 7 18);
	}
</style>
